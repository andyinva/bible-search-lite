#!/bin/bash
# Test script to check gray highlighting debug output

cd /home/ajhinva/projects/bible-search-lite

echo "Starting Bible Search Lite with debug output..."
echo "Please:"
echo "1. Search for 'Jesus' and click a verse in Window 2 (should show gray highlight)"
echo "2. Create a subject and add verses to Window 4"
echo "3. Click a verse in Window 4 (should show gray highlight but doesn't)"
echo ""
echo "Watch for debug messages starting with 🔦 and 🎨"
echo ""

python3 bible_search_lite.py 2>&1 | grep -E "(🔦|🎨|Subject verse clicked)"
