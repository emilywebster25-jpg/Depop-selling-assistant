# 🛍️ Depop Selling Assistant

**A comprehensive web-based system to streamline your Depop selling process** - Built with Claude Code to demonstrate AI-human collaboration in creating practical business tools.

## 📋 What It Is

This is a complete **visual photo organizer and inventory management system** specifically designed for Depop sellers. It transforms the tedious process of organizing photos and creating listings into a streamlined, efficient workflow.

**Key Components:**
- 🌐 **Web-based photo organizer** with visual interface
- 📊 **Inventory tracking system** with CSV integration  
- 📸 **Photo organization** by category and item
- 🏷️ **Listing templates and hashtags** for optimization
- 🔗 **Direct Depop integration** for seamless uploading

## ⚙️ How It Works

### Visual Photo Organization
1. **Drop photos** into the staging folder
2. **Launch the web interface** (`./launch_organizer.sh`)
3. **Select which photos go together** for each item
4. **Fill out the form** (categories, brands, descriptions)
5. **Submit** - photos get copied to organized folders and details saved to CSV
6. **Use CSV data** to quickly fill out Depop listing details
7. **Click "Open Folder"** to drag photos directly into Depop

### What It Actually Does
- **Photo preview** - Click photos to see them larger
- **File organization** - Copies photos to organized folders when you submit the form
- **CSV tracking** - Saves your item details to a spreadsheet
- **Character counter** - Shows hashtag length in the description field
- **Form dropdowns** - Uses real Depop categories and brands

## 💡 Why I Made It

I was spending way too much time organizing photos for Depop listings and wanted to see if I could automate the boring parts. Since I don't have a traditional programming background, I used Claude Code to help build something functional.

**The Problem:** Manually organizing photos, tracking inventory, and creating listings was taking forever.

**My Approach:** Build a simple web interface to streamline the workflow, with Claude doing most of the technical heavy lifting while I provided direction and testing.

## Quick Start Guide

### Option 1: Web Photo Organizer (Recommended)
1. **Setup**: Run `./setup.sh` (one time only)
2. **Drop photos** into `photos/staging/` folder  
3. **Launch organizer**: `./launch_organizer.sh` (opens web interface)
4. **Group and tag photos** using the visual interface
5. **Submit form** - photos get copied to organized folders  
6. **Click "Open Folder"** to easily drag photos into Depop

### Option 2: Command Line Photo Tool  
1. **Setup**: Run `./setup.sh` (one time only)
2. **Drop photos** into `photos/staging/` folder  
3. **Run script**: `python3 photo_analyzer.py`
4. **Enter details** for each photo manually
5. **Photos organized** and **inventory populated**

### Option 3: Manual Process
1. **Add your items** to `data/inventory_tracker.csv`
2. **Organize photos** in the `photos/` folder using the naming convention
3. **Use listing templates** from `docs/listing_templates.md` to create descriptions
4. **Check daily tasks** in `docs/daily_tasks.md` for routine activities
5. **Track your progress** in `session_summary.md`

## Project Structure

```
Depop_Selling/
├── data/                           # Spreadsheets and tracking files
│   ├── inventory_tracker.csv       # Main inventory database
│   ├── hashtag_bank.csv           # Trending hashtags by category
│   └── pricing_research.csv       # Competitor pricing data
├── photos/                         # Photo management system
│   ├── by_category/               # Photos organized by type
│   ├── ready_for_depop/           # Item-specific folders for easy uploading
│   └── staging/                   # New photos to be processed
├── docs/                          # Guides and templates
│   ├── depop_guide.md            # Comprehensive selling tips
│   ├── listing_templates.md      # Pre-written descriptions
│   ├── photo_checklist.md        # Photo quality standards
│   ├── photo_assessment_guide.md # Photo workflow guide
│   ├── daily_tasks.md            # Routine activities
│   └── listing_workflow.md       # Step-by-step process
├── photo_organizer.html           # Web-based photo organizer interface
├── photo_server.py               # Backend server for web organizer
├── photo_analyzer.py             # Photo organization script
├── launch_organizer.sh           # Launches web organizer
├── setup.sh                      # One-time setup script
└── session_summary.md            # Daily progress tracking
```

## Key Features

- **🌐 Web Photo Organizer**: Visual interface for grouping photos with real-time preview
- **📁 Dual Organization**: Photos stored in both category folders and item-specific folders  
- **🔗 Direct Depop Integration**: "Open Folder" button opens item folders for easy drag-and-drop
- **🎯 Authentic Form Fields**: Real Depop categories, brands, and options (scraped from actual site)
- **📊 Inventory Management**: Track all items with photos, descriptions, and status
- **📸 Photo Organization**: Organize photos by category and item-specific folders
- **🏷️ Listing Optimization**: Templates and hashtags based on 2025 Depop best practices
- **⚡ Streamlined Workflow**: 30-minute process from photo to listing
- **📈 Progress Tracking**: Monitor sales, profits, and engagement

## Getting Help

This project is designed to be collaborative. Use Claude Code to:
- **Generate listing titles and descriptions** from inventory data
- **Research pricing for similar items** and update market data
- **Update inventory tracking** and performance metrics
- **Get suggestions for hashtags and categories** based on trends
- **Analyze sales performance** and optimize strategies
- **Create seasonal updates** for templates and hashtags

## Important Depop Facts (2025)
- No selling fees for listings created after July 15, 2024
- Transaction fee: 3.3% + $0.45 in the US
- 90% of users are under 26 (Gen Z focused)
- Items 40% more likely to sell with video
- Refreshing listings bumps them to top of search

