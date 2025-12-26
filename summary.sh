#!/usr/bin/env zsh
# Project summary display

echo "📦 Manga Translator V1 - Project Summary"
echo "=========================================="
echo ""
echo "📂 Structure:"
tree -I '.venv|__pycache__|*.pyc|.pytest_cache|*.egg-info|.git|.idea' -L 3
echo ""
echo "📊 Tests:"
source .venv/bin/activate
pytest --tb=no -q
echo ""
echo "📈 Coverage:"
pytest --cov=mangatrans --cov-report=term --tb=no -q
echo ""
echo "📝 Files:"
echo "- README.md          : Complete documentation"
echo "- QUICKSTART.md      : Quick start guide"
echo "- DELIVERY.md        : Delivery summary"
echo "- docs/spec.md       : JSON schema v1.0 specification"
echo "- demo.sh            : Demonstration script"
echo ""
echo "✨ CLI Command:"
echo "mangatrans translate <image> -o <output.json> --src <lang> --tgt <lang>"
echo ""
echo "🎯 Status: READY FOR V1"