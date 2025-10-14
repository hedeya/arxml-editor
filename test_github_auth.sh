#!/bin/bash

echo "🔐 Testing GitHub Authentication"
echo "==============================="

# Check if credentials file exists
if [ -f ~/.git-credentials ]; then
    echo "✅ Credentials file found"
    echo "📋 Contents:"
    cat ~/.git-credentials | sed 's/:[^@]*@/:***@/g'  # Hide the token
else
    echo "❌ No credentials file found"
    echo "   Please set up your Personal Access Token first"
    exit 1
fi

echo ""
echo "🧪 Testing repository access..."

# Test if we can access the repository
if git ls-remote https://github.com/hedeya/arxml-editor.git >/dev/null 2>&1; then
    echo "✅ Authentication successful!"
    echo "🚀 You can now push your code with: git push -u origin main"
else
    echo "❌ Authentication failed"
    echo "   Please check your Personal Access Token"
    echo "   Make sure it has 'repo' scope enabled"
fi