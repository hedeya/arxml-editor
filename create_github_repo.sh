#!/bin/bash

# Create GitHub Repository Script
# This script creates the ARXML Editor repository on GitHub

echo "🚀 Creating GitHub Repository for ARXML Editor"
echo "=============================================="

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found. Creating repository..."
    
    # Create repository
    gh repo create arxml-editor \
        --public \
        --description "Professional AUTOSAR XML (ARXML) editor with dynamic schema detection, validation, and comprehensive editing capabilities" \
        --homepage "https://github.com/hedeya/arxml-editor#readme" \
        --add-readme=false \
        --clone=false
    
    if [ $? -eq 0 ]; then
        echo "✅ Repository created successfully!"
        
        # Add remote origin
        git remote add origin https://github.com/hedeya/arxml-editor.git
        
        # Push to GitHub
        echo "📤 Pushing code to GitHub..."
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo "🎉 Repository created and code pushed successfully!"
            echo "📍 Repository URL: https://github.com/hedeya/arxml-editor"
        else
            echo "❌ Failed to push code. Please check your authentication."
        fi
    else
        echo "❌ Failed to create repository. Please check your GitHub CLI authentication."
        echo "   Run: gh auth login"
    fi
else
    echo "⚠️  GitHub CLI not found. Please create the repository manually:"
    echo ""
    echo "📋 Manual Steps:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: arxml-editor"
    echo "3. Description: Professional AUTOSAR XML (ARXML) editor with dynamic schema detection, validation, and comprehensive editing capabilities"
    echo "4. Set to Public"
    echo "5. Don't initialize with README, .gitignore, or license (we already have them)"
    echo "6. Click 'Create repository'"
    echo ""
    echo "🔗 Then run these commands:"
    echo "   git remote add origin https://github.com/hedeya/arxml-editor.git"
    echo "   git push -u origin main"
    echo ""
    echo "📚 Or install GitHub CLI:"
    echo "   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg"
    echo "   echo \"deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main\" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null"
    echo "   sudo apt update"
    echo "   sudo apt install gh"
    echo "   gh auth login"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Visit your repository: https://github.com/hedeya/arxml-editor"
echo "2. Share the repository with your team"
echo "3. Set up branch protection rules if needed"
echo "4. Configure GitHub Actions (already included)"
echo "5. Add collaborators in repository settings"
echo ""
echo "📚 Documentation:"
echo "- README.md: Project overview and usage"
echo "- CONTRIBUTING.md: Guidelines for contributors"
echo "- TEAM_GUIDE.md: Team collaboration guide"
echo "- docs/INSTALLATION.md: Detailed installation guide"
echo ""
echo "🚀 Happy coding!"