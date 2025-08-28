# 📚 UtterType AI User Guide

A comprehensive guide to using UtterType AI for professional voice transcription and text enhancement.

## 🎯 What is UtterType AI?

UtterType AI is a powerful voice transcription tool that converts your speech into text with intelligent AI-powered formatting. It's designed for professionals who need fast, accurate voice-to-text conversion with context-aware enhancements.

### Key Benefits
- **Faster than typing** - Speak at 150+ WPM vs 40 WPM typing
- **Hands-free operation** - Work while walking, standing, or multitasking
- **Professional output** - AI formats text appropriately for context
- **Universal compatibility** - Works in any application
- **Cost-effective** - Minimal API costs for maximum productivity

## 🚀 Getting Started

### First-Time Setup

1. **Install and configure** UtterType AI (see [Installation Guide](../README.md#installation))
2. **Test your microphone** using `python list_audio_devices.py`
3. **Verify hotkeys work** using `python test_hotkeys.py`
4. **Choose VAD setting** when prompted on first run

### Your First Transcription

1. **Open any text editor** (Notepad, Word, email, etc.)
2. **Position your cursor** where you want text to appear
3. **Hold `Ctrl+Alt+Q`** and speak clearly
4. **Release keys** when finished
5. **Watch text appear** automatically!

## 🎤 Voice Transcription Modes

### Standard Transcription (`Ctrl+Alt+Q`)

**Best for:**
- Quick notes and drafts
- Raw content creation
- Casual communications
- When you want minimal AI processing

**How it works:**
1. Hold `Ctrl+Alt+Q`
2. Speak your content
3. Release keys to stop recording
4. Text appears with basic formatting

**Example:**
```
Input (speech): "call john tomorrow about the meeting"
Output: "Call John tomorrow about the meeting."
```

### AI-Enhanced Transcription (`Ctrl+Alt+A`)

**Best for:**
- Professional communications
- Emails and documents
- Content that needs structure
- When you want intelligent formatting

**How it works:**
1. Hold `Ctrl+Alt+A`
2. Speak your content
3. Release keys to stop recording
4. AI analyzes context and applies formatting
5. Enhanced text appears

**Example:**
```
Input (speech): "hi sarah wanted to follow up on our meeting yesterday can we schedule another one next week"

Output: "Hi Sarah,

I wanted to follow up on our meeting yesterday. Can we schedule another one next week?

Best regards,"
```

## 📧 Email Enhancement Feature

Transform any existing text into professional email format.

### How to Use
1. **Select text** in any application
2. **Press `Ctrl+Alt+Shift+E`**
3. **Wait 1-3 seconds** for processing
4. **Text is automatically replaced** with enhanced version

### Before & After Examples

**Original:**
```
need help with the report due friday not sure about the data analysis section can you review it
```

**Enhanced:**
```
Hi,

I need help with the report that's due Friday. I'm not sure about the data analysis section.

Could you please review it when you have a chance?

Thanks for your help.

Best regards,
```

## 🛠️ Advanced Features

### Voice Activity Detection (VAD)

**With VAD (Recommended):**
- Only records when you're speaking
- Ignores background noise
- Better battery life
- More accurate transcriptions

**Without VAD:**
- Records continuously while hotkey is held
- Better for very quiet speech
- Works in noisy environments
- May capture background sounds

### Real-Time Cost Tracking

The console interface shows:
- Each transcription in real-time
- Processing time for each request
- Cumulative API costs
- Total usage statistics

### Context-Aware Processing

The AI automatically detects:
- **Email content** → Professional formatting
- **Chat messages** → Casual tone preservation
- **Documents** → Structured formatting
- **Technical content** → Precise language

## 💡 Best Practices

### Speaking Techniques

#### For Better Transcription
- **Speak clearly** at normal pace
- **Use natural pauses** between sentences
- **Avoid filler words** (um, ah, like)
- **State punctuation** for complex formatting ("comma", "period", "new paragraph")

#### Microphone Positioning
- **6-12 inches** from your mouth
- **Avoid breathing directly** into microphone
- **Minimize background noise**
- **Use a quality headset** for best results

### Content Structure

#### For Emails
Start with context cues:
```
"Email to John: Hi John, I wanted to follow up..."
```

#### For Documents
Use structural cues:
```
"New paragraph. The quarterly results show..."
"Bullet point: Increased customer satisfaction"
```

#### For Technical Content
Be explicit about formatting:
```
"Code block: function getName() return name"
"Heading: Database Configuration"
```

## 🔧 Troubleshooting Common Issues

### No Text Appearing

**Possible Causes:**
- Microphone not working
- Wrong hotkey combination
- Application doesn't accept paste
- API key issues

**Solutions:**
1. Test microphone with other apps
2. Verify hotkeys with test script
3. Try in a simple text editor (Notepad)
4. Check OpenAI API key and credits

### Poor Transcription Quality

**Possible Causes:**
- Background noise
- Speaking too fast/slow
- Poor microphone quality
- Incorrect audio device

**Solutions:**
1. Find a quieter environment
2. Speak at normal conversational pace
3. Use a better microphone/headset
4. Check audio device selection

### AI Enhancement Not Working

**Possible Causes:**
- API connectivity issues
- Wrong model configuration
- Insufficient API credits
- Rate limiting

**Solutions:**
1. Check internet connection
2. Verify OpenAI configuration
3. Check API usage in OpenAI dashboard
4. Wait and retry if rate limited

### Hotkeys Not Responding

**Possible Causes:**
- Application conflicts
- Insufficient permissions
- Hardware issues
- Configuration errors

**Solutions:**
1. Close conflicting applications
2. Run as administrator (Windows)
3. Test with different hotkey combinations
4. Verify configuration file

## 📊 Productivity Tips

### Workflow Integration

#### Morning Routine
1. Start UtterType AI
2. Voice-dictate your daily priorities
3. AI-enhance for professional emails
4. Share with team

#### Meeting Follow-ups
1. Use standard transcription during meetings
2. Voice-dictate action items after
3. AI-enhance for distribution
4. Send professional follow-up emails

#### Content Creation
1. Voice-dictate initial draft
2. Use AI enhancement for structure
3. Further edit as needed
4. Publish or distribute

### Efficiency Multipliers

#### Combine with Other Tools
- **Task management** - Voice-add tasks to your system
- **Calendar apps** - Dictate meeting notes
- **CRM systems** - Voice-update client records
- **Documentation** - Rapidly create technical docs

#### Keyboard Shortcuts Stack
1. `Ctrl+Alt+A` - Voice dictate
2. `Ctrl+Alt+Shift+E` - Enhance text
3. `Ctrl+A` - Select all
4. `Ctrl+C` - Copy to clipboard
5. Paste into final destination

## 📈 Performance Optimization

### Speed Settings

#### For Maximum Speed
```env
OPENAI_CHAT_MODEL=gpt-3.5-turbo  # Fastest model
```

#### For Best Quality
```env
OPENAI_CHAT_MODEL=gpt-4o  # Highest quality
```

#### Balanced (Recommended)
```env
OPENAI_CHAT_MODEL=gpt-4o-mini  # Good speed + quality
```

### Cost Management

#### Monitor Usage
- Check console for cost tracking
- Review OpenAI dashboard monthly
- Set usage alerts in OpenAI account

#### Optimize Costs
- Use cheaper models for simple tasks
- Batch similar content together
- Use standard transcription when AI isn't needed

## 🎨 Customization Guide

### Personal Preferences

#### Adjust AI Tone
Modify prompts in `main.py` for:
- More formal output
- Casual, friendly tone
- Industry-specific language
- Regional variations

#### Custom Hotkeys
Change hotkeys in `.env`:
```env
UTTERTYPE_RECORD_HOTKEYS=<ctrl>+<alt>+q
UTTERTYPE_AI_HOTKEYS=<ctrl>+<alt>+a
UTTERTYPE_EMAIL_HOTKEY=<ctrl>+<alt>+<shift>+e
```

#### Audio Settings
Configure in code:
- Different sample rates
- Audio device selection
- VAD sensitivity
- Buffer sizes

## 🔮 Advanced Use Cases

### Content Creation
- **Blog posts** - Voice-dictate, AI-structure
- **Documentation** - Technical writing with voice
- **Marketing copy** - Creative content with AI polish
- **Reports** - Data-driven content with professional formatting

### Business Communication
- **Client emails** - Professional, polished communication
- **Team updates** - Quick, structured information sharing
- **Meeting minutes** - Real-time transcription and formatting
- **Proposals** - Structured business documents

### Personal Productivity
- **Journaling** - Daily reflection with voice
- **Note-taking** - Lectures, meetings, thoughts
- **Task management** - Voice-to-task creation
- **Learning** - Voice notes for study materials

## 🎓 Learning Resources

### Practice Exercises

#### Week 1: Basic Transcription
- Practice with simple sentences
- Focus on clear speech
- Test different applications

#### Week 2: AI Enhancement
- Experiment with different content types
- Compare standard vs AI transcription
- Practice email enhancement

#### Week 3: Advanced Features
- Customize hotkeys and settings
- Integrate into daily workflows
- Optimize for your use cases

#### Week 4: Mastery
- Develop personal voice patterns
- Create custom prompts
- Build efficient workflows

### Community Resources
- GitHub Issues for support
- User discussions and tips
- Feature requests and feedback
- Community-contributed improvements

---

**Ready to become a voice transcription expert?** Start with the [Quick Start guide](../README.md#quick-start) and gradually explore advanced features as you become comfortable with the basics.

**Need help?** Check the [troubleshooting section](#troubleshooting-common-issues) or [create an issue](https://github.com/lukebills/uttertype-ai/issues) for support.
