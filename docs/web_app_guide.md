# 🌐 Web Photo Organizer - User Guide

## 🚀 Quick Start

### Launch the App
```bash
cd /Users/emilywebster/Dev/Depop_Selling
./launch_organizer.sh
```

**Or start manually:**
```bash
python3 photo_server.py
```

**Access at:** http://localhost:8001

---

## ✨ Features

### ✅ **HEIC Photo Support**
- Automatically converts iPhone HEIC photos to web-friendly JPEGs
- Resizes images to 800px max for faster loading
- No broken images - everything displays properly

### ✅ **Chronological Sorting** 
- Photos sorted by filename (IMG_3058, IMG_3059, IMG_3060...)
- Makes it easy to spot consecutive photos of the same item
- Perfect for your 157 iPhone photos

### ✅ **Clean, Professional Interface**
- Minimal design with neutral colors
- Clean photo grid with hover effects
- Simple status bar and refresh button
- No unnecessary clutter or "hideous colors"

### ✅ **Photo Grouping Workflow**
- Click photos to select them (blue border appears)
- Group 2-6 photos of the same clothing item
- Fill in details: brand, category, size, color, price
- Auto-generates hashtags and organizing photos

---

## 📱 How to Use

### 1. **View Your Photos**
- All 157 photos load automatically in chronological order
- Each photo shows filename and file size
- Images are converted and resized for web viewing

### 2. **Select Photos for an Item**
- Click on photos to select them (blue border appears)
- Select 2-6 photos of the same clothing item
- Use the "Selected: X photos" indicator to track your selection

### 3. **Create Item Listing**
- Click "Group Selected Photos" when ready
- Fill in the item form:
  - Brand, Category, Item Type
  - Size, Color, Condition
  - Purchase Price, Target Price
  - Notes (optional)

### 4. **Automatic Processing**
- Photos are renamed and moved to category folders
- Item is added to inventory_tracker.csv
- Hashtags are generated automatically
- Ready for Depop listing!

---

## 🔧 Technical Details

### **Server Info**
- Port: 8001
- HEIC conversion: Automatic via pillow-heif
- Image processing: PIL with optimization
- File serving: Python HTTP server

### **Photo Processing**
- Original HEIC files remain in staging folder
- Web display: Converted to JPEG, max 800px
- Quality: 75% with optimization for fast loading
- Chunked transfer to prevent timeouts

### **File Organization**
```
photos/
├── staging/           # Your original 157 HEIC photos
└── by_category/       # Organized photos after processing
    ├── tops/
    ├── dresses/
    ├── bottoms/
    └── ...
```

---

## 🎯 Perfect for Your Situation

### **157 HEIC Photos**
- All photos load and display properly
- Chronological order makes grouping easy
- Fast conversion and loading

### **Multiple Angles per Item**
- Easy to spot consecutive photos of same item
- Select 2-6 related photos per clothing piece
- Professional photo organization

### **Depop Selling Ready**
- Generates proper hashtags
- Organizes photos by category
- Creates comprehensive inventory tracking
- Optimized for Gen Z selling platform

---

## 🚨 Troubleshooting

### **Photos Not Loading?**
- Check server is running: `ps aux | grep photo_server`
- Try refreshing the page
- Ensure you're using http://localhost:8001

### **HEIC Images Broken?**
- HEIC support is now installed (pillow-heif)
- Should show "✅ HEIC support loaded" on server start
- All 157 photos should display properly

### **Wrong Order?**
- Photos are sorted alphabetically by filename
- Should show IMG_3058, IMG_3059, IMG_3060... in order
- Restart server if sorting seems off

---

## 💡 Pro Tips

### **Efficient Workflow**
- Photos of same item are usually consecutive
- Look for similar backgrounds/lighting
- 3-4 photos per item is ideal for Depop

### **Best Photo Selection**
- Front view (main listing photo)
- Back view or detail shot
- Close-up of fabric/tags
- Styled/worn photo if available

### **Quality Selection**
- System will suggest best photos
- Higher resolution is better
- Square aspect ratio preferred for Depop

---

**🎉 Your photo organization system is ready! Visit http://localhost:8001 to start turning your 157 photos into professional Depop listings.**