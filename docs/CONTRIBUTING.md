# 🤝 Contributing to UtterType AI

Thank you for your interest in contributing to UtterType AI! This guide will help you get started with contributing to the project.

## 🎯 How to Contribute

There are many ways to contribute to UtterType AI:

- 🐛 **Report bugs** and issues
- 💡 **Suggest new features** or improvements
- 📝 **Improve documentation**
- 🔧 **Submit code fixes** and enhancements
- 🧪 **Test new features** and provide feedback
- 🌍 **Add language support** and localization
- 📚 **Create tutorials** and guides

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork" button
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/uttertype-ai.git
   cd uttertype-ai
   ```

3. **Create development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy example .env file
   cp .env.example .env
   
   # Add your OpenAI API key
   # Edit .env file with your credentials
   ```

5. **Test the setup**
   ```bash
   # Test hotkeys
   python test_hotkeys.py
   
   # Test audio devices
   python list_audio_devices.py
   
   # Run the main application
   python main.py
   ```

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   # Run existing tests
   python -m pytest tests/
   
   # Test functionality manually
   python test_hotkeys.py
   python main.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to GitHub and create a PR
   - Describe your changes clearly
   - Link any related issues

## 📝 Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

#### Code Formatting
```python
# Use descriptive variable names
transcription_text = whisper_api.transcribe(audio_data)

# Function names should be descriptive
def format_text_for_email(input_text: str) -> str:
    """Format text for professional email communication."""
    pass

# Class names use PascalCase
class AudioTranscriber:
    """Handles audio transcription using Whisper API."""
    pass

# Constants use UPPER_CASE
DEFAULT_SAMPLE_RATE = 16000
MAX_RECORDING_DURATION = 300
```

#### Documentation
```python
def transcribe_audio(audio_data: bytes, language: str = "en") -> str:
    """
    Transcribe audio data using OpenAI Whisper API.
    
    Args:
        audio_data: Raw audio bytes in WAV format
        language: Language code for transcription (default: "en")
        
    Returns:
        Transcribed text string
        
    Raises:
        TranscriptionError: If API call fails
        ValidationError: If audio data is invalid
    """
    pass
```

#### Error Handling
```python
# Use specific exception types
try:
    transcription = whisper_api.transcribe(audio)
except OpenAIError as e:
    logger.error(f"OpenAI API error: {e}")
    raise TranscriptionError("Failed to transcribe audio") from e
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### File Organization

```
uttertype-ai/
├── src/                    # Source code
│   ├── __init__.py
│   ├── transcriber.py      # Audio transcription logic
│   ├── key_listener.py     # Hotkey management
│   ├── ai_formatter.py     # AI text formatting
│   └── utils.py           # Utility functions
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_transcriber.py
│   ├── test_key_listener.py
│   └── test_ai_formatter.py
├── docs/                   # Documentation
├── examples/               # Example scripts
└── requirements.txt        # Dependencies
```

## 🧪 Testing Guidelines

### Test Categories

#### Unit Tests
```python
import unittest
from src.transcriber import AudioTranscriber

class TestAudioTranscriber(unittest.TestCase):
    def setUp(self):
        self.transcriber = AudioTranscriber()
    
    def test_audio_format_validation(self):
        """Test audio format validation."""
        valid_audio = b"valid_wav_data"
        self.assertTrue(self.transcriber.validate_audio(valid_audio))
        
    def test_transcription_with_valid_audio(self):
        """Test transcription with valid audio data."""
        # Mock API response
        with patch('openai.Audio.transcribe') as mock_transcribe:
            mock_transcribe.return_value = {"text": "Hello world"}
            result = self.transcriber.transcribe(b"audio_data")
            self.assertEqual(result, "Hello world")
```

#### Integration Tests
```python
def test_full_transcription_workflow():
    """Test complete transcription workflow."""
    # Test with real audio file
    with open("tests/fixtures/test_audio.wav", "rb") as f:
        audio_data = f.read()
    
    transcriber = AudioTranscriber()
    result = transcriber.transcribe(audio_data)
    
    assert isinstance(result, str)
    assert len(result) > 0
```

#### Manual Testing Checklist

Before submitting a PR, test these scenarios:

- [ ] **Basic transcription** works with `Ctrl+Alt+Q`
- [ ] **AI enhancement** works with `Ctrl+Alt+A`
- [ ] **Email formatting** works with `Ctrl+Alt+Shift+E`
- [ ] **Hotkeys work** in different applications
- [ ] **VAD mode** functions correctly
- [ ] **Error handling** works with invalid inputs
- [ ] **Cost tracking** displays correctly
- [ ] **Configuration changes** take effect

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Test with latest version** from main branch
3. **Reproduce the issue** consistently
4. **Gather system information**

### Bug Report Template

```markdown
## Bug Description
Clear description of what went wrong.

## Steps to Reproduce
1. Open UtterType AI
2. Press Ctrl+Alt+Q
3. Speak into microphone
4. Release keys
5. No text appears

## Expected Behavior
Text should appear at cursor location.

## Actual Behavior
Nothing happens, no text is inserted.

## Environment
- OS: Windows 11
- Python: 3.9.7
- UtterType AI: v1.2.0
- OpenAI Model: gpt-4o-mini

## Console Output
```
Starting transcription...
Error: API key not found
```

## Additional Context
This started happening after updating Windows.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
## Feature Summary
Brief description of the proposed feature.

## Problem Statement
What problem does this solve? Who would benefit?

## Proposed Solution
Detailed description of how it should work.

## Alternative Solutions
Other ways this could be implemented.

## Use Cases
Specific examples of how this would be used.

## Implementation Notes
Technical considerations or suggestions.
```

## 📚 Documentation Contributions

### Documentation Standards

- **Clear headings** and structure
- **Code examples** for technical content
- **Screenshots** for UI elements
- **Cross-references** to related sections
- **Keep it updated** with code changes

### Areas Needing Documentation

- **API reference** for developers
- **Troubleshooting guides** for common issues
- **Advanced configuration** examples
- **Integration tutorials** with other tools
- **Video tutorials** for visual learners

## 🔧 Code Contribution Guidelines

### Pull Request Process

1. **Reference an issue** - Link to existing issue or create one
2. **Single purpose** - One feature/fix per PR
3. **Clear description** - Explain what and why
4. **Tests included** - Add/update tests as needed
5. **Documentation updated** - Update relevant docs

### PR Template

```markdown
## Description
Brief description of changes made.

## Motivation
Why are these changes needed?

## Changes Made
- Added feature X
- Fixed bug Y
- Updated documentation Z

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No breaking changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated

## Related Issues
Fixes #123
```

### Code Review Process

1. **Automated checks** run first
2. **Maintainer review** for code quality
3. **Community feedback** welcome
4. **Iterative improvements** based on feedback
5. **Final approval** and merge

## 🌍 Internationalization

### Adding Language Support

1. **Create language files**
   ```python
   # locales/en.py
   MESSAGES = {
       "recording_started": "Recording started...",
       "recording_stopped": "Recording stopped...",
       "error_no_api_key": "OpenAI API key not found"
   }
   
   # locales/es.py
   MESSAGES = {
       "recording_started": "Grabación iniciada...",
       "recording_stopped": "Grabación detenida...",
       "error_no_api_key": "Clave API de OpenAI no encontrada"
   }
   ```

2. **Update AI prompts**
   ```python
   def get_email_prompt(language="en"):
       prompts = {
           "en": "Format for professional English email...",
           "es": "Formatear para email profesional en español...",
           "fr": "Formater pour email professionnel français..."
       }
       return prompts.get(language, prompts["en"])
   ```

3. **Test with different languages**
   - Voice recognition accuracy
   - AI formatting quality
   - UI text display

## 📊 Performance Contributions

### Areas for Optimization

- **Audio processing** efficiency
- **API call** optimization
- **Memory usage** reduction
- **Startup time** improvement
- **Battery usage** on laptops

### Benchmarking

```python
import time
import psutil

def benchmark_transcription():
    """Benchmark transcription performance."""
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss
    
    # Run transcription
    result = transcriber.transcribe(audio_data)
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss
    
    print(f"Time: {end_time - start_time:.2f}s")
    print(f"Memory: {(end_memory - start_memory) / 1024 / 1024:.2f}MB")
    
    return result
```

## 🎓 Learning Resources

### Useful Technologies

- **Python async/await** - For audio processing
- **OpenAI API** - For transcription and AI
- **PyAudio** - For audio input/output
- **pynput** - For global hotkeys
- **tkinter** - For GUI dialogs

### Recommended Reading

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [PyAudio Documentation](https://pypi.org/project/PyAudio/)
- [Python Asyncio Guide](https://docs.python.org/3/library/asyncio.html)
- [Audio Programming with Python](https://realpython.com/playing-and-recording-sound-python/)

## 🏆 Recognition

### Contributors

We recognize contributors in several ways:

- **Contributors list** in README
- **Release notes** mention significant contributions
- **Social media** recognition for major features
- **Maintainer status** for consistent contributors

### Contribution Types

We value all types of contributions:

- 💻 **Code** - Features, fixes, optimizations
- 📝 **Documentation** - Guides, examples, translations
- 🐛 **Testing** - Bug reports, QA, validation
- 💡 **Ideas** - Feature requests, design suggestions
- 🎨 **Design** - UI/UX improvements, graphics
- 📢 **Community** - Support, tutorials, advocacy

## 📞 Getting Help

### Communication Channels

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions and community chat
- **Email** - [maintainer@uttertype.ai](mailto:maintainer@uttertype.ai)
- **Discord** - [Community Discord Server](https://discord.gg/uttertype)

### Questions Welcome

Don't hesitate to ask:

- ❓ "How do I implement feature X?"
- 🤔 "What's the best way to test Y?"
- 🚀 "Can you review my approach for Z?"
- 📖 "Where should I add documentation for A?"

---

**Thank you for contributing to UtterType AI!** 🙏

Every contribution, no matter how small, helps make voice transcription more accessible and powerful for everyone.
