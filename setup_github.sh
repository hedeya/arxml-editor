#!/bin/bash

# GitHub Repository Setup Script for ARXML Editor
# This script helps set up the GitHub repository

echo "🚀 Setting up GitHub repository for ARXML Editor"
echo "================================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Check if there are any changes
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing initial files..."
    git commit -m "Initial commit: ARXML Editor v1.0.0

- Professional AUTOSAR XML editor
- Dynamic schema detection and validation
- Interactive editing capabilities
- Clean tree interface and diagram view
- Support for ARXML and ECUC files
- Windows distribution package included"
    echo "✅ Initial commit created"
fi

# Check if remote origin exists
if git remote get-url origin &> /dev/null; then
    echo "✅ Remote origin already configured"
    echo "📍 Current remote: $(git remote get-url origin)"
else
    echo "🔗 Setting up remote repository..."
    echo "Please follow these steps:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named 'arxml-editor'"
    echo "3. Don't initialize with README, .gitignore, or license (we already have them)"
    echo "4. Copy the repository URL"
    echo ""
    read -p "Enter the GitHub repository URL (https://github.com/hedeya/arxml-editor.git): " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote origin added: $repo_url"
    else
        echo "⚠️  No URL provided. You can add it later with:"
        echo "   git remote add origin https://github.com/hedeya/arxml-editor.git"
    fi
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
if git push -u origin main 2>/dev/null; then
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Repository setup complete!"
    echo "📍 Repository URL: https://github.com/hedeya/arxml-editor"
    echo ""
    echo "Next steps:"
    echo "1. Visit https://github.com/hedeya/arxml-editor"
    echo "2. Share the repository with your team"
    echo "3. Set up branch protection rules if needed"
    echo "4. Configure GitHub Actions (already included)"
    echo "5. Add collaborators in repository settings"
else
    echo "⚠️  Could not push to GitHub. This might be because:"
    echo "   - The repository doesn't exist yet"
    echo "   - You don't have push permissions"
    echo "   - Authentication is required"
    echo ""
    echo "Please:"
    echo "1. Create the repository on GitHub first"
    echo "2. Set up authentication (SSH key or personal access token)"
    echo "3. Run: git push -u origin main"
fi

echo ""
echo "📚 Documentation:"
echo "- README.md: Project overview and usage"
echo "- CONTRIBUTING.md: Guidelines for contributors"
echo "- docs/INSTALLATION.md: Detailed installation guide"
echo "- CHANGELOG.md: Version history and changes"
echo ""
echo "🔧 Development:"
echo "- Run tests: python -c \"from src.core.models.arxml_document import ARXMLDocument; print('Test passed')\""
echo "- Start application: python main.py"
echo "- Build executable: pyinstaller --onefile --windowed main.py"
echo ""
echo "Happy coding! 🚀"