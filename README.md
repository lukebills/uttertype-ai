# UtterType AI

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

**UtterType AI** is a powerful real-time voice transcription tool that transforms speech into text with intelligent AI-powered formatting. Perfect for professionals who need quick, accurate voice-to-text conversion with context-aware formatting for emails, documents, and chat messages.

## ✨ Key Features

### 🎤 Voice Transcription
- **Real-time speech-to-text** using OpenAI's Whisper API
- **Hold-to-record functionality** with configurable hotkeys
- **Voice Activity Detection (VAD)** - Only records when you're actually speaking
- **Instant text insertion** at your cursor location
- **High accuracy** transcription in multiple languages

### 🤖 AI-Powered Text Enhancement
- **Context-aware formatting** - Automatically detects and formats emails, chat messages, and documents
- **Professional email enhancement** with grammar correction and proper structure
- **Australian English** spelling and conventions
- **Customizable AI models** and formatting prompts

### ⌨️ Smart Keyboard Shortcuts
| Shortcut | Function | Description |
|----------|----------|-------------|
| `Ctrl+Alt+Q` | Standard Transcription | Voice-to-text without AI formatting |
| `Ctrl+Alt+A` | AI-Enhanced Transcription | Voice-to-text with intelligent formatting |
| `Ctrl+Alt+Shift+E` | Email Enhancement | Improves selected text for professional emails |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Microphone access

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lukebills/uttertype-ai.git
   cd uttertype-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your environment:**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_CHAT_MODEL=gpt-4o-mini-2024-07-18
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

### First Time Setup
- On startup, choose whether to use Voice Activity Detection (VAD)
- **Yes (Recommended)**: Only records when speech is detected
- **No**: Records continuously (useful in noisy environments)

## 📖 How to Use

### Voice Transcription

#### Standard Transcription (`Ctrl+Alt+Q`)
1. Hold down `Ctrl+Alt+Q`
2. Speak clearly into your microphone
3. Release the keys when finished
4. Text appears instantly at your cursor location

#### AI-Enhanced Transcription (`Ctrl+Alt+A`)
1. Hold down `Ctrl+Alt+A`
2. Speak your message
3. Release the keys
4. AI automatically formats the text based on context:
   - **Emails**: Adds proper structure, greetings, and professional tone
   - **Chat messages**: Keeps casual tone with light editing
   - **Documents**: Applies appropriate formatting and punctuation

### Email Enhancement (`Ctrl+Alt+Shift+E`)

Transform any text into professional email format:

1. **Select text** in any application (Word, Outlook, browser, etc.)
2. **Press** `Ctrl+Alt+Shift+E`
3. **Watch** as your text is automatically enhanced with:
   - Grammar and spelling correction
   - Professional email structure
   - Australian English conventions
   - Proper paragraphing and formatting

#### Example Transformation

**Before (Raw text):**
```
hi john thanks for you're email about the meeting tommorow i think we should discus the budget and also talk about the new project timeline let me know if you need anything else
```

**After (AI Enhanced):**
```
Hi John,

Thank you for your email about the meeting tomorrow. I think we should discuss the budget and also talk about the new project timeline.

Please let me know if you need anything else.

Best regards,
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_BASE_URL` | OpenAI API endpoint | `https://api.openai.com/v1` |
| `OPENAI_CHAT_MODEL` | AI model for formatting | `gpt-4o` |
| `UTTERTYPE_RECORD_HOTKEYS` | Standard transcription hotkey | `<ctrl>+<alt>+q` |
| `UTTERTYPE_AI_HOTKEYS` | AI transcription hotkey | `<ctrl>+<alt>+a` |
| `UTTERTYPE_EMAIL_HOTKEY` | Email enhancement hotkey | `<ctrl>+<alt>+<shift>+e` |
| `UTTERTYPE_MIN_TRANSCRIPTION_SIZE_MS` | Minimum recording duration | `1500` |

### Customization Options

#### Hotkey Configuration
Modify hotkeys in your `.env` file:
```env
UTTERTYPE_RECORD_HOTKEYS=<ctrl>+<alt>+q
UTTERTYPE_AI_HOTKEYS=<ctrl>+<alt>+a
UTTERTYPE_EMAIL_HOTKEY=<ctrl>+<alt>+<shift>+e
```

#### AI Model Settings
Adjust AI behavior by changing the model and temperature:
- **Higher temperature** (0.5-0.8): More creative, varied output
- **Lower temperature** (0.1-0.3): More consistent, predictable formatting

## 🏗️ Architecture

### Project Structure
```
uttertype-ai/
├── 📄 main.py                 # Application entry point and AI formatting
├── 🎤 transcriber.py          # Whisper API integration and audio processing
├── ⌨️ key_listener.py         # Global hotkey management
├── 🖥️ table_interface.py      # Console UI and cost tracking
├── 🛠️ utils.py               # Utility functions and clipboard operations
├── 🧪 test_hotkeys.py        # Hotkey testing utility
├── 🔊 list_audio_devices.py  # Audio device discovery
├── ⚙️ .env                   # Environment configuration
├── 📦 requirements.txt       # Python dependencies
└── 📚 docs/                  # Documentation files
```

### Key Components

#### 🎤 Audio Processing Pipeline
1. **Microphone Input** → PyAudio captures audio at 16kHz
2. **Voice Activity Detection** → WebRTC VAD filters silence
3. **Whisper API** → OpenAI transcribes speech to text
4. **AI Enhancement** → GPT models format and improve text
5. **Output** → Text inserted at cursor location

#### ⌨️ Hotkey System
- **Global hotkeys** work across all applications
- **Hold-to-record** mechanism for intuitive operation
- **Key release detection** for precise recording control
- **Debouncing** prevents accidental multiple triggers

## 🔧 Troubleshooting

### Common Issues

#### 🚫 No Transcription Appearing
- **Check microphone permissions** in system settings
- **Verify OpenAI API key** is correct and has credits
- **Test audio devices** using `python list_audio_devices.py`
- **Confirm hotkey configuration** using `python test_hotkeys.py`

#### 📧 Email Formatting Not Working
- **Select text first** before pressing the hotkey
- **Check clipboard permissions** for the application
- **Verify OpenAI API connectivity**
- **Wait for debounce period** (2 seconds between triggers)

#### 🎯 Poor Transcription Quality
- **Speak clearly** at normal pace and volume
- **Use a quality microphone** positioned 6-12 inches away
- **Minimize background noise**
- **Try adjusting VAD sensitivity** (modes 0-3)

#### ⌨️ Hotkeys Not Working
- **Run as administrator** on Windows if needed
- **Check for conflicting hotkeys** with other applications
- **Test individual hotkeys** using the test script
- **Verify Python has accessibility permissions** on macOS

### Performance Optimization

#### 🔋 Battery Life
- **Use VAD mode** to reduce continuous processing
- **Lower the minimum transcription duration**
- **Close unnecessary applications** during use

#### 🚀 Speed Improvements
- **Use faster OpenAI models** (e.g., gpt-4o-mini)
- **Reduce AI temperature** for quicker responses
- **Optimize network connection** for API calls

## 🧪 Testing & Utilities

### Test Your Setup
```bash
# Test hotkey detection
python test_hotkeys.py

# List available audio devices  
python list_audio_devices.py
```

### Development Tools
- **Hotkey tester** - Verify keyboard shortcuts work correctly
- **Audio device lister** - Find the best microphone for your setup
- **Console interface** - Real-time transcription monitoring with cost tracking

## 📦 Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `openai` | Whisper and GPT API access | Latest |
| `PyAudio` | Audio input/output | Latest |
| `pynput` | Global hotkey detection | Latest |
| `pyautogui` | GUI automation | Latest |
| `pyperclip` | Clipboard operations | Latest |
| `python-dotenv` | Environment variables | Latest |
| `rich` | Console formatting | Latest |
| `webrtcvad` | Voice activity detection | Latest |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Documentation

- 📖 **[User Guide](docs/USER_GUIDE.md)** - Detailed usage instructions
- ⚙️ **[Hotkey Configuration](docs/HOTKEY_GUIDE.md)** - Complete hotkey reference
- 🤖 **[AI Enhancement Guide](docs/AI_ENHANCEMENT.md)** - AI formatting features
- 📧 **[Email Enhancement](docs/EMAIL_ENHANCEMENT.md)** - Professional email formatting
- 🐛 **[Issues](https://github.com/lukebills/uttertype-ai/issues)** - Report bugs or request features
- 💬 **[Discussions](https://github.com/lukebills/uttertype-ai/discussions)** - Community support

## 🙏 Acknowledgments

- **OpenAI** for Whisper and GPT APIs
- **WebRTC** for voice activity detection
- **Python community** for excellent libraries
- **Contributors** who help improve UtterType AI

---

**Made with ❤️ for productivity enthusiasts who want to speak their thoughts into existence.**
