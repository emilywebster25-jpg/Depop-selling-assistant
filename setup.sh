#!/bin/bash

# Depop Selling Project Setup Script
echo "🛍️  Depop Selling Project Setup"
echo "=============================="

# Check if Python 3 is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION found"
else
    echo "❌ Python 3 not found. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
echo "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found"
elif command -v pip &> /dev/null; then
    echo "✅ pip found"
else
    echo "❌ pip not found. Please install pip first."
    exit 1
fi

# Install required Python packages
echo ""
echo "Installing required Python packages..."
echo "This may take a few minutes..."

PACKAGES=("pillow")
OPTIONAL_PACKAGES=("requests" "openai" "anthropic")

for package in "${PACKAGES[@]}"; do
    echo "Installing $package..."
    pip3 install "$package" --quiet
    if [ $? -eq 0 ]; then
        echo "✅ $package installed successfully"
    else
        echo "❌ Failed to install $package"
        exit 1
    fi
done

echo ""
echo "Optional AI packages (install if you want AI vision features):"
for package in "${OPTIONAL_PACKAGES[@]}"; do
    echo "To install $package later, run: pip3 install $package"
done

# Make scripts executable
echo ""
echo "Setting up script permissions..."
chmod +x photo_analyzer.py
chmod +x setup.sh
echo "✅ Scripts made executable"

# Create any missing directories
echo ""
echo "Ensuring all directories exist..."
mkdir -p "photos/staging"
mkdir -p "photos/by_category/tops"
mkdir -p "photos/by_category/dresses" 
mkdir -p "photos/by_category/bottoms"
mkdir -p "photos/by_category/outerwear"
mkdir -p "photos/by_category/shoes"
mkdir -p "photos/by_category/accessories"
echo "✅ Directory structure verified"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Add photos to the 'photos/staging/' folder"
echo "2. Run: python3 photo_analyzer.py"
echo "3. Follow the interactive prompts"
echo ""
echo "For help, see: docs/photo_assessment_guide.md"
echo ""
echo "Happy selling! 📸✨"