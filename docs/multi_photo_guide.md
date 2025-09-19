# Multi-Photo Grouping Guide

## 🎯 Perfect for Your Situation!

You have **154 photos** with multiple angles and detail shots of the same items - this enhanced system handles that perfectly.

---

## 🚀 How to Use the Enhanced System

### Run the Enhanced Analyzer
```bash
cd /Users/emilywebster/Dev/Depop_Selling
python3 photo_grouper.py
```

### Interactive Grouping Process

#### 1. **Photo Display**
- Shows you **10 photos at a time** with details:
  - Filename, dimensions, file size
  - Date modified (helps identify related photos)
  - Quality score (helps pick the best ones)

#### 2. **Grouping Interface**
```
OPTIONS:
  1-10: Add photo to current group
  'done': Finish current group and save item
  'skip': Skip current photo
  'restart': Start current group over  
  'quit': Exit grouping
```

#### 3. **Smart Photo Selection**
- **Quality scoring**: Ranks photos by resolution, aspect ratio, file size
- **Automatic recommendations**: Suggests best 4 photos per item
- **Manual override**: You can choose different photos if you prefer

#### 4. **Item Details Input**
For each group, you'll enter:
- Brand, category, item type
- Size, color, condition
- Purchase price, target price
- Material, notes

#### 5. **Automatic Processing**
- **Photos renamed**: `brand_color_itemtype_1.jpg` through `_4.jpg`
- **Organized by category**: Moved to correct folders
- **Inventory updated**: Single entry per item with all 4 photos
- **Hashtags generated**: Based on category and trends

---

## 💡 Tips for Efficient Grouping

### Identify Related Photos
Look for photos taken at similar times (check date modified) or with similar backgrounds/lighting.

### Typical Photo Groups
- **Front view** (main listing photo)
- **Back view** (show full garment)
- **Detail shot** (fabric, buttons, tags)
- **Styling shot** (how to wear it)

### Quality Selection
The system will suggest the best photos based on:
- **Resolution** (higher is better)
- **Square aspect ratio** (required for Depop)
- **File size** (not too large, not too small)
- **Filename hints** (front, main, detail, etc.)

---

## 📊 Example Workflow

### You'll see something like:
```
======================================================
📋 PHOTOS REMAINING: 154
======================================================
[1] IMG_2847.jpg
    Size: 1920x1920, 2.3MB
    Modified: 2025-09-14 10:30
[2] IMG_2848.jpg  
    Size: 1920x1920, 2.1MB
    Modified: 2025-09-14 10:31
[3] IMG_2849.jpg
    Size: 1920x1920, 2.4MB
    Modified: 2025-09-14 10:31
...

📁 CURRENT GROUP: 0 photos

What would you like to do? 
```

### Your workflow:
1. **Type "1"** to add IMG_2847.jpg to group
2. **Type "2"** to add IMG_2848.jpg to group  
3. **Type "3"** to add IMG_2849.jpg to group
4. **Type "done"** when you have 2-6 photos of the same item
5. **Enter item details** when prompted
6. **Confirm photo selection** (or choose different ones)
7. **Repeat** for next item

---

## 🎯 Expected Results

### For 154 Photos
- **Estimated items**: 25-40 individual clothing pieces
- **Time investment**: 2-4 hours total (depends on how organized your photos are)
- **Output**: Professional inventory with organized photos ready for listing

### What You'll Get
```
✅ DP004: Zara Black Blazer
   Photos: 4
     [1] zara_black_blazer_1.jpg
     [2] zara_black_blazer_2.jpg  
     [3] zara_black_blazer_3.jpg
     [4] zara_black_blazer_4.jpg

✅ DP005: Vintage Floral Dress
   Photos: 3
     [1] vintage_floral_dress_1.jpg
     [2] vintage_floral_dress_2.jpg
     [3] vintage_floral_dress_3.jpg
```

### Ready for Depop
- **Inventory tracker updated** with all items
- **Photos organized** in category folders
- **Hashtags generated** for each item
- **Ready to create listings** using templates

---

## ⚡ Pro Tips

### Speed Up the Process
- **Group chronologically**: Photos taken at the same time are likely the same item
- **Look for backgrounds**: Same background/lighting = probably same item
- **Use quality scores**: Let the system recommend the best photos
- **Don't overthink**: 3-4 good photos per item is perfect

### Handle Difficult Cases
- **Similar items**: If you have multiple black tops, be extra careful with grouping
- **Mixed lighting**: Photos with different lighting might still be the same item
- **Unclear photos**: Use the 'skip' option for photos that are too blurry/dark

### Batch Strategy
- **Process 20-30 items at a time**: Take breaks to stay focused
- **Save frequently**: The system saves each completed group immediately
- **Review after**: Check your inventory_tracker.csv to see results

---

## 🚀 Ready to Start?

**Your command:**
```bash
python3 photo_grouper.py
```

**Expected time:** 2-4 hours for 154 photos
**Expected output:** 25-40 professionally organized items ready for Depop

This will transform your pile of photos into a systematic, sellable inventory! 📸✨