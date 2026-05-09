# FastAPI Backend Deployment Guide

This guide will help you deploy your FastAPI backend to Render.com.

## 📁 Project Structure

```
demo/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration (optional)
├── render.yaml         # Render Docker deployment config (optional)
├── render-python.yaml  # Render Python deployment config (recommended)
├── .gitignore          # Git ignore file
└── DEPLOYMENT_GUIDE.md # This guide
```

## 🚀 Quick Start

### 1. Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Or use uvicorn directly
uvicorn main:app --reload
```

Visit `http://localhost:8000` to see your API, and `http://localhost:8000/docs` for interactive documentation.

### 2. Deploy to Render

You have **two deployment options**:

## Option 1: Python Runtime (Recommended - Simpler)
## Option 2: Docker (More control)

---

### Option 1: Python Runtime Deployment (No Docker)

#### Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:

```bash
git init
git add .
git commit -m "Initial FastAPI backend"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

#### Step 2: Deploy on Render (Python)

1. Go to [render.com](https://render.com)
2. Sign up/login with your GitHub account
3. Click "New +" → "Web Service"
4. Select your GitHub repository
5. Configure the service:
   - **Name**: `fastapi-backend` (or your preferred name)
   - **Environment**: `Python`
   - **Python Version**: `3.11`
   - **Branch**: `main`
   - **Root Directory**: Leave empty (root of repo)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` (for testing) or `Starter` ($7/month for production)
   - **Auto-Deploy**: ✅ Enable

6. Click "Create Web Service"

---

### Option 2: Docker Deployment

#### Step 1: Push to GitHub

Same as above - push your code to GitHub.

#### Step 2: Deploy on Render (Docker)

1. Go to [render.com](https://render.com)
2. Sign up/login with your GitHub account
3. Click "New +" → "Web Service"
4. Select your GitHub repository
5. Configure the service:
   - **Name**: `fastapi-backend` (or your preferred name)
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Root Directory**: Leave empty (root of repo)
   - **Dockerfile Path**: `Dockerfile`
   - **Instance Type**: `Free` (for testing) or `Starter` ($7/month for production)
   - **Auto-Deploy**: ✅ Enable

6. Click "Create Web Service"

#### Step 3: Monitor Deployment

- Render will automatically build and deploy your application
- You can monitor the build logs in the Render dashboard
- Once deployed, you'll get a URL like `https://fastapi-backend.onrender.com`

## 🔧 Configuration Details

### Dockerfile Explained

```dockerfile
FROM python:3.11-slim          # Lightweight Python image
WORKDIR /app                    # Set working directory
COPY requirements.txt .         # Copy dependencies first
RUN pip install --no-cache-dir -r requirements.txt  # Install dependencies
COPY main.py .                  # Copy application code
EXPOSE 8000                     # Expose port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  # Run command
```

### render.yaml Explained

The `render.yaml` file provides deployment configuration:

- **type: web**: Web service
- **env: docker**: Use Docker deployment
- **plan: free**: Free tier (limited resources)
- **healthCheckPath: /health**: Health check endpoint
- **autoDeploy: true**: Auto-deploy on git push

## 📚 API Endpoints

Once deployed, your API will have these endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/items` | Get all items |
| GET | `/items/{id}` | Get specific item |
| POST | `/items` | Create new item |
| PUT | `/items/{id}` | Update item |
| DELETE | `/items/{id}` | Delete item |

## 🧪 Testing Your API

### Using the Interactive Docs

Visit `https://your-app-url.onrender.com/docs` for Swagger UI documentation.

### Using curl

```bash
# Get all items
curl https://your-app-url.onrender.com/items

# Create an item
curl -X POST https://your-app-url.onrender.com/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item", "price": 29.99}'

# Get a specific item
curl https://your-app-url.onrender.com/items/1
```

## 🔍 Troubleshooting

### Common Issues

1. **Build fails**: Check the build logs in Render dashboard
2. **503 Service Unavailable**: The app might still be starting (cold start on free tier)
3. **Health check fails**: Ensure `/health` endpoint returns 200 status
4. **Memory issues**: Free tier has limited RAM, upgrade to Starter for production

### Logs

You can view logs in the Render dashboard under your service → "Logs".

## 🚀 Production Tips

1. **Upgrade to Starter Plan**: Free tier has sleep periods
2. **Add Environment Variables**: Use Render's environment variables for secrets
3. **Monitor Performance**: Use Render's metrics dashboard
4. **Set Up Custom Domain**: Available on paid plans
5. **Add HTTPS**: Render provides automatic SSL certificates

## 📞 Support

- Render docs: [https://render.com/docs](https://render.com/docs)
- FastAPI docs: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- Issues: Check Render's status page for platform issues
