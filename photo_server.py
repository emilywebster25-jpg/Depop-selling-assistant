#!/usr/bin/env python3
"""
Simple web server for the Depop Photo Organizer
Serves photos from the staging folder and handles photo organization
"""

import http.server
import socketserver
import json
import os
import shutil
import csv
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse, quote, unquote
import base64
import mimetypes
from PIL import Image
import io

# Register HEIC plugin
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    print("✅ HEIC support loaded")
except ImportError:
    print("❌ HEIC support not available - install pillow-heif")

class PhotoOrganizerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.project_path = Path("/Users/emilywebster/Dev/Depop_Selling")
        self.staging_path = self.project_path / "photos" / "staging"
        self.category_path = self.project_path / "photos" / "by_category"
        self.ready_for_depop_path = self.project_path / "photos" / "ready_for_depop"
        self.inventory_path = self.project_path / "data" / "inventory_tracker.csv"
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/photo_organizer.html'
        
        if self.path == '/api/photos':
            self.serve_photos_list()
        elif self.path.startswith('/api/photo/'):
            self.serve_photo_file()
        elif self.path.startswith('/api/category-photo/'):
            self.serve_category_photo_file()
        elif self.path == '/api/stats':
            self.serve_stats()
        elif self.path == '/api/completed-items':
            self.serve_completed_items()
        elif self.path.startswith('/api/open-folder/'):
            self.handle_open_folder()
        else:
            return super().do_GET()
    
    def do_POST(self):
        print(f"🔧 POST request received: {self.path}")
        if self.path == '/api/save-item':
            print("🔧 Routing to handle_save_item")
            self.handle_save_item()
        else:
            print(f"🔧 Unknown POST path: {self.path}")
            self.send_error(404)
    
    def do_DELETE(self):
        if self.path.startswith('/api/delete-item/'):
            self.handle_delete_item()
        else:
            self.send_error(404)
    
    def serve_photos_list(self):
        """Return list of photos in staging folder"""
        try:
            photos = []
            image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.HEIC'}
            
            if self.staging_path.exists():
                for file_path in self.staging_path.iterdir():
                    if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                        stat = file_path.stat()
                        photos.append({
                            'id': str(hash(file_path.name)),
                            'name': file_path.name,
                            'size': f"{stat.st_size / 1024 / 1024:.1f} MB",
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                            'url': f'/api/photo/{file_path.name}'
                        })
            
            # Sort photos by filename (chronological for IMG_XXXX format)
            photos.sort(key=lambda x: x['name'])
            
            self.send_json_response(photos)
        except Exception as e:
            self.send_error(500, f"Error loading photos: {str(e)}")
    
    def serve_photo_file(self):
        """Serve individual photo files, converting HEIC to JPEG"""
        try:
            filename = self.path.split('/')[-1]
            file_path = self.staging_path / filename
            
            if not file_path.exists():
                self.send_error(404, "Photo not found")
                return
            
            # Check if it's a HEIC file that needs conversion
            if file_path.suffix.upper() in ['.HEIC', '.HEIF']:
                try:
                    # Convert HEIC to JPEG with smaller size for web
                    with Image.open(file_path) as img:
                        # Convert to RGB if necessary
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Resize for web display (max 800px)
                        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                        
                        # Create JPEG in memory
                        jpeg_buffer = io.BytesIO()
                        img.save(jpeg_buffer, format='JPEG', quality=75, optimize=True)
                        jpeg_data = jpeg_buffer.getvalue()
                        
                        # Send JPEG response
                        self.send_response(200)
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', str(len(jpeg_data)))
                        self.send_header('Cache-Control', 'max-age=3600')  # Cache for 1 hour
                        self.end_headers()
                        
                        # Write data in chunks to prevent timeout
                        chunk_size = 8192
                        for i in range(0, len(jpeg_data), chunk_size):
                            chunk = jpeg_data[i:i + chunk_size]
                            self.wfile.write(chunk)
                            
                        return
                        
                except Exception as convert_error:
                    print(f"Error converting HEIC {filename}: {convert_error}")
                    # Return a simple error response instead of falling back
                    self.send_response(500)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b"HEIC conversion failed")
                    return
            
            # Serve original file (JPG, PNG, etc.)
            content_type, _ = mimetypes.guess_type(str(file_path))
            if content_type is None:
                content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(file_path.stat().st_size))
            self.send_header('Cache-Control', 'max-age=3600')  # Cache for 1 hour
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)
                
        except (BrokenPipeError, ConnectionResetError):
            # Client disconnected, ignore
            pass
        except Exception as e:
            try:
                self.send_error(500, f"Error serving photo: {str(e)}")
            except (BrokenPipeError, ConnectionResetError):
                # Client disconnected while sending error, ignore
                pass
    
    def serve_category_photo_file(self):
        """Serve photos from category folders, converting HEIC to JPEG"""
        try:
            # Parse path like /api/category-photo/tops/IMG_3058_1.HEIC
            path_parts = self.path.split('/')
            if len(path_parts) < 5:
                self.send_error(400, "Invalid category photo path")
                return
            
            category = unquote(path_parts[3])
            filename = unquote(path_parts[4])
            file_path = self.category_path / category / filename
            
            print(f"Looking for photo: {file_path}")
            print(f"Category: '{category}'")
            print(f"Filename: '{filename}'")
            print(f"File exists: {file_path.exists()}")
            
            if not file_path.exists():
                self.send_error(404, "Category photo not found")
                return
            
            # Check if it's a HEIC file that needs conversion
            if file_path.suffix.upper() in ['.HEIC', '.HEIF']:
                try:
                    # Convert HEIC to JPEG with smaller size for web
                    with Image.open(file_path) as img:
                        # Convert to RGB if necessary
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Resize for web display (max 800px)
                        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                        
                        # Create JPEG in memory
                        jpeg_buffer = io.BytesIO()
                        img.save(jpeg_buffer, format='JPEG', quality=75, optimize=True)
                        jpeg_data = jpeg_buffer.getvalue()
                        
                        # Send JPEG response
                        self.send_response(200)
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', str(len(jpeg_data)))
                        self.send_header('Cache-Control', 'max-age=3600')  # Cache for 1 hour
                        self.end_headers()
                        
                        # Write data in chunks to prevent timeout
                        chunk_size = 8192
                        for i in range(0, len(jpeg_data), chunk_size):
                            chunk = jpeg_data[i:i + chunk_size]
                            self.wfile.write(chunk)
                        
                        return
                except Exception as e:
                    print(f"Error converting HEIC from category: {e}")
                    self.send_error(500, f"Error converting HEIC: {str(e)}")
                    return
            
            # Serve original file (JPG, PNG, etc.)
            content_type, _ = mimetypes.guess_type(str(file_path))
            if content_type is None:
                content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(file_path.stat().st_size))
            self.send_header('Cache-Control', 'max-age=3600')  # Cache for 1 hour
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)
                
        except (BrokenPipeError, ConnectionResetError):
            # Client disconnected, ignore
            pass
        except Exception as e:
            try:
                self.send_error(500, f"Error serving category photo: {str(e)}")
            except (BrokenPipeError, ConnectionResetError):
                # Client disconnected while sending error, ignore
                pass
    
    def serve_stats(self):
        """Return current stats"""
        try:
            # Count photos in staging
            staging_count = 0
            image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.HEIC'}
            
            if self.staging_path.exists():
                staging_count = len([f for f in self.staging_path.iterdir() 
                                   if f.is_file() and f.suffix.lower() in image_extensions])
            
            # Count completed items from CSV
            completed_count = 0
            if self.inventory_path.exists():
                try:
                    with open(self.inventory_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        completed_count = sum(1 for row in reader)
                except:
                    pass
            
            stats = {
                'totalPhotos': staging_count,
                'completedItems': completed_count,
                'estimatedItemsRemaining': max(0, staging_count // 4)  # Rough estimate
            }
            
            self.send_json_response(stats)
        except Exception as e:
            self.send_error(500, f"Error getting stats: {str(e)}")
    
    def serve_completed_items(self):
        """Return list of completed items from CSV"""
        try:
            items = []
            if self.inventory_path.exists():
                with open(self.inventory_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Convert CSV row to the format expected by the client
                        photos = []
                        category = row.get('Category', '').lower()
                        for i in range(1, 5):  # Photo_1 through Photo_4
                            photo_col = f'Photo_{i}'
                            if row.get(photo_col):
                                photo_filename = row[photo_col]
                                # Construct proper photo object with URL pointing to category folder
                                photos.append({
                                    'id': str(hash(photo_filename)),
                                    'name': photo_filename,
                                    'url': f'/api/category-photo/{quote(category)}/{quote(photo_filename)}'
                                })
                        
                        item = {
                            'id': row['Item_ID'],
                            'brand': row.get('Brand', ''),
                            'category': row.get('Category', ''),
                            'itemType': row.get('Item_Type', ''),
                            'size': row.get('Size', ''),
                            'color': row.get('Color', ''),
                            'condition': row.get('Condition', ''),
                            'purchasePrice': row.get('Purchase_Price', ''),
                            'targetPrice': row.get('Target_Price', ''),
                            'notes': row.get('Notes', ''),
                            'photos': photos,
                            'dateAdded': row.get('Date_Added', ''),
                            'hashtags': row.get('Hashtags', ''),
                            'title': row.get('Title', ''),
                            'description': row.get('Description', ''),
                            'depopFolder': row.get('Depop_Folder', '')
                        }
                        items.append(item)
            
            self.send_json_response(items)
        except Exception as e:
            self.send_error(500, f"Error loading completed items: {str(e)}")
    
    def handle_save_item(self):
        """Save a completed item to inventory (create new or update existing)"""
        try:
            print("🔧 handle_save_item called")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Check if we're editing an existing item
            is_editing = 'itemId' in data and data['itemId']
            
            if is_editing:
                # Update existing item
                item_id = data['itemId']
                self.update_inventory_item(data, item_id)
                response = {
                    'success': True,
                    'itemId': item_id,
                    'message': f'Item {item_id} updated successfully!'
                }
            else:
                # Create new item
                print("🔧 Creating new item")
                next_id = self.get_next_item_id()
                print(f"🔧 Next ID: {next_id}")
                
                # Create item-specific folder for Depop uploads
                item_folder, folder_name = self.create_item_folder(
                    next_id, 
                    data.get('title', ''), 
                    data.get('brand', ''), 
                    data.get('color', '')
                )
                
                # Process and copy photos to both category and item folders
                photo_filenames = []
                
                for i, photo_name in enumerate(data['photos'][:4]):  # Max 4 photos
                    old_path = self.staging_path / photo_name
                    if old_path.exists():
                        new_filename = self.move_photo_dual(old_path, data['category'], item_folder, i + 1)
                        photo_filenames.append(new_filename)
                
                # Add to inventory CSV (including folder name for tracking)
                self.add_to_inventory(data, photo_filenames, next_id, folder_name)
                
                response = {
                    'success': True,
                    'itemId': next_id,
                    'message': f'Item {next_id} saved successfully!'
                }
            
            self.send_json_response(response)
            
        except Exception as e:
            print(f"🔧 ERROR in handle_save_item: {str(e)}")
            print(f"🔧 Exception type: {type(e).__name__}")
            import traceback
            print(f"🔧 Traceback: {traceback.format_exc()}")
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status_code=500)
    
    def handle_delete_item(self):
        """Delete a completed item and its copied photos"""
        try:
            # Extract item ID from URL path
            item_id = self.path.split('/')[-1]
            
            if not self.inventory_path.exists():
                self.send_json_response({
                    'success': False,
                    'error': 'No inventory file found'
                }, status_code=404)
                return
            
            # Read current CSV and find the item to delete
            rows_to_keep = []
            item_found = False
            item_photos = []
            item_category = ""
            item_folder_name = ""
            
            with open(self.inventory_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Item_ID'] == item_id:
                        item_found = True
                        item_category = row['Category'].lower()
                        item_folder_name = row.get('Depop_Folder', '')
                        # Collect photo filenames to delete
                        for i in range(1, 5):
                            photo_col = f'Photo_{i}'
                            if row.get(photo_col):
                                item_photos.append(row[photo_col])
                    else:
                        rows_to_keep.append(row)
            
            if not item_found:
                self.send_json_response({
                    'success': False,
                    'error': f'Item {item_id} not found'
                }, status_code=404)
                return
            
            # Delete copied photos from category folder
            category_folder = self.category_path / item_category
            for photo_filename in item_photos:
                photo_path = category_folder / photo_filename
                if photo_path.exists():
                    photo_path.unlink()  # Delete the file
            
            # Delete item-specific folder from ready_for_depop directory
            if item_folder_name:
                item_folder = self.ready_for_depop_path / item_folder_name
                if item_folder.exists():
                    import shutil
                    shutil.rmtree(item_folder)  # Delete entire folder and contents
            
            # Rewrite CSV without the deleted item
            with open(self.inventory_path, 'w', newline='', encoding='utf-8') as file:
                if rows_to_keep:
                    fieldnames = list(rows_to_keep[0].keys())
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows_to_keep)
                else:
                    # If no rows left, write just headers
                    fieldnames = ['Item_ID', 'Brand', 'Category', 'Subcategory', 'Title', 'Description', 
                                'Style', 'Source', 'Age', 'Size', 'Color', 'Condition',
                                'Purchase_Price', 'Target_Price', 'Actual_Sale_Price',
                                'Parcel_Size', 'International_Shipping', 'City',
                                'Photo_1', 'Photo_2', 'Photo_3', 'Photo_4', 
                                'Hashtags', 'Status', 'Date_Added', 'Date_Listed', 'Date_Sold', 
                                'Likes', 'Views', 'Notes', 'Depop_Folder']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
            
            self.send_json_response({
                'success': True,
                'message': f'Item {item_id} deleted successfully',
                'freedPhotos': item_photos  # Return list of photos that are now available again
            })
            
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status_code=500)
    
    def handle_open_folder(self):
        """Open the item-specific folder in macOS Finder"""
        try:
            # Extract folder name from URL path
            folder_name = self.path.split('/')[-1]
            
            if not folder_name:
                self.send_json_response({
                    'success': False,
                    'error': 'No folder name provided'
                }, status_code=400)
                return
            
            # Construct full path to the folder
            folder_path = self.ready_for_depop_path / folder_name
            
            if not folder_path.exists():
                self.send_json_response({
                    'success': False,
                    'error': f'Folder {folder_name} does not exist'
                }, status_code=404)
                return
            
            # Open folder in macOS Finder
            import subprocess
            subprocess.run(['open', str(folder_path)], check=True)
            
            self.send_json_response({
                'success': True,
                'message': f'Opened folder: {folder_name}'
            })
            
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status_code=500)
    
    def get_next_item_id(self):
        """Get the next available item ID"""
        if not self.inventory_path.exists():
            return "DP004"
        
        max_id = 3  # Start from DP004
        try:
            with open(self.inventory_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Item_ID'].startswith('DP'):
                        try:
                            id_num = int(row['Item_ID'][2:])  # Remove 'DP' prefix
                            max_id = max(max_id, id_num)
                        except ValueError:
                            continue
        except Exception:
            pass
        
        return f"DP{(max_id + 1):03d}"
    
    def generate_filename(self, data):
        """Generate base filename from item data"""
        import re
        
        brand = re.sub(r'[^a-zA-Z0-9]', '', data.get('brand', 'item').lower())
        color = re.sub(r'[^a-zA-Z0-9]', '', data.get('color', 'unknown').lower())
        item_type = re.sub(r'[^a-zA-Z0-9]', '', data.get('itemType', 'clothing').lower())
        
        return f"{brand}_{color}_{item_type}"
    
    def sanitize_folder_name(self, name):
        """Sanitize folder name for filesystem compatibility"""
        import re
        # Remove or replace problematic characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Remove excessive whitespace and replace with underscores
        sanitized = re.sub(r'\s+', '_', sanitized.strip())
        # Remove leading/trailing underscores and periods
        sanitized = sanitized.strip('_.')
        # Limit length to 100 characters
        return sanitized[:100] if sanitized else "Untitled_Item"
    
    def generate_item_folder_name(self, item_id, title, brand, color):
        """Generate a descriptive folder name for the item"""
        parts = [f"Item_{item_id}"]
        
        if brand and brand != "Other":
            parts.append(brand)
        
        if color and color != "N/A":
            parts.append(color)
            
        if title:
            # Use first 3 words of title
            title_words = title.split()[:3]
            parts.extend(title_words)
        
        folder_name = "_".join(parts)
        return self.sanitize_folder_name(folder_name)
    
    def create_item_folder(self, item_id, title, brand, color):
        """Create item-specific folder in ready_for_depop directory"""
        folder_name = self.generate_item_folder_name(item_id, title, brand, color)
        item_folder = self.ready_for_depop_path / folder_name
        item_folder.mkdir(parents=True, exist_ok=True)
        return item_folder, folder_name
    
    def move_photo(self, old_path, category, base_name, photo_number):
        """Move photo to appropriate category folder keeping original filename"""
        category_folder = self.category_path / category.lower()
        category_folder.mkdir(parents=True, exist_ok=True)
        
        # Keep the original filename
        original_filename = old_path.name
        new_path = category_folder / original_filename
        
        # Handle duplicate filenames by adding a number suffix before the extension
        counter = 1
        while new_path.exists():
            name_part = old_path.stem
            extension = old_path.suffix
            duplicate_filename = f"{name_part}_{counter}{extension}"
            new_path = category_folder / duplicate_filename
            original_filename = duplicate_filename
            counter += 1
        
        shutil.copy2(str(old_path), str(new_path))
        return original_filename
    
    def move_photo_dual(self, old_path, category, item_folder, photo_number):
        """Move photo to both category folder and item-specific folder"""
        # Keep the original filename
        original_filename = old_path.name
        
        # 1. Copy to category folder (existing functionality)
        category_folder = self.category_path / category.lower()
        category_folder.mkdir(parents=True, exist_ok=True)
        
        category_new_path = category_folder / original_filename
        # Handle duplicate filenames in category folder
        counter = 1
        while category_new_path.exists():
            name_part = old_path.stem
            extension = old_path.suffix
            duplicate_filename = f"{name_part}_{counter}{extension}"
            category_new_path = category_folder / duplicate_filename
            counter += 1
        
        shutil.copy2(str(old_path), str(category_new_path))
        
        # 2. Copy to item-specific folder
        item_new_path = item_folder / original_filename
        # Handle duplicate filenames in item folder
        counter = 1
        while item_new_path.exists():
            name_part = old_path.stem
            extension = old_path.suffix
            duplicate_filename = f"{name_part}_{counter}{extension}"
            item_new_path = item_folder / duplicate_filename
            counter += 1
        
        shutil.copy2(str(old_path), str(item_new_path))
        
        return original_filename
    
    def add_to_inventory(self, data, photo_filenames, item_id, folder_name=None):
        """Add item to inventory CSV"""
        # Extract hashtags from description or generate them
        hashtags = self.extract_hashtags_from_description(data.get('description', '')) or self.generate_hashtags(data.get('category'), data.get('brand'))
        
        # Combine category and subcategory
        category_full = data.get('category', '')
        if data.get('subcategory'):
            category_full += f" > {data.get('subcategory')}"
        
        row_data = {
            'Item_ID': item_id,
            'Brand': data.get('brand', ''),
            'Category': category_full,
            'Subcategory': data.get('subcategory', ''),
            'Title': data.get('title', ''),
            'Description': data.get('description', ''),
            'Style': data.get('style', ''),
            'Source': data.get('source', ''),
            'Age': data.get('age', ''),
            'Size': data.get('size', ''),
            'Color': data.get('color', ''),
            'Condition': data.get('condition', ''),
            'Purchase_Price': data.get('purchasePrice', ''),
            'Target_Price': data.get('targetPrice', ''),
            'Actual_Sale_Price': '',
            'Parcel_Size': data.get('parcelSize', ''),
            'International_Shipping': data.get('internationalShipping', 'No'),
            'City': data.get('city', ''),
            'Photo_1': photo_filenames[0] if len(photo_filenames) > 0 else '',
            'Photo_2': photo_filenames[1] if len(photo_filenames) > 1 else '',
            'Photo_3': photo_filenames[2] if len(photo_filenames) > 2 else '',
            'Photo_4': photo_filenames[3] if len(photo_filenames) > 3 else '',
            'Hashtags': hashtags,
            'Status': 'Not Listed',
            'Date_Added': datetime.now().strftime('%Y-%m-%d'),
            'Date_Listed': '',
            'Date_Sold': '',
            'Likes': '0',
            'Views': '0',
            'Notes': data.get('notes', ''),
            'Depop_Folder': folder_name or ''
        }
        
        # Write to CSV
        file_exists = self.inventory_path.exists()
        
        with open(self.inventory_path, 'a', newline='', encoding='utf-8') as file:
            fieldnames = list(row_data.keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row_data)
    
    def update_inventory_item(self, data, item_id):
        """Update an existing item in the inventory CSV"""
        if not self.inventory_path.exists():
            raise Exception("Inventory file not found")
        
        # Read all rows
        rows = []
        updated = False
        
        with open(self.inventory_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            
            for row in reader:
                if row['Item_ID'] == item_id:
                    # Combine category and subcategory
                    category_full = data.get('category', '')
                    if data.get('subcategory'):
                        category_full += f" > {data.get('subcategory')}"
                    
                    # Update this row with new data (but keep photos unchanged)
                    row.update({
                        'Brand': data.get('brand', ''),
                        'Category': category_full,
                        'Subcategory': data.get('subcategory', ''),
                        'Title': data.get('title', ''),
                        'Description': data.get('description', ''),
                        'Style': data.get('style', ''),
                        'Source': data.get('source', ''),
                        'Age': data.get('age', ''),
                        'Size': data.get('size', ''),
                        'Color': data.get('color', ''),
                        'Condition': data.get('condition', ''),
                        'Purchase_Price': data.get('purchasePrice', ''),
                        'Target_Price': data.get('targetPrice', ''),
                        'Parcel_Size': data.get('parcelSize', ''),
                        'International_Shipping': data.get('internationalShipping', 'No'),
                        'City': data.get('city', ''),
                        'Hashtags': self.extract_hashtags_from_description(data.get('description', '')),
                        'Notes': data.get('notes', ''),
                    })
                    updated = True
                rows.append(row)
        
        if not updated:
            raise Exception(f"Item {item_id} not found")
        
        # Write back all rows
        with open(self.inventory_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    
    def extract_hashtags_from_description(self, description):
        """Extract hashtags from description text"""
        import re
        if not description:
            return ""
        
        # Find all hashtags in the description
        hashtags = re.findall(r'#\w+', description)
        # Limit to 5 hashtags as per Depop's limit
        return ' '.join(hashtags[:5])
    
    def generate_hashtags(self, category, brand):
        """Generate hashtags for the item"""
        hashtag_bank = {
            'tops': ['#top', '#shirt', '#blouse', '#workwear', '#casual'],
            'dresses': ['#dress', '#midi', '#party', '#formal', '#cottagecore'],
            'bottoms': ['#jeans', '#trousers', '#y2k', '#highwaisted', '#vintage'],
            'outerwear': ['#jacket', '#coat', '#blazer', '#oversized', '#structured'],
            'shoes': ['#shoes', '#boots', '#sneakers', '#platform', '#chunky'],
            'accessories': ['#accessories', '#bag', '#jewelry', '#vintage', '#statement']
        }
        
        tags = []
        
        if category and category.lower() in hashtag_bank:
            tags.extend(hashtag_bank[category.lower()][:3])
        
        if brand:
            tags.append(f"#{brand.lower()}")
        
        tags.append('#preloved')
        
        return ' '.join(tags[:5])
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_server():
    PORT = 8001
    project_path = Path("/Users/emilywebster/Dev/Depop_Selling")
    
    print("🚀 Starting Depop Photo Organizer Server...")
    print("=" * 50)
    print(f"📂 Project: {project_path}")
    print(f"🌐 Server: http://localhost:{PORT}")
    print(f"📸 Photos: {project_path / 'photos' / 'staging'}")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(str(project_path))
    
    # Start server
    with socketserver.TCPServer(("", PORT), PhotoOrganizerHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        print("📱 Open this URL in your browser to use the photo organizer")
        print("🛑 Press Ctrl+C to stop the server")
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")
            print("✨ Thanks for using Depop Photo Organizer!")

if __name__ == "__main__":
    run_server()