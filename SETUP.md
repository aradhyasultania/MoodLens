# MoodLens Setup Guide

## Quick Start (5 minutes)

### 1. Prerequisites

Check you have Python 3.9+:
```bash
python3 --version
```

### 2. Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/moodlens.git
cd moodlens

# Create virtual environment
python3 -m venv moodlens-env

# Activate virtual environment
source moodlens-env/bin/activate  # macOS/Linux
# OR
moodlens-env\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Hugging Face Transformers (AI models)
- PyTorch (deep learning)
- OpenCV (computer vision)
- NumPy, SciPy (data analysis)
- librosa (audio processing)

### 4. Run Application

```bash
python moodlens_simplified.py
```

You should see:
```
🧠 Starting MoodLens Simplified...
==================================================
✨ Guided Emotional Wellness Companion
📱 Web interface: http://localhost:5001
🔍 Health check: http://localhost:5001/health
==================================================
```

### 5. Open in Browser

Navigate to: **http://localhost:5001**

---

## Troubleshooting

### Port Already in Use

If port 5001 is occupied:
```bash
# Find process using port 5001
lsof -i :5001

# Kill process (replace PID with actual process ID)
kill -9 <PID>
```

### Module Not Found Errors

Ensure virtual environment is activated:
```bash
source moodlens-env/bin/activate  # macOS/Linux
```

Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Camera/Microphone Access

- **Chrome**: Settings → Privacy → Site Settings → Camera/Microphone
- **Firefox**: Preferences → Privacy & Security → Permissions
- **Safari**: Preferences → Websites → Camera/Microphone

### Model Download Issues

First run downloads AI models (1-2 GB). Ensure:
- Stable internet connection
- Sufficient disk space
- No firewall blocking Hugging Face

---

## Testing

Run test suite to verify installation:
```bash
python test_system.py
```

Expected output:
```
✅ Anxious: 100.0% confidence
✅ Sad: 100.0% confidence
✅ Happy: 100.0% confidence
✅ Overwhelmed: 95.8% confidence
✅ ALL TESTS PASSED!
```

---

## Optional: GPU Acceleration

For faster processing, install CUDA-enabled PyTorch:

```bash
# Check if you have NVIDIA GPU
nvidia-smi

# Install CUDA PyTorch (example for CUDA 11.8)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

## Development Mode

For development with auto-reload:

```bash
export FLASK_ENV=development  # macOS/Linux
set FLASK_ENV=development     # Windows

python moodlens_simplified.py
```

---

## Production Deployment

For production, use a WSGI server:

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5001 moodlens_simplified:app
```

---

## Support

- 📧 Email: support@moodlens.example
- 🐛 Issues: https://github.com/yourusername/moodlens/issues
- 💬 Discussions: https://github.com/yourusername/moodlens/discussions

---

**Ready to use MoodLens!** 🎉

