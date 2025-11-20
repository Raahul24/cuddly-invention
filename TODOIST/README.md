# Todoist Clone - Deployment Guide

## 🚀 Deploy to Railway

This app is ready to deploy to [Railway](https://railway.app) with zero configuration!

### Prerequisites
- A [Railway](https://railway.app) account (free tier available)
- Git repository (GitHub, GitLab, or Bitbucket)

### Deployment Steps

1. **Push to Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the configuration and deploy!

3. **Access Your App**
   - Railway will provide a public URL
   - Your app will be live at: `https://your-app.up.railway.app`

### Environment Variables (Optional)

Railway automatically handles:
- `PORT` - Server port (set by Railway)
- Database storage - SQLite file persists automatically

### Configuration Files

✅ All deployment files are included:
- `Procfile` - Start command
- `railway.toml` - Railway configuration
- `backend/requirements.txt` - Python dependencies
- `runtime.txt` - Python version
- `.gitignore` - Git exclusions

### Local Development

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run locally
cd backend
uvicorn main:app --reload

# Visit http://localhost:8000
```

### Database

- **Development**: SQLite (`todoist.db`)
- **Production**: SQLite with Railway's persistent volumes
- Data persists across deployments

### Features Available

✅ Tasks CRUD
✅ Projects & Labels
✅ Custom Filters
✅ Advanced Reminders (Time, Relative, Location)
✅ Activity History
✅ Task Editing
✅ Dark Mode Ready

### Troubleshooting

**App won't start?**
- Check Railway logs
- Ensure `requirements.txt` includes all dependencies
- Verify Python version in `runtime.txt`

**Database not persisting?**
- Railway automatically handles SQLite persistence
- Check deployment logs for write permissions

**Need help?**
- [Railway Docs](https://docs.railway.app)
- [FastAPI Docs](https://fastapi.tiangolo.com)

---

Built with ❤️ using FastAPI, SQLite, and Vanilla JS
