# Photo Assessment Workflow Guide

## 🎯 Overview: Drop Photos → Get AI Analysis → Organized Inventory

This system analyzes your photos and helps populate your inventory with minimal manual work.

---

## 📋 Quick Start

### 1. Setup (One Time Only)
```bash
# Install required Python packages
pip install pillow requests openai anthropic

# Make the script executable
chmod +x photo_analyzer.py
```

### 2. Basic Workflow
1. **Drop photos** into `photos/staging/` folder
2. **Run the analyzer**: `python3 photo_analyzer.py`
3. **Confirm/edit** AI suggestions for each photo
4. **Photos automatically organized** and **inventory updated**

---

## 🚀 Step-by-Step Workflow

### Step 1: Add Photos to Staging
- Copy/move your photos to `Depop_Selling/photos/staging/`
- Supported formats: JPG, JPEG, PNG, HEIC
- No need to rename - the script handles this

### Step 2: Run the Analyzer
```bash
cd /Users/emilywebster/Dev/Depop_Selling
python3 photo_analyzer.py
```

### Step 3: Interactive Analysis
For each photo, the script will:
1. **Show AI analysis** with best guesses
2. **Ask for confirmation** on each detail
3. **Let you edit** any incorrect information
4. **Ask if you want to process** the item

### Step 4: Automatic Processing
The script will:
- **Move photo** to correct category folder (`photos/by_category/`)
- **Rename file** using convention: `brand_color_itemtype_1.jpg`
- **Add entry** to `inventory_tracker.csv`
- **Generate hashtags** based on item details

---

## 🔍 What the AI Analyzes

### Current Analysis (Manual Confirmation)
- **Item Type**: dress, top, jeans, shoes, jacket, etc.
- **Category**: maps to folder structure
- **Brand**: asks you to confirm/identify
- **Color**: primary color identification
- **Size**: you input based on tags
- **Condition**: you assess condition
- **Style**: casual, formal, vintage, etc.

### Future AI Enhancement Options
When you add AI vision integration:
- **Automatic brand detection** from logos/tags
- **Size tag reading** from photos
- **Condition assessment** from visual wear
- **Material identification** from fabric appearance
- **Quality scoring** for listing suitability

---

## 📊 Example Session

```
Depop Photo Analyzer
===================
Project: /Users/emilywebster/Dev/Depop_Selling
Staging folder: photos/staging
Next Item ID: DP004

Found 3 photos to process.
Start processing photos? (y/n) [y]: y

============================================================
Analyzing: IMG_2847.jpg
============================================================
AI Assessment:
  Item Type: Unknown
  Category: Unknown
  Brand: Unknown
  Color: Unknown
  Size: Unknown
  Condition: Good
  Style: Unknown
  Suggested Price: £15-35
  Image Quality: Good

Please confirm or edit the details:
Brand [Unknown]: Zara
Category (tops/dresses/bottoms/outerwear/shoes/accessories) [Unknown]: tops
Item Type (blazer/dress/jeans/etc.) [Unknown]: blazer
Size [Unknown]: M
Color [Unknown]: black
Condition (Excellent/Very Good/Good/Fair) [Good]: Excellent
Purchase Price (£): 25
Target Sale Price (£): 45
Material [Unknown]: polyester blend
Any notes: Professional blazer, great condition

Process this item? (y/n) [y]: y
✅ Successfully processed DP004: Zara blazer -> zara_black_blazer_1.jpg
```

---

## 📁 File Organization Results

### Before Processing
```
photos/staging/
├── IMG_2847.jpg
├── IMG_2848.jpg
└── IMG_2849.jpg
```

### After Processing
```
photos/by_category/
├── tops/
│   └── zara_black_blazer_1.jpg
├── dresses/
│   └── vintage_floral_dress_1.jpg
└── shoes/
    └── nike_white_sneakers_1.jpg
```

### Inventory Updated
New entries added to `inventory_tracker.csv` with:
- Auto-generated Item IDs (DP004, DP005, DP006)
- All confirmed details
- Photo filenames linked
- Suggested hashtags
- Date added
- Status: "Not Listed"

---

## 🛠️ Customization Options

### Modify Analysis Prompts
Edit the `analyze_photo_with_ai()` function to:
- Change what the AI looks for
- Add new categories or attributes
- Modify confidence scoring
- Customize pricing suggestions

### Add AI Vision Integration
To connect real AI vision:
1. **OpenAI GPT-4 Vision**: Add API key and vision calls
2. **Claude Computer Use**: Add Anthropic API integration  
3. **Google Vision API**: Add Google Cloud vision
4. **Local AI Models**: Use open-source vision models

### Custom Categories
Modify `hashtag_bank.csv` to add new categories:
- Athletic wear
- Vintage decades (60s, 70s, 80s, 90s)
- Designer subcategories
- Seasonal collections

---

## 💡 Pro Tips

### Photo Quality Tips
- **Well-lit photos** get better AI analysis
- **Clear brand tags** improve brand detection
- **Flat lay or hung** items analyze better than crumpled
- **Multiple angles** provide more data points

### Workflow Efficiency
- **Process in batches** - 5-10 photos at once
- **Consistent lighting** helps AI learn your style
- **Standardize backgrounds** for professional look
- **Group similar items** for faster processing

### Data Quality
- **Be consistent** with brand names (e.g., always "Zara", not "ZARA")
- **Use standard conditions** (Excellent/Very Good/Good/Fair)
- **Check category spelling** (matches folder names exactly)
- **Add meaningful notes** for unique features

---

## 🔧 Troubleshooting

### Common Issues

**Script won't run**
```bash
# Check Python installation
python3 --version

# Install missing packages
pip install pillow
```

**No photos found**
- Check photos are in `photos/staging/` folder
- Verify file extensions (JPG, PNG, etc.)
- Make sure files aren't hidden

**CSV not updating**
- Check file permissions on `inventory_tracker.csv`
- Ensure folder structure exists
- Verify CSV isn't open in Excel/Sheets

**Photos not moving**
- Check category folder structure exists
- Verify permissions on photo folders
- Make sure category names match exactly

### Error Messages
- **"Permission denied"**: Check file/folder permissions
- **"Module not found"**: Install required packages
- **"Invalid category"**: Use exact category names from folder structure

---

## 🚀 Advanced Usage

### Batch Processing Multiple Sessions
```bash
# Process morning photos
python3 photo_analyzer.py

# Add more photos later
# Process afternoon batch
python3 photo_analyzer.py
```

### Integration with Listing Creation
After photo analysis:
1. **Open inventory_tracker.csv**
2. **Use listing templates** to create descriptions
3. **Copy hashtags** generated by analyzer
4. **Upload organized photos** from category folders

### Performance Tracking
The script tracks:
- **Processing date** for each item
- **Generated hashtags** for consistency
- **File organization** for easy retrieval
- **Next available IDs** for smooth workflow

---

## 🎯 Next Steps After Analysis

### Ready to List Items
1. **Open inventory tracker** to see new items
2. **Review suggested hashtags** and pricing
3. **Use listing templates** to create descriptions
4. **Upload photos** from organized category folders
5. **Follow listing workflow** for publishing

### Ongoing Optimization
- **Track which items sell fastest** 
- **Adjust AI analysis** based on results
- **Update hashtag suggestions** for trends
- **Refine pricing models** based on sales data

---

## 🤝 Getting Help

### AI Assistance Available
- **Description writing** using your analysis data
- **Hashtag optimization** based on performance
- **Pricing research** for specific items
- **Listing creation** using templates
- **Performance analysis** of sold items

### Manual Backup
If the script has issues:
1. **Manually analyze photos** using the checklist
2. **Add items to CSV** following the format
3. **Organize photos** using naming convention
4. **Continue with normal workflow**

**Remember**: This system saves time and ensures consistency, but you always have full control over the final details!