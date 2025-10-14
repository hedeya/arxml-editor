#!/bin/bash

# SSH Key Setup for GitHub
# This script helps set up SSH key authentication with GitHub

echo "🔐 Setting up SSH key authentication for GitHub"
echo "=============================================="

# Check if SSH key already exists
if [ -f ~/.ssh/id_rsa.pub ] || [ -f ~/.ssh/id_ed25519.pub ]; then
    echo "✅ SSH key already exists!"
    echo "📋 Your public key:"
    if [ -f ~/.ssh/id_ed25519.pub ]; then
        cat ~/.ssh/id_ed25519.pub
        echo ""
        echo "📋 Copy the above key and add it to GitHub:"
        echo "   1. Go to GitHub.com → Settings → SSH and GPG keys"
        echo "   2. Click 'New SSH key'"
        echo "   3. Paste the key above"
        echo "   4. Give it a title like 'ARXML Editor Development'"
        echo "   5. Click 'Add SSH key'"
    else
        cat ~/.ssh/id_rsa.pub
        echo ""
        echo "📋 Copy the above key and add it to GitHub:"
        echo "   1. Go to GitHub.com → Settings → SSH and GPG keys"
        echo "   2. Click 'New SSH key'"
        echo "   3. Paste the key above"
        echo "   4. Give it a title like 'ARXML Editor Development'"
        echo "   5. Click 'Add SSH key'"
    fi
else
    echo "🔑 No SSH key found. Let's create one..."
    echo ""
    
    # Get user email
    read -p "Enter your GitHub email: " github_email
    
    # Generate SSH key
    echo "⚙️  Generating SSH key..."
    ssh-keygen -t ed25519 -C "$github_email" -f ~/.ssh/id_ed25519 -N ""
    
    # Start SSH agent
    echo "🚀 Starting SSH agent..."
    eval "$(ssh-agent -s)"
    
    # Add key to SSH agent
    echo "🔑 Adding key to SSH agent..."
    ssh-add ~/.ssh/id_ed25519
    
    # Display public key
    echo "✅ SSH key generated successfully!"
    echo "📋 Your public key:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "📋 Next steps:"
    echo "   1. Copy the key above"
    echo "   2. Go to GitHub.com → Settings → SSH and GPG keys"
    echo "   3. Click 'New SSH key'"
    echo "   4. Paste the key above"
    echo "   5. Give it a title like 'ARXML Editor Development'"
    echo "   6. Click 'Add SSH key'"
fi

echo ""
echo "🧪 Testing SSH connection..."
echo "   Run: ssh -T git@github.com"
echo "   You should see: 'Hi username! You've successfully authenticated...'"
echo ""
echo "🔧 To use SSH with your repository:"
echo "   git remote set-url origin git@github.com:hedeya/arxml-editor.git"
echo ""
echo "🚀 SSH authentication is more secure than tokens!"