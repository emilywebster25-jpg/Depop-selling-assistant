# Depop Selling Project - Claude Instructions

## Project Overview
This project helps Emily streamline her Depop selling process with organized inventory management, photo tracking, and listing optimization.

## Standard Workflow
1. First think through the problem, read the codebase for relevant files, and write a plan to todo.md, then create a 'session summary' document to track where we are up to in the day's session
2. The plan should have a list of todo items that you can check off as you complete them
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, add a review section to the todo.md file with a summary of the changes you made and any other relevant information, every time you make this change, and also update the session summary MD

## Project-Specific Guidelines
- This is for a non-technical user with no coding experience
- Focus on simple, practical tools that make selling easier
- All file names should be clear and descriptive
- Use CSV files for data tracking (easy to open in Excel/Google Sheets)
- Provide step-by-step guides for all processes
- Make everything collaborative between AI and human

## Depop Context
- User has photos of items that are steamed and ready
- Photo assessment system available for automated analysis and organization
- Interactive workflow: AI suggests details, human confirms/edits
- Needs help with listing titles, descriptions, and performance optimization
- Following 2025 Depop best practices (no selling fees, focus on engagement)
- Target audience is Gen Z (90% under 26)

## Photo Assessment Workflow
1. User drops photos in `photos/staging/` folder
2. Runs `python3 photo_analyzer.py` for interactive analysis
3. AI suggests item details (brand, category, size, condition, etc.)
4. User confirms/edits suggestions through prompts
5. System automatically organizes photos and updates inventory
6. Ready to create listings using templates and organized data

## AI Collaboration Features
- Help analyze photos and suggest details
- Generate optimized listing titles and descriptions using inventory data
- Research competitive pricing and update market data
- Suggest trending hashtags based on item categories
- Analyze sales performance and recommend optimizations
- Create seasonal updates for templates and strategies