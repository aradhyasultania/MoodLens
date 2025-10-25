#!/bin/bash
# MoodLens Launcher Script

echo "🧠 Starting MoodLens..."
echo ""

# Activate virtual environment
source moodlens-env/bin/activate

# Set PYTHONPATH to project root
export PYTHONPATH=.

# Run the application
python moodlens_simplified.py

