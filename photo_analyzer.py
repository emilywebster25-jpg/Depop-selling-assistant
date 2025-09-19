#!/usr/bin/env python3
"""
Depop Photo Analyzer
Analyzes photos in the staging folder and helps populate inventory with AI assessments.
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

# You'll need to install: pip install pillow requests openai anthropic
# Choose one of these AI services (comment out the ones you don't want to use)

class PhotoAnalyzer:
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

    def analyze_photo_with_ai(self, image_path):
        """
        Analyze a photo using AI vision.
        This is a template - you'll need to implement with your preferred AI service.
        """
        # This is where you'd call Claude, GPT-4 Vision, or another AI service
        # For now, we'll return a template structure that you can fill in manually
        
        try:
            # Load and analyze image
            with Image.open(image_path) as img:
                width, height = img.size
                
            # Basic analysis we can do without AI
            filename = Path(image_path).name
            
            # Template analysis - replace with actual AI call
            analysis = {
                "item_type": "Unknown",  # AI would determine: dress, top, jeans, etc.
                "category": "Unknown",   # maps to folder structure
                "brand": "Unknown",      # AI would read tags/logos
                "color": "Unknown",      # AI would identify primary color
                "size": "Unknown",       # AI would read size tags
                "condition": "Good",     # AI would assess wear/condition
                "material": "Unknown",   # AI might identify fabric
                "style": "Unknown",      # casual, formal, vintage, etc.
                "unique_features": [],   # special details AI notices
                "suggested_price_range": "15-35",  # based on brand/type
                "confidence": 0.7,       # how confident AI is
                "image_quality": "Good", # suitable for listing?
                "filename": filename,
                "dimensions": f"{width}x{height}"
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing {image_path}: {e}")
            return None

    def get_user_confirmation(self, analysis, image_path):
        """Interactive process to confirm/edit AI analysis."""
        print(f"\n{'='*60}")
        print(f"Analyzing: {Path(image_path).name}")
        print(f"{'='*60}")
        
        # Show AI analysis
        print(f"AI Assessment:")
        print(f"  Item Type: {analysis['item_type']}")
        print(f"  Category: {analysis['category']}")
        print(f"  Brand: {analysis['brand']}")
        print(f"  Color: {analysis['color']}")
        print(f"  Size: {analysis['size']}")
        print(f"  Condition: {analysis['condition']}")
        print(f"  Style: {analysis['style']}")
        print(f"  Suggested Price: £{analysis['suggested_price_range']}")
        print(f"  Image Quality: {analysis['image_quality']}")
        
        # Get user input
        print(f"\nPlease confirm or edit the details:")
        
        confirmed = {}
        confirmed['brand'] = input(f"Brand [{analysis['brand']}]: ").strip() or analysis['brand']
        confirmed['category'] = input(f"Category (tops/dresses/bottoms/outerwear/shoes/accessories) [{analysis['category']}]: ").strip() or analysis['category']
        confirmed['item_type'] = input(f"Item Type (blazer/dress/jeans/etc.) [{analysis['item_type']}]: ").strip() or analysis['item_type']
        confirmed['size'] = input(f"Size [{analysis['size']}]: ").strip() or analysis['size']
        confirmed['color'] = input(f"Color [{analysis['color']}]: ").strip() or analysis['color']
        confirmed['condition'] = input(f"Condition (Excellent/Very Good/Good/Fair) [{analysis['condition']}]: ").strip() or analysis['condition']
        confirmed['purchase_price'] = input(f"Purchase Price (£): ").strip()
        confirmed['target_price'] = input(f"Target Sale Price (£): ").strip()
        confirmed['material'] = input(f"Material [{analysis['material']}]: ").strip() or analysis['material']
        confirmed['notes'] = input(f"Any notes: ").strip()
        
        return confirmed

    def generate_filename(self, confirmed_details):
        """Generate filename using naming convention: brand_color_itemtype_number.jpg"""
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

    def move_and_rename_photo(self, original_path, confirmed_details, photo_number=1):
        """Move photo to appropriate category folder with new name."""
        category = confirmed_details['category'].lower()
        category_folder = self.category_path / category
        
        # Create category folder if it doesn't exist
        category_folder.mkdir(parents=True, exist_ok=True)
        
        # Generate new filename
        base_name = self.generate_filename(confirmed_details)
        file_extension = Path(original_path).suffix.lower()
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

    def add_to_inventory(self, confirmed_details, photo_filename):
        """Add new item to inventory CSV."""
        item_id = f"DP{self.next_item_id:03d}"
        
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
            'Photo_1': photo_filename,
            'Photo_2': '',
            'Photo_3': '',
            'Photo_4': '',
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
        
        self.next_item_id += 1
        return item_id

    def process_staging_photos(self):
        """Main function to process all photos in staging folder."""
        # Get all image files in staging
        image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.HEIC'}
        image_files = [f for f in self.staging_path.iterdir() 
                      if f.is_file() and f.suffix.lower() in image_extensions]
        
        if not image_files:
            print("No photos found in staging folder!")
            return
        
        print(f"Found {len(image_files)} photos to analyze...")
        
        processed_items = []
        
        for image_path in image_files:
            try:
                print(f"\nProcessing: {image_path.name}")
                
                # Analyze photo with AI
                analysis = self.analyze_photo_with_ai(image_path)
                if not analysis:
                    print(f"Failed to analyze {image_path.name}, skipping...")
                    continue
                
                # Get user confirmation/corrections
                confirmed_details = self.get_user_confirmation(analysis, image_path)
                
                # Ask if user wants to process this item
                process = input(f"\nProcess this item? (y/n) [y]: ").strip().lower()
                if process in ['n', 'no']:
                    print("Skipping this item...")
                    continue
                
                # Move and rename photo
                new_filename = self.move_and_rename_photo(image_path, confirmed_details)
                
                # Add to inventory
                item_id = self.add_to_inventory(confirmed_details, new_filename)
                
                processed_items.append({
                    'item_id': item_id,
                    'filename': new_filename,
                    'brand': confirmed_details['brand'],
                    'item_type': confirmed_details['item_type']
                })
                
                print(f"✅ Successfully processed {item_id}: {confirmed_details['brand']} {confirmed_details['item_type']}")
                
            except KeyboardInterrupt:
                print("\nProcessing interrupted by user.")
                break
            except Exception as e:
                print(f"Error processing {image_path.name}: {e}")
                continue
        
        # Summary
        print(f"\n{'='*60}")
        print(f"PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"Items processed: {len(processed_items)}")
        for item in processed_items:
            print(f"  {item['item_id']}: {item['brand']} {item['item_type']} -> {item['filename']}")
        print(f"\nAll items added to inventory tracker!")
        print(f"Photos organized in category folders.")
        print(f"Ready to create listings using the templates!")

def main():
    # Set up the analyzer
    project_path = "/Users/emilywebster/Dev/Depop_Selling"
    analyzer = PhotoAnalyzer(project_path)
    
    print("Depop Photo Analyzer")
    print("===================")
    print(f"Project: {project_path}")
    print(f"Staging folder: {analyzer.staging_path}")
    print(f"Next Item ID: DP{analyzer.next_item_id:03d}")
    
    # Check if staging folder has photos
    image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.HEIC'}
    image_files = [f for f in analyzer.staging_path.iterdir() 
                  if f.is_file() and f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"\nNo photos found in {analyzer.staging_path}")
        print("Please add photos to the staging folder and run again.")
        return
    
    print(f"\nFound {len(image_files)} photos to process.")
    
    # Confirm before starting
    start = input("\nStart processing photos? (y/n) [y]: ").strip().lower()
    if start in ['n', 'no']:
        print("Cancelled.")
        return
    
    # Process photos
    analyzer.process_staging_photos()

if __name__ == "__main__":
    main()