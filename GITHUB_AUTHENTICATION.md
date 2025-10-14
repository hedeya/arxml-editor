# GitHub Authentication Setup Guide

This guide will help you set up GitHub authentication so you don't need to login each time you push to the repository.

## 🔐 **Authentication Methods**

### **Method 1: Personal Access Token (Easiest)**

#### Step 1: Create Personal Access Token
1. Go to [GitHub.com](https://github.com) → Settings → Developer settings
2. Click "Personal access tokens" → "Tokens (classic)"
3. Click "Generate new token (classic)"
4. Fill in the form:
   - **Note**: "ARXML Editor Development"
   - **Expiration**: Choose appropriate duration (90 days recommended)
   - **Scopes**: Select `repo`, `workflow`, `write:packages`
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

#### Step 2: Configure Git
```bash
# Run the setup script
./setup_git_credentials.sh

# Or configure manually:
git config --global user.name "hedeya"
git config --global user.email "your-email@example.com"
git config --global credential.helper store
```

#### Step 3: Test Authentication
```bash
# Test with your repository
git ls-remote https://github.com/hedeya/arxml-editor.git
```

---

### **Method 2: SSH Key Authentication (Most Secure)**

#### Step 1: Generate SSH Key
```bash
# Run the SSH setup script
./setup_ssh_github.sh

# Or generate manually:
ssh-keygen -t ed25519 -C "your-email@example.com"
```

#### Step 2: Add Key to GitHub
1. Copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. Go to GitHub.com → Settings → SSH and GPG keys
3. Click "New SSH key"
4. Paste the key and give it a title
5. Click "Add SSH key"

#### Step 3: Test SSH Connection
```bash
ssh -T git@github.com
# Should show: "Hi hedeya! You've successfully authenticated..."
```

#### Step 4: Update Repository URL
```bash
# Change from HTTPS to SSH
git remote set-url origin git@github.com:hedeya/arxml-editor.git
```

---

## 🚀 **Quick Setup Commands**

### For Personal Access Token:
```bash
# 1. Create token on GitHub (see Method 1 above)
# 2. Run setup script
./setup_git_credentials.sh

# 3. Test authentication
git push origin main
```

### For SSH Key:
```bash
# 1. Generate and add SSH key
./setup_ssh_github.sh

# 2. Add key to GitHub (see Method 2 above)

# 3. Update repository URL
git remote set-url origin git@github.com:hedeya/arxml-editor.git

# 4. Test authentication
git push origin main
```

---

## 🔧 **Manual Configuration**

If you prefer to configure manually:

### Personal Access Token:
```bash
# Configure Git user
git config --global user.name "hedeya"
git config --global user.email "your-email@example.com"

# Store credentials
git config --global credential.helper store

# Create credentials file
echo "https://hedeya:YOUR_TOKEN@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials
```

### SSH Key:
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Display public key
cat ~/.ssh/id_ed25519.pub
# Copy this key to GitHub
```

---

## 🧪 **Testing Your Setup**

### Test Personal Access Token:
```bash
# Test repository access
git ls-remote https://github.com/hedeya/arxml-editor.git

# Test push (after making a commit)
git add .
git commit -m "Test commit"
git push origin main
```

### Test SSH Key:
```bash
# Test SSH connection
ssh -T git@github.com

# Test repository access
git ls-remote git@github.com:hedeya/arxml-editor.git

# Test push (after making a commit)
git add .
git commit -m "Test commit"
git push origin main
```

---

## 🔒 **Security Best Practices**

### Personal Access Token:
- ✅ **Use minimal scopes** (only what you need)
- ✅ **Set expiration date** (90 days recommended)
- ✅ **Store securely** (use credential helper)
- ✅ **Rotate regularly** (create new token before old one expires)

### SSH Key:
- ✅ **Use strong key type** (ed25519 recommended)
- ✅ **Protect private key** (don't share or commit)
- ✅ **Use passphrase** (optional but recommended)
- ✅ **Add to SSH agent** (for convenience)

---

## 🆘 **Troubleshooting**

### Common Issues:

**"Authentication failed":**
- Check username/token is correct
- Verify token has correct scopes
- Ensure token hasn't expired

**"Permission denied (publickey)":**
- Verify SSH key is added to GitHub
- Check SSH agent is running: `ssh-add -l`
- Test SSH connection: `ssh -T git@github.com`

**"Repository not found":**
- Check repository URL is correct
- Verify you have access to the repository
- Ensure repository exists on GitHub

### Debug Commands:
```bash
# Check Git configuration
git config --global --list

# Check SSH keys
ssh-add -l

# Test SSH connection
ssh -T git@github.com

# Check remote URL
git remote -v

# Test repository access
git ls-remote origin
```

---

## 📋 **Summary**

### Recommended Setup:
1. **Use SSH Key** for maximum security
2. **Use Personal Access Token** for simplicity
3. **Test authentication** before committing
4. **Keep credentials secure** and rotate regularly

### Quick Start:
```bash
# Choose one method:
./setup_ssh_github.sh      # SSH Key (recommended)
# OR
./setup_git_credentials.sh # Personal Access Token
```

---

**You're all set!** 🚀 Once configured, you can push to GitHub without entering credentials each time.