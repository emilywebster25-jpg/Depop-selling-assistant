# Quick Reference Guide - Depop Selling System

## 🚀 Most Common Tasks

### 📸 Process New Photos
```bash
# 1. Drop photos in staging folder
# 2. Run analyzer
python3 photo_analyzer.py
# 3. Follow prompts to confirm details
# 4. Photos auto-organized, inventory updated
```

### 📝 Create a Listing  
```bash
# 1. Open inventory_tracker.csv
# 2. Find your item (photos already organized)
# 3. Use templates from docs/listing_templates.md
# 4. Copy hashtags from inventory spreadsheet
# 5. Upload photos from photos/by_category/[type]/
```

### ⏰ Daily Routine (25 minutes)
```bash
Morning (10 min):
- Check messages on Depop
- Send offers to likers
- Respond to any questions

Evening (15 min):  
- Refresh 10-15 listings
- Like/follow similar sellers
- Check performance in inventory tracker
```

---

## 📁 File Locations

### 📊 Data Files
- **Main inventory**: `data/inventory_tracker.csv`
- **Hashtag bank**: `data/hashtag_bank.csv`  
- **Pricing research**: `data/pricing_research.csv`

### 📸 Photos
- **Drop new photos**: `photos/staging/`
- **Organized photos**: `photos/by_category/[tops|dresses|bottoms|etc]/`

### 📝 Templates & Guides
- **Listing templates**: `docs/listing_templates.md`
- **Daily tasks**: `docs/daily_tasks.md`
- **Photo guide**: `docs/photo_assessment_guide.md`
- **Depop tips**: `docs/depop_guide.md`

---

## ⚡ Quick Commands

### Setup (One Time)
```bash
./setup.sh
```

### Process Photos
```bash
python3 photo_analyzer.py
```

### Check What's Ready to List
```bash
# Look for items with Status = "Not Listed" in inventory_tracker.csv
```

---

## 🎯 Key Numbers to Remember

### Depop Platform (2025)
- **No selling fees** (since July 2024)
- **Transaction fee**: 3.3% + $0.45
- **90% users under 26** (Gen Z focused)
- **40% higher sales** with video
- **Square photos required**: 1280x1280px

### Time Commitments
- **Photo processing**: 2-3 min per photo
- **Listing creation**: 10 min per item
- **Daily tasks**: 25 min total
- **Weekly review**: 30 min

---

## 🏷️ Quick Hashtag Reference

### Universal Tags
- `#depop #secondhand #preloved #sustainable #vintage`

### By Category
- **Tops**: `#top #shirt #blouse #workwear #casual`
- **Dresses**: `#dress #midi #party #formal #cottagecore`  
- **Bottoms**: `#jeans #trousers #y2k #highwaisted #vintage`
- **Shoes**: `#shoes #boots #sneakers #platform #chunky`

### Trending 2025
- `#y2k #cottagecore #darkacademia #streetwear #minimalist`

---

## 💰 Quick Pricing Guide

### Fast Fashion Brands
- **H&M/Forever21**: £5-15
- **Zara/COS**: £15-40
- **ASOS**: £10-25

### Premium/Designer  
- **& Other Stories**: £25-60
- **Vintage pieces**: £15-80
- **Designer items**: Research required

### Pricing Strategy
1. Check `pricing_research.csv`
2. Research similar listings
3. Price 20% higher than minimum acceptable
4. Leave room for offers

---

## ✅ Pre-Listing Checklist

### Photo Quality
- [ ] Square format (1:1 ratio)
- [ ] Good natural lighting
- [ ] Item fills frame
- [ ] All 4 photos ready (main, detail, styled, back)
- [ ] Brand/size tags visible

### Listing Details
- [ ] Compelling title with brand and keywords
- [ ] Complete description using templates
- [ ] All 5 hashtags selected
- [ ] Competitive pricing researched
- [ ] Measurements included

### File Organization
- [ ] Photos in correct category folder
- [ ] Files named with convention: brand_color_type_1.jpg
- [ ] Inventory tracker updated
- [ ] Status set to "Listed" after publishing

---

## 🚨 Quick Troubleshooting

### Photo Analyzer Issues
```bash
# Script won't run
python3 --version  # Check Python installed
pip3 install pillow  # Install missing packages

# No photos found
# Check photos are in photos/staging/ folder
# Verify file extensions (JPG, PNG, etc.)
```

### Inventory Tracker Problems
- **CSV won't open**: Make sure it's not already open in Excel/Google Sheets
- **Missing columns**: Use the example format, don't modify headers
- **Wrong category**: Use exact folder names (tops, dresses, bottoms, etc.)

### Depop Listing Issues
- **Photos wrong size**: Must be square 1:1 ratio
- **Description too long**: Keep under 1000 characters
- **Hashtags not working**: Use # symbol, no spaces in tags

---

## 📞 Getting Help

### Documentation
- **Complete overview**: `PROJECT_OVERVIEW.md`
- **Photo workflow**: `docs/photo_assessment_guide.md`  
- **Listing process**: `docs/listing_workflow.md`
- **Depop tips**: `docs/depop_guide.md`

### AI Assistance
Ask Claude Code to help with:
- Writing compelling descriptions
- Research pricing for specific items
- Generate hashtags for new trends  
- Analyze your sales performance
- Update templates seasonally

---

## 🎯 Success Metrics to Track

### Weekly Goals
- **New listings**: 5-10 items
- **Messages responded**: 100% within 24hrs
- **Listings refreshed**: All items at least once
- **Community engagement**: 50+ likes, 10+ follows

### Monthly Analysis
- **Profit margins**: Track actual vs target prices
- **Best performers**: Which categories sell fastest
- **Photo performance**: Which styles get most likes
- **Price optimization**: Adjust based on market response

**Remember**: Consistency beats perfection. Small daily actions compound into big results! 🌟