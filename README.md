# UtterType AI

A real-time voice transcription tool with AI-powered text formatting and email grammar correction.

## Features

### Core Functionality
- **Real-time voice transcription** using OpenAI's Whisper API
- **Voice Activity Detection (VAD)** - Optional feature to only record when speech is detected
- **AI-powered text formatting** based on context (emails, chat messages, etc.)
- **Professional email formatting** with grammar and spelling correction
- **Australian English** spelling and conventions

### Keyboard Shortcuts
- **Primary transcription hotkey** - Configurable via key_listener module
- **AI formatting toggle** - Enable/disable AI formatting for transcriptions
- **Ctrl+Alt+Shift+E** - Email formatting shortcut for selected text

## Requirements

- Python 3.8+
- OpenAI API access
- Required Python packages (see installation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd uttertype-ai
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your configuration:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_CHAT_MODEL=gpt-4o-mini-2024-07-18
```

## Usage

### Starting the Application
```bash
python main.py
```

Upon startup, you'll be prompted to choose whether to use Voice Activity Detection (VAD):
- **Yes**: Only records when speech is detected (recommended for most users)
- **No**: Records continuously (useful in noisy environments)

### Voice Transcription
1. Use the configured hotkey to start/stop voice recording
2. Speak clearly into your microphone
3. The transcribed text will be automatically pasted at your cursor location
4. Toggle AI formatting on/off using the formatting hotkey

### Email Formatting Feature
The email formatting feature allows you to improve any selected text for professional email communication:

1. **Select text** you want to format in any application (Word, Outlook, browser, etc.)
2. **Press Ctrl+Alt+Shift+E**
3. The selected text will be automatically:
   - Grammar and spelling corrected
   - Formatted for professional email communication
   - Converted to Australian English spelling
   - Replaced in-place with the improved version

#### Email Formatting Examples

**Before:**
```
hi john thanks for you're email about the meeting tommorow i think we should discus the budget and also talk about the new project timeline let me know if you need anything else
```

**After:**
```
Hi John,

Thank you for your email about the meeting tomorrow. I think we should discuss the budget and also talk about the new project timeline.

Please let me know if you need anything else.
```

### AI Text Formatting
The AI formatting feature automatically detects context and applies appropriate formatting:
- **Emails**: Adds proper greetings, paragraphs, and professional structure
- **Chat messages**: Maintains casual tone with minimal editing
- **Other text**: Applies basic formatting and grammar correction

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_BASE_URL` - OpenAI API base URL (default: https://api.openai.com/v1)
- `OPENAI_CHAT_MODEL` - Model to use for text formatting (default: gpt-4o-mini-2024-07-18)

### Customisation
- Hotkeys can be configured in the `key_listener.py` module
- AI prompts can be modified in the `format_with_context()` and `format_for_email()` functions
- Temperature settings can be adjusted for different formatting behaviours

## File Structure

```
uttertype-ai/
├── main.py                 # Main application entry point
├── transcriber.py          # Whisper API transcription handling
├── key_listener.py         # Keyboard shortcut management
├── table_interface.py      # Console output formatting
├── utils.py               # Utility functions
├── .env                   # Environment configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **No transcription appearing**
   - Check your microphone permissions
   - Verify OpenAI API key is correct
   - Ensure you're using the correct hotkey

2. **Email formatting not working**
   - Make sure text is selected before pressing Ctrl+Alt+Shift+E
   - Check that the application has permission to access clipboard
   - Verify OpenAI API is accessible

3. **Poor transcription quality**
   - Ensure you're speaking clearly and at normal volume
   - Check microphone quality and positioning
   - Try adjusting VAD settings

### Performance Tips
- Use VAD mode for better battery life on laptops
- Lower temperature settings (0.1-0.3) for more consistent formatting
- Higher temperature settings (0.5-0.8) for more creative text generation

## Dependencies

- `asyncio` - Asynchronous programming
- `pynput` - Keyboard and mouse input handling
- `openai` - OpenAI API client
- `pyautogui` - GUI automation
- `pyperclip` - Clipboard operations
- `tkinter` - GUI dialogs
- `python-dotenv` - Environment variable management

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and feature requests, please [create an issue](link-to-issues) in the repository.
