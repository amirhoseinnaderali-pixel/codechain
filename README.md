# DevGenie - AI Code Assistant

A powerful AI-powered code generation assistant built with FastAPI and Google Gemini AI. Generate production-ready code with multiple AI models working in sequence.

## 🚀 Features

- ✅ **Multi-Model AI Chain**: Uses multiple Google Gemini models in sequence for better code quality
- ✅ **Multiple Modes**: Fast, Advance, Full Power, Optimized, Aggressive, Balanced, and Strongest modes
- ✅ **Session-Based API Keys**: Secure API key management with session storage
- ✅ **Beautiful UI**: Modern, responsive interface with dark/light theme support
- ✅ **Real-time Code Generation**: Get instant code suggestions and improvements
- ✅ **Conversation History**: Save and manage your coding conversations

## 📋 Prerequisites

- Python 3.11 or higher
- Google AI Studio API Key ([Get one here](https://aistudio.google.com/app/apikey))
- pip package manager

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/devgenie.git
cd devgenie
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
python api.py
```

The server will start on `http://localhost:8000`

## 🎯 Usage

1. Open your browser and navigate to `http://localhost:8000`
2. Enter your Google AI Studio API key when prompted
3. Start generating code by describing what you need
4. Choose from different modes (Fast, Advance, Full Power, etc.)
5. Get production-ready code instantly!

## 🚀 Deployment

### Quick Deploy Options

#### 1. Railway (Recommended - Easiest)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. ✅ Done! Railway automatically deploys your app

#### 2. Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"

#### 3. Docker

```bash
# Build the image
docker build -t devgenie .

# Run the container
docker run -d -p 8000:8000 --name devgenie devgenie
```

For detailed deployment instructions, see [DEPLOY.md](DEPLOY.md)

## 📁 Project Structure

```
devgenie/
├── api.py              # FastAPI backend server
├── agents.py           # AI code generation logic with multi-model chains
├── requirements.txt    # Python dependencies
├── static/
│   └── index.html      # Frontend UI (single-page application)
├── Dockerfile          # Docker configuration
├── Procfile            # Process file for Heroku/Railway
├── nixpacks.toml       # Railway build configuration
└── README.md           # This file
```

## 🔧 Configuration

### API Key Management

- API keys are stored in `sessionStorage` (not `localStorage`)
- Keys are automatically cleared when the browser tab is closed
- Each user must enter their own API key
- API keys are never stored on the server

### Environment Variables (Optional)

You can set a default API key as an environment variable:

```bash
export GOOGLE_API_KEY=your_api_key_here
```

**Note**: The app works without this - users can enter their own API keys.

### Port Configuration

The app automatically uses the `PORT` environment variable if available, otherwise defaults to `8000`.

## 🎨 Modes Explained

- **Fast**: Quick responses with minimal models (3-4 models)
- **Advance**: Balanced approach with more models (6 models)
- **Full Power**: Maximum quality with all models (30+ models)
- **Optimized**: Smart model selection for best results (12 models)
- **Aggressive**: Fast but thorough (9 models)
- **Balanced**: Good balance between speed and quality (15 models)
- **Strongest**: Maximum quality with all available models (30+ models)

## 🔒 Security

- ✅ API keys are stored client-side only (sessionStorage)
- ✅ API keys are never stored on the server
- ✅ HTTPS recommended for production
- ✅ CORS configured for security
- ✅ Session-based storage (cleared on tab close)

## 🐛 Troubleshooting

### Server won't start

**Solution:**
- Make sure Python 3.11+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use

### API key errors

**Solution:**
- Make sure your API key is valid
- Check that you have API access enabled in Google AI Studio
- Verify the API key format (should start with "AIza")

### Static files not loading

**Solution:**
- Ensure the `static/` folder exists in the project root
- Check file paths in `api.py`
- Verify static files are included in deployment

## 📝 Development

### Running in development mode

```bash
python api.py
```

The server runs with auto-reload enabled.

### Making changes

1. Make your changes
2. The server will auto-reload (if running with `python api.py`)
3. Test your changes in the browser

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Google Gemini AI](https://ai.google.dev/)
- UI inspired by modern chat interfaces

## 📞 Support

If you encounter any issues:
1. Check the [DEPLOY.md](DEPLOY.md) for deployment help
2. Review the error logs
3. Open an issue on GitHub

---

**Made with ❤️ for developers who want to code faster and better**
