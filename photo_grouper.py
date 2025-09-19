#!/usr/bin/env python3
"""
Enhanced Depop Photo Analyzer - Multi-Photo Item Grouping
Handles multiple photos per item and creates organized inventory entries.
"""

import os
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image
import re

class MultiPhotoAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.staging_path = self.project_path / "photos" / "staging"
        self.category_path = self.project_path / "photos" / "by_category"
        self.inventory_path = self.project_path / "data" / "inventory_tracker.csv"
        self.hashtag_path = self.project_path / "data" / "hashtag_bank.csv"
        
        # Create staging folder if it doesn't exist
        self.staging_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing inventory to get next ID
        self.next_item_id = self._get_next_item_id()
        
        # Load hashtag bank for recommendations
        self.hashtag_bank = self._load_hashtag_bank()

    def _get_next_item_id(self):
        """Get the next available item ID by checking existing inventory."""
        if not self.inventory_path.exists():
            return 1
        
        max_id = 0
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
        except Exception as e:
            print(f"Error reading inventory: {e}")
        
        return max_id + 1

    def _load_hashtag_bank(self):
        """Load hashtag bank for recommendations."""
        hashtags = {}
        if self.hashtag_path.exists():
            try:
                with open(self.hashtag_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        hashtags[row['Category'].lower()] = {
                            'primary': row['Primary_Hashtags'].split(' '),
                            'style': row['Style_Hashtags'].split(' '),
                            'trending': row['Trending_Hashtags'].split(' ')
                        }
            except Exception as e:
                print(f"Error loading hashtag bank: {e}")
        return hashtags

    def get_all_photos(self):
        """Get all image files in staging folder."""
        image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.HEIC'}
        image_files = [f for f in self.staging_path.iterdir() 
                      if f.is_file() and f.suffix.lower() in image_extensions]
        return sorted(image_files)  # Sort for consistent ordering

    def display_photo_info(self, photo_path, index):
        """Display basic info about a photo."""
        try:
            with Image.open(photo_path) as img:
                width, height = img.size
                file_size = photo_path.stat().st_size / 1024 / 1024  # MB
            
            print(f"[{index}] {photo_path.name}")
            print(f"    Size: {width}x{height}, {file_size:.1f}MB")
            print(f"    Modified: {datetime.fromtimestamp(photo_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}")
            
        except Exception as e:
            print(f"[{index}] {photo_path.name} - Error reading: {e}")

    def score_photo_quality(self, photo_path):
        """Basic photo quality scoring."""
        try:
            with Image.open(photo_path) as img:
                width, height = img.size
                
                score = 0
                
                # Resolution score (max 30 points)
                total_pixels = width * height
                if total_pixels >= 1280 * 1280:
                    score += 30
                elif total_pixels >= 800 * 800:
                    score += 20
                else:
                    score += 10
                
                # Aspect ratio score (max 20 points) - prefer square
                ratio = min(width, height) / max(width, height)
                if ratio >= 0.95:  # Nearly square
                    score += 20
                elif ratio >= 0.8:
                    score += 15
                else:
                    score += 10
                
                # File size score (max 20 points) - prefer reasonable size
                file_size = photo_path.stat().st_size / 1024 / 1024  # MB
                if 1 <= file_size <= 8:  # Good size range
                    score += 20
                elif file_size <= 15:  # Still acceptable
                    score += 15
                else:
                    score += 10
                
                # File name hints (max 30 points) - prefer descriptive names
                filename_lower = photo_path.name.lower()
                if any(word in filename_lower for word in ['front', 'main', '01', '_1']):
                    score += 30
                elif any(word in filename_lower for word in ['detail', 'close', 'tag', 'label']):
                    score += 25
                elif any(word in filename_lower for word in ['back', 'rear', '02', '_2']):
                    score += 20
                else:
                    score += 15
                
                return min(score, 100)  # Cap at 100
                
        except Exception as e:
            return 0

    def group_photos_interactively(self):
        """Interactive photo grouping interface."""
        photos = self.get_all_photos()
        if not photos:
            print("No photos found in staging folder!")
            return []
        
        print(f"\n{'='*80}")
        print(f"📸 PHOTO GROUPING - Found {len(photos)} photos")
        print(f"{'='*80}")
        print("You'll group photos that belong to the same item.")
        print("Multiple photos of the same clothing item should be grouped together.\n")
        
        grouped_items = []
        remaining_photos = list(photos)
        current_group = []
        
        while remaining_photos:
            print(f"\n{'='*60}")
            print(f"📋 PHOTOS REMAINING: {len(remaining_photos)}")
            print(f"{'='*60}")
            
            # Show first 10 remaining photos
            display_count = min(10, len(remaining_photos))
            for i in range(display_count):
                self.display_photo_info(remaining_photos[i], i + 1)
            
            if len(remaining_photos) > 10:
                print(f"... and {len(remaining_photos) - 10} more photos")
            
            print(f"\n📁 CURRENT GROUP: {len(current_group)} photos")
            for i, photo in enumerate(current_group):
                print(f"  [{i+1}] {photo.name}")
            
            print(f"\nOPTIONS:")
            print(f"  1-{display_count}: Add photo to current group")
            print(f"  'done': Finish current group and save item")
            print(f"  'skip': Skip current photo")
            print(f"  'restart': Start current group over")
            print(f"  'quit': Exit grouping")
            
            choice = input(f"\nWhat would you like to do? ").strip().lower()
            
            if choice == 'quit':
                print("Grouping cancelled.")
                return []
            
            elif choice == 'done':
                if current_group:
                    # Process current group
                    print(f"\n✅ GROUP COMPLETE: {len(current_group)} photos")
                    item_data = self.process_photo_group(current_group)
                    if item_data:
                        grouped_items.append(item_data)
                    current_group = []
                else:
                    print("❌ No photos in current group!")
            
            elif choice == 'restart':
                # Put current group photos back in remaining
                remaining_photos.extend(current_group)
                remaining_photos.sort()
                current_group = []
                print("🔄 Current group cleared.")
            
            elif choice == 'skip':
                if remaining_photos:
                    skipped = remaining_photos.pop(0)
                    print(f"⏭️ Skipped: {skipped.name}")
            
            elif choice.isdigit():
                photo_num = int(choice)
                if 1 <= photo_num <= min(display_count, len(remaining_photos)):
                    selected_photo = remaining_photos.pop(photo_num - 1)
                    current_group.append(selected_photo)
                    print(f"➕ Added to group: {selected_photo.name}")
                else:
                    print("❌ Invalid photo number!")
            
            else:
                print("❌ Invalid option!")
        
        # Handle any remaining group
        if current_group:
            print(f"\n✅ FINAL GROUP: {len(current_group)} photos")
            item_data = self.process_photo_group(current_group)
            if item_data:
                grouped_items.append(item_data)
        
        return grouped_items

    def process_photo_group(self, photo_group):
        """Process a group of photos for a single item."""
        print(f"\n{'='*60}")
        print(f"📸 PROCESSING ITEM GROUP ({len(photo_group)} photos)")
        print(f"{'='*60}")
        
        # Show photos with quality scores
        photo_scores = []
        for i, photo in enumerate(photo_group):
            score = self.score_photo_quality(photo)
            photo_scores.append((photo, score))
            print(f"[{i+1}] {photo.name} - Quality Score: {score}/100")
        
        # Sort by quality score (best first)
        photo_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Recommend best 4 photos
        recommended = photo_scores[:4]
        print(f"\n⭐ RECOMMENDED BEST 4 PHOTOS:")
        for i, (photo, score) in enumerate(recommended):
            print(f"  [{i+1}] {photo.name} (Score: {score})")
        
        # Get user input for item details
        print(f"\n📝 ITEM DETAILS:")
        confirmed = {}
        confirmed['brand'] = input(f"Brand: ").strip()
        confirmed['category'] = input(f"Category (tops/dresses/bottoms/outerwear/shoes/accessories): ").strip().lower()
        confirmed['item_type'] = input(f"Item Type (blazer/dress/jeans/etc.): ").strip()
        confirmed['size'] = input(f"Size: ").strip()
        confirmed['color'] = input(f"Primary Color: ").strip()
        confirmed['condition'] = input(f"Condition (Excellent/Very Good/Good/Fair): ").strip()
        confirmed['purchase_price'] = input(f"Purchase Price (£): ").strip()
        confirmed['target_price'] = input(f"Target Sale Price (£): ").strip()
        confirmed['material'] = input(f"Material (if known): ").strip()
        confirmed['notes'] = input(f"Any notes: ").strip()
        
        # Confirm photo selection
        print(f"\n📸 PHOTO SELECTION:")
        print("Use recommended photos? (y/n) [y]: ", end="")
        use_recommended = input().strip().lower()
        
        if use_recommended in ['n', 'no']:
            # Let user select photos manually
            selected_photos = []
            print("Select up to 4 photos (enter numbers separated by spaces):")
            for i, photo in enumerate(photo_group):
                print(f"  [{i+1}] {photo.name}")
            
            selection = input("Photo numbers: ").strip().split()
            try:
                for num in selection[:4]:  # Max 4 photos
                    idx = int(num) - 1
                    if 0 <= idx < len(photo_group):
                        selected_photos.append(photo_group[idx])
            except ValueError:
                print("Invalid selection, using recommended photos.")
                selected_photos = [photo for photo, score in recommended]
        else:
            selected_photos = [photo for photo, score in recommended]
        
        # Final confirmation
        print(f"\n✅ FINAL ITEM SUMMARY:")
        print(f"  Item: {confirmed['brand']} {confirmed['item_type']}")
        print(f"  Category: {confirmed['category']}")
        print(f"  Photos: {len(selected_photos)} selected")
        for i, photo in enumerate(selected_photos):
            print(f"    [{i+1}] {photo.name}")
        
        confirm = input(f"\nSave this item? (y/n) [y]: ").strip().lower()
        if confirm in ['n', 'no']:
            print("❌ Item cancelled.")
            return None
        
        # Process the item
        item_id = f"DP{self.next_item_id:03d}"
        self.next_item_id += 1
        
        # Move and rename photos
        photo_filenames = []
        base_name = self.generate_filename(confirmed)
        
        for i, photo in enumerate(selected_photos):
            new_filename = self.move_and_rename_photo(photo, confirmed, i + 1, base_name)
            photo_filenames.append(new_filename)
        
        # Add to inventory
        self.add_to_inventory(confirmed, photo_filenames, item_id)
        
        print(f"✅ SUCCESS! Created item {item_id} with {len(photo_filenames)} photos")
        
        return {
            'item_id': item_id,
            'details': confirmed,
            'photos': photo_filenames
        }

    def generate_filename(self, confirmed_details):
        """Generate base filename using naming convention."""
        brand = re.sub(r'[^a-zA-Z0-9]', '', confirmed_details['brand'].lower())
        color = re.sub(r'[^a-zA-Z0-9]', '', confirmed_details['color'].lower())
        item_type = re.sub(r'[^a-zA-Z0-9]', '', confirmed_details['item_type'].lower())
        
        if not brand:
            brand = "item"
        if not color:
            color = "unknown"
        if not item_type:
            item_type = "clothing"
            
        return f"{brand}_{color}_{item_type}"

    def move_and_rename_photo(self, original_path, confirmed_details, photo_number, base_name):
        """Move photo to appropriate category folder with new name."""
        category = confirmed_details['category'].lower()
        category_folder = self.category_path / category
        
        # Create category folder if it doesn't exist
        category_folder.mkdir(parents=True, exist_ok=True)
        
        # Generate new filename
        file_extension = original_path.suffix.lower()
        new_filename = f"{base_name}_{photo_number}{file_extension}"
        
        new_path = category_folder / new_filename
        
        # Handle duplicate filenames
        counter = 1
        while new_path.exists():
            new_filename = f"{base_name}_{photo_number}_{counter}{file_extension}"
            new_path = category_folder / new_filename
            counter += 1
        
        # Move file
        shutil.move(str(original_path), str(new_path))
        return new_filename

    def suggest_hashtags(self, confirmed_details):
        """Suggest hashtags based on item details."""
        category = confirmed_details['category'].lower()
        hashtags = []
        
        if category in self.hashtag_bank:
            # Get relevant hashtags from bank
            bank_tags = self.hashtag_bank[category]
            hashtags.extend(bank_tags['primary'][:2])  # 2 primary tags
            hashtags.extend(bank_tags['style'][:2])    # 2 style tags
            hashtags.extend(bank_tags['trending'][:1]) # 1 trending tag
        else:
            # Generic hashtags if category not found
            hashtags = [f"#{confirmed_details['item_type']}", 
                       f"#{confirmed_details['color']}", 
                       f"#{confirmed_details['brand'].lower()}", 
                       "#preloved", "#sustainable"]
        
        return ' '.join(hashtags[:5])  # Max 5 hashtags

    def add_to_inventory(self, confirmed_details, photo_filenames, item_id):
        """Add new item to inventory CSV with multiple photos."""
        
        # Prepare row data
        row_data = {
            'Item_ID': item_id,
            'Brand': confirmed_details['brand'],
            'Category': confirmed_details['category'].title(),
            'Item_Type': confirmed_details['item_type'].title(),
            'Size': confirmed_details['size'],
            'Color': confirmed_details['color'].title(),
            'Condition': confirmed_details['condition'],
            'Purchase_Price': confirmed_details.get('purchase_price', ''),
            'Target_Price': confirmed_details.get('target_price', ''),
            'Actual_Sale_Price': '',
            'Photo_1': photo_filenames[0] if len(photo_filenames) > 0 else '',
            'Photo_2': photo_filenames[1] if len(photo_filenames) > 1 else '',
            'Photo_3': photo_filenames[2] if len(photo_filenames) > 2 else '',
            'Photo_4': photo_filenames[3] if len(photo_filenames) > 3 else '',
            'Title': '',  # Will be generated when creating listing
            'Description': '',  # Will be generated when creating listing
            'Hashtags': self.suggest_hashtags(confirmed_details),
            'Status': 'Not Listed',
            'Date_Added': datetime.now().strftime('%Y-%m-%d'),
            'Date_Listed': '',
            'Date_Sold': '',
            'Likes': '0',
            'Views': '0',
            'Notes': confirmed_details.get('notes', '')
        }
        
        # Check if CSV exists and has headers
        file_exists = self.inventory_path.exists()
        
        # Write to CSV
        with open(self.inventory_path, 'a', newline='', encoding='utf-8') as file:
            fieldnames = list(row_data.keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write headers if file is new
            if not file_exists or os.path.getsize(self.inventory_path) == 0:
                writer.writeheader()
            
            writer.writerow(row_data)

def main():
    # Set up the analyzer
    project_path = "/Users/emilywebster/Dev/Depop_Selling"
    analyzer = MultiPhotoAnalyzer(project_path)
    
    print("📸 Depop Multi-Photo Analyzer")
    print("============================")
    print("Group multiple photos of the same item together!")
    print(f"Project: {project_path}")
    print(f"Staging folder: {analyzer.staging_path}")
    print(f"Next Item ID: DP{analyzer.next_item_id:03d}")
    
    # Check if staging folder has photos
    photos = analyzer.get_all_photos()
    
    if not photos:
        print(f"\nNo photos found in {analyzer.staging_path}")
        print("Please add photos to the staging folder and run again.")
        return
    
    print(f"\nFound {len(photos)} photos to process.")
    print("You'll be able to group photos that show the same item.")
    
    # Confirm before starting
    start = input("\nStart photo grouping? (y/n) [y]: ").strip().lower()
    if start in ['n', 'no']:
        print("Cancelled.")
        return
    
    # Group photos interactively
    grouped_items = analyzer.group_photos_interactively()
    
    # Summary
    print(f"\n{'='*80}")
    print(f"🎉 PROCESSING COMPLETE!")
    print(f"{'='*80}")
    print(f"Items created: {len(grouped_items)}")
    
    for item in grouped_items:
        details = item['details']
        print(f"\n✅ {item['item_id']}: {details['brand']} {details['item_type']}")
        print(f"   Photos: {len(item['photos'])}")
        for i, photo in enumerate(item['photos']):
            print(f"     [{i+1}] {photo}")
    
    if grouped_items:
        print(f"\n🚀 All items added to inventory tracker!")
        print(f"📁 Photos organized in category folders.")
        print(f"📝 Ready to create listings using templates!")
        print(f"\nNext steps:")
        print(f"1. Open data/inventory_tracker.csv to see your items")
        print(f"2. Use docs/listing_templates.md to create descriptions")
        print(f"3. Upload organized photos from photos/by_category/ folders")

if __name__ == "__main__":
    main()