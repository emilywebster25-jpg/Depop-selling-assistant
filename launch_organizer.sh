#!/bin/bash

# Depop Photo Organizer Launcher
echo "🚀 Starting Depop Photo Organizer..."
echo "=================================="

# Get the project directory
PROJECT_DIR="/Users/emilywebster/Dev/Depop_Selling"
HTML_FILE="$PROJECT_DIR/photo_organizer.html"

# Check if the HTML file exists
if [ ! -f "$HTML_FILE" ]; then
    echo "❌ Photo organizer not found at $HTML_FILE"
    echo "Please make sure you're in the right directory."
    exit 1
fi

echo "✅ Found photo organizer web app"
echo "📂 Project directory: $PROJECT_DIR"
echo ""
echo "🚀 Starting photo organizer server..."
echo "📸 The app will automatically load your photos from the staging folder!"
echo ""
echo "💡 The app will:"
echo "   • Auto-load all photos from photos/staging/ folder"
echo "   • Let you group photos of the same item together"
echo "   • Fill in item details (brand, size, price, etc.)"
echo "   • Automatically organize photos and update inventory"
echo ""

# Start the Python server
echo "⚡ Starting server..."
python3 "$PROJECT_DIR/photo_server.py" &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

echo "🌐 Server running at http://localhost:8001"

# Try to open in different browsers (Mac)
if command -v open >/dev/null 2>&1; then
    echo "🍎 Opening in default browser on Mac..."
    open "http://localhost:8001"
elif command -v xdg-open >/dev/null 2>&1; then
    echo "🐧 Opening in default browser on Linux..."
    xdg-open "http://localhost:8001"
elif command -v start >/dev/null 2>&1; then
    echo "🪟 Opening in default browser on Windows..."
    start "http://localhost:8001"
else
    echo "🌐 Please open this URL in your browser:"
    echo "   http://localhost:8001"
fi

echo ""
echo "✨ Photo organizer is now running!"
echo "📂 It will automatically show your 154 photos from the staging folder"
echo "🛑 Press Ctrl+C to stop the server when you're done"
echo ""

# Wait for server process
wait $SERVER_PID