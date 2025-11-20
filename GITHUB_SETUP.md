# GitHub Repository Setup Instructions

This guide will help you create a GitHub repository for your Weather CLI application and upload all the code.

## 📋 Prerequisites

- A GitHub account ([Sign up here](https://github.com/join) if you don't have one)
- Python 3.7+ installed
- PyGithub library installed

## 🚀 Quick Start

### Step 1: Install PyGithub

```bash
pip install PyGithub
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Create a GitHub Personal Access Token

1. **Go to GitHub Settings**
   - Visit: https://github.com/settings/tokens
   - Or navigate: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**
   - Click **"Generate new token"** → **"Generate new token (classic)"**

3. **Configure Token**
   - **Note**: Give it a descriptive name (e.g., "Weather CLI Repository Upload")
   - **Expiration**: Choose expiration period (recommend: 30 days for one-time use)
   - **Select scopes**: Check the **`repo`** checkbox (this selects all repo permissions)
     ```
     ✓ repo
       ✓ repo:status
       ✓ repo_deployment
       ✓ public_repo
       ✓ repo:invite
       ✓ security_events
     ```

4. **Generate and Copy Token**
   - Click **"Generate token"** at the bottom
   - **⚠️ IMPORTANT**: Copy the token immediately! You won't be able to see it again.
   - The token looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 3: Set Environment Variable

Choose the method for your operating system:

#### Linux / macOS / WSL

```bash
export GITHUB_TOKEN='ghp_your_token_here'
```

To make it persistent for the current session, add it to your shell:

```bash
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

Or for zsh:

```bash
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

#### Windows (PowerShell)

```powershell
$env:GITHUB_TOKEN='ghp_your_token_here'
```

To make it persistent:

```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'ghp_your_token_here', 'User')
```

#### Windows (Command Prompt)

```cmd
set GITHUB_TOKEN=ghp_your_token_here
```

### Step 4: Run the Repository Creation Script

```bash
cd /app/workspaces/proj-alpha/weather-cli
python create_github_repo.py
```

## 📤 What the Script Does

The `create_github_repo.py` script will:

1. ✅ Authenticate with GitHub using your token
2. ✅ Create a new public repository named `weather-cli`
3. ✅ Upload all project files:
   - `weather_cli.py` - Main application
   - `README.md` - Documentation
   - `requirements.txt` - Dependencies
   - `.gitignore` - Git ignore rules
   - `pytest.ini` - Pytest configuration
   - `tests/` - All test files
4. ✅ Provide you with the repository URL and clone instructions

## 📊 Expected Output

When successful, you'll see:

```
============================================================
  GitHub Repository Creator - Weather CLI
============================================================

✓ Authenticated as: your-username
  Name: Your Name
  Email: your.email@example.com

📦 Creating repository 'weather-cli'...
✓ Repository created: https://github.com/your-username/weather-cli

📤 Uploading files from: /app/workspaces/proj-alpha/weather-cli
  ✓ .gitignore
  ✓ README.md
  ✓ pytest.ini
  ✓ requirements.txt
  ✓ weather_cli.py
  ✓ tests/__init__.py
  ✓ tests/conftest.py
  ✓ tests/test_weather_cli.py

📊 Upload Summary:
  Total files: 8
  Uploaded: 8
  Failed: 0

✓ Repository initialized with branch: main

============================================================
✅ SUCCESS!
============================================================

🎉 Your repository is ready!

📍 Repository URL: https://github.com/your-username/weather-cli
📍 Clone URL (HTTPS): https://github.com/your-username/weather-cli.git
📍 Clone URL (SSH): git@github.com:your-username/weather-cli.git

📋 Next steps:
   git clone https://github.com/your-username/weather-cli.git
   cd weather-cli
   # Start using your weather CLI!

============================================================
```

## 🔧 Troubleshooting

### Error: "GITHUB_TOKEN environment variable not set"

**Solution**: Make sure you've exported the token in your current terminal session:

```bash
export GITHUB_TOKEN='your_token_here'
echo $GITHUB_TOKEN  # Verify it's set
```

### Error: "Authentication failed"

**Possible causes**:
- Token is invalid or expired
- Token doesn't have `repo` permissions
- Token was copied incorrectly (extra spaces, missing characters)

**Solution**: Generate a new token and ensure you select the `repo` scope.

### Error: "Repository 'weather-cli' already exists"

**Solution**: Either:
1. Delete the existing repository from GitHub
2. Or modify the `REPO_NAME` variable in `create_github_repo.py` to use a different name

### Error: "Some files failed to upload"

**Possible causes**:
- Network connectivity issues
- Rate limiting
- File size limits (>100MB)

**Solution**:
- Check your internet connection
- Wait a few minutes and try again
- Check file sizes: `ls -lh`

## 🔐 Security Best Practices

1. **Never commit your token to a repository**
   - The `.gitignore` file already excludes common token file names
   - Never hardcode tokens in scripts

2. **Use tokens with minimal permissions**
   - Only grant `repo` scope for this task
   - Delete the token after use if you don't need it

3. **Set token expiration**
   - Use short expiration periods for one-time tasks
   - Regenerate tokens periodically for ongoing use

4. **Revoke tokens when done**
   - Go to https://github.com/settings/tokens
   - Click "Delete" next to tokens you no longer need

## 📝 Manual Alternative (Using Git CLI)

If you prefer using Git directly, you can also push manually:

```bash
cd /app/workspaces/proj-alpha/weather-cli

# Initialize git repository
git init
git add .
git commit -m "Initial commit: Weather CLI application

- Add weather_cli.py with OpenWeatherMap integration
- Add comprehensive README with usage examples
- Add unit tests with pytest
- Add requirements.txt and configuration files

🤖 Generated with Claude Code"

# Create repository on GitHub (via web interface)
# Then add remote and push

git remote add origin https://github.com/your-username/weather-cli.git
git branch -M main
git push -u origin main
```

## 🎯 Repository Customization

To customize the repository before creation, edit `create_github_repo.py`:

```python
# Line ~185
REPO_NAME = "weather-cli"  # Change repository name
REPO_DESCRIPTION = "Your custom description"  # Change description
PRIVATE_REPO = False  # Set to True for private repository
```

## 📚 Additional Resources

- [GitHub Personal Access Tokens Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [GitHub API Documentation](https://docs.github.com/en/rest)

## ✅ Verification Checklist

Before running the script, ensure:

- [ ] PyGithub is installed (`pip list | grep PyGithub`)
- [ ] GitHub token is created with `repo` scope
- [ ] `GITHUB_TOKEN` environment variable is set
- [ ] You're in the weather-cli directory
- [ ] All files are present (check with `ls -la`)

## 🆘 Support

If you encounter any issues:

1. Check the error message carefully
2. Refer to the troubleshooting section above
3. Verify your token permissions at https://github.com/settings/tokens
4. Check GitHub's status page: https://www.githubstatus.com/

---

**Ready to create your repository?** Run:

```bash
python create_github_repo.py
```

Good luck! 🚀
