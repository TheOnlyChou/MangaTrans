#!/usr/bin/env zsh
# Quick start demo script

echo "🚀 Manga Translator V1 - Quick Start Demo"
echo ""

# Activate venv
source .venv/bin/activate

echo "📦 Installing project (if not already installed)..."
pip install -e ".[dev]" > /dev/null 2>&1

echo ""
echo "Running tests..."
pytest -v

echo ""
echo "📝 Generating sample translation..."
mkdir -p input output
touch input/sample_page.png

mangatrans translate input/sample_page.png -o output/sample_page.json --src ja --tgt en

echo ""
echo "Generated JSON (schema v1.0):"
cat output/sample_page.json | python -m json.tool

echo ""
echo "✨ Done! Check README.md for more details."