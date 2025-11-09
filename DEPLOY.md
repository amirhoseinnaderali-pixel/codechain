# Deployment Guide - DevGenie

Complete guide for deploying DevGenie on various platforms.

## 🚀 Deployment Options

### 1. Railway (Recommended - Easiest)

Railway is the simplest and fastest platform for deployment.

#### Steps:

1. **Sign up for Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy your project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically deploy your project

3. **Configuration:**
   - Railway automatically reads `requirements.txt`
   - Port is automatically configured
   - You'll receive a public URL

**Advantages:**
- ✅ Free tier available
- ✅ Automatic deployment on Git push
- ✅ Automatic SSL
- ✅ Very simple setup

---

### 2. Render

Render is a simple cloud platform.

#### Steps:

1. **Sign up:**
   - Go to [render.com](https://render.com)
   - Sign in with GitHub

2. **Create Web Service:**
   - Click "New +"
   - Select "Web Service"
   - Connect your repository

3. **Configuration:**
   ```
   Name: devgenie
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn api:app --host 0.0.0.0 --port $PORT
   ```

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically deploy

**Advantages:**
- ✅ Free tier available
- ✅ Automatic SSL
- ✅ Auto-deploy on Git push

---

### 3. Heroku

#### Steps:

1. **Install Heroku CLI:**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Or download from heroku.com
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create App:**
   ```bash
   heroku create devgenie-app
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Open App:**
   ```bash
   heroku open
   ```

**Note:** Heroku no longer offers a free tier, but you can use it for testing.

---

### 4. Docker + VPS

If you have a VPS (like DigitalOcean, Linode, or any other VPS):

#### Steps:

1. **Build Docker Image:**
   ```bash
   docker build -t devgenie .
   ```

2. **Run Container:**
   ```bash
   docker run -d -p 8000:8000 --name devgenie devgenie
   ```

3. **With Nginx (Recommended for production):**
   
   Install Nginx:
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

   Create Nginx configuration file:
   ```bash
   sudo nano /etc/nginx/sites-available/devgenie
   ```

   File content:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/devgenie /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **SSL with Let's Encrypt:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

### 5. DigitalOcean App Platform

#### Steps:

1. **Sign up:**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Create an account

2. **Create App:**
   - Go to "App Platform"
   - Click "Create App"
   - Connect your GitHub repository

3. **Configuration:**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

4. **Deploy:**
   - Click "Create Resources"
   - DigitalOcean will automatically deploy

---

## 📝 Important Notes

### 1. Environment Variables

If you want to set API key as an environment variable (optional):

```bash
# In Railway/Render/Heroku
GOOGLE_API_KEY=your_api_key_here
```

**Note:** In this project, API key is obtained from users, so environment variable is not required.

### 2. Port Configuration

Many platforms get the port from environment variable:

```python
# In api.py (already configured):
import os
port = int(os.getenv("PORT", 8000))
```

### 3. CORS

CORS is currently open for all origins (`allow_origins=["*"]`). For production, it's better to restrict to your domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Only your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. HTTPS

Always use HTTPS for production. Most platforms provide automatic SSL.

---

## 🔧 Troubleshooting

### Issue: App won't deploy

**Solution:**
- Make sure `requirements.txt` is correct
- Check the logs
- Verify Python version is correct (3.11)

### Issue: Port binding error

**Solution:**
- Make sure you're using `$PORT` environment variable
- Or use `0.0.0.0` instead of `localhost`

### Issue: Static files won't load

**Solution:**
- Make sure `static/` folder is in project root
- Check file paths

### Issue: Build fails

**Solution:**
- Check logs in your platform's dashboard
- Verify all dependencies in `requirements.txt`
- Make sure Python 3.11 is specified

---

## 🎯 Final Recommendation

For quick start, I recommend **Railway** or **Render**:
- ✅ Free tier
- ✅ Simple setup
- ✅ Automatic SSL
- ✅ Automatic deployment

After testing, you can migrate to VPS with Docker for more control.

---

## 📞 Support

If you encounter any issues:
- Check the logs in your platform's dashboard
- Review error messages
- Open an issue on GitHub

---

**Happy Deploying! 🚀**
