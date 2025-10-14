#!/bin/bash

# Git Credentials Setup Script
# This script helps configure Git with your GitHub credentials

echo "🔐 Setting up Git credentials for GitHub"
echo "======================================="

# Check if git is configured
echo "📋 Current Git configuration:"
git config --global --list | grep -E "(user\.name|user\.email|credential)" || echo "No Git configuration found"

echo ""
echo "🔧 Let's configure Git with your GitHub credentials:"
echo ""

# Get user information
read -p "Enter your GitHub username: " github_username
read -p "Enter your GitHub email: " github_email
read -p "Enter your GitHub Personal Access Token: " -s github_token
echo ""

# Configure Git user
echo "⚙️  Configuring Git user information..."
git config --global user.name "$github_username"
git config --global user.email "$github_email"

# Configure credential helper
echo "🔑 Setting up credential helper..."
git config --global credential.helper store

# Create credential file
echo "💾 Storing credentials securely..."
echo "https://$github_username:$github_token@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

echo ""
echo "✅ Git credentials configured successfully!"
echo ""
echo "📋 Configuration summary:"
echo "  Username: $github_username"
echo "  Email: $github_email"
echo "  Credential helper: store"
echo ""
echo "🔒 Your credentials are stored securely in ~/.git-credentials"
echo "   You won't need to enter them again for this machine."
echo ""
echo "🧪 Testing Git authentication..."
echo "   Run: git ls-remote https://github.com/$github_username/arxml-editor.git"
echo "   If successful, you're all set!"
echo ""
echo "🚀 You can now push to GitHub without re-entering credentials!"