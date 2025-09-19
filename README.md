# Depop Selling Project

A comprehensive system to streamline your Depop selling process, from inventory management to listing optimization.

## Quick Start Guide

### Option 1: Web Photo Organizer (Recommended)
1. **Setup**: Run `./setup.sh` (one time only)
2. **Drop photos** into `photos/staging/` folder  
3. **Launch organizer**: `./launch_organizer.sh` (opens web interface)
4. **Group and tag photos** using the visual interface
5. **Photos automatically organized** in both category and item-specific folders
6. **Click "Open Folder"** to easily drag photos into Depop

### Option 2: Photo Assessment Workflow  
1. **Setup**: Run `./setup.sh` (one time only)
2. **Drop photos** into `photos/staging/` folder  
3. **Run analyzer**: `python3 photo_analyzer.py`
4. **Confirm details** for each photo interactively
5. **Photos automatically organized** and **inventory populated**

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
│   ├── photo_assessment_guide.md # AI photo analysis workflow
│   ├── daily_tasks.md            # Routine activities
│   └── listing_workflow.md       # Step-by-step process
├── photo_organizer.html           # Web-based photo organizer interface
├── photo_server.py               # Backend server for web organizer
├── photo_analyzer.py             # AI photo analysis script
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
- **🤖 AI Photo Assessment**: Drop photos, get automated analysis and organization
- **📸 Smart Photo Organization**: Automated naming and categorization
- **🏷️ Listing Optimization**: Templates and hashtags based on 2025 Depop best practices
- **⚡ Streamlined Workflow**: 30-minute process from photo to listing
- **📈 Progress Tracking**: Monitor sales, profits, and engagement

## Getting Help

This project is designed to be collaborative. Use Claude Code to:
- **Analyze photos automatically** using the photo assessment system
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