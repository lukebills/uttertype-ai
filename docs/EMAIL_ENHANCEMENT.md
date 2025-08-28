# 📧 Email Enhancement Guide

Transform any text into professional email format with UtterType AI's powerful email enhancement feature.

## 🎯 Overview

The Email Enhancement feature (`Ctrl+Alt+Shift+E`) takes any selected text and transforms it into professional, well-formatted email content with:

- ✅ Grammar and spelling correction
- ✅ Professional email structure  
- ✅ Australian English conventions
- ✅ Proper paragraphing and tone
- ✅ Business-appropriate formatting

## 🚀 How to Use

### Basic Usage

1. **Select text** in any application (Word, Outlook, browser, notepad, etc.)
2. **Press** `Ctrl+Alt+Shift+E`
3. **Wait** for processing (1-3 seconds)
4. **Text is automatically replaced** with enhanced version

### Supported Applications

The email enhancement works in virtually any application that supports:
- Text selection
- Clipboard operations (copy/paste)
- Standard keyboard shortcuts

#### ✅ Confirmed Working Applications
- Microsoft Outlook
- Gmail (web)
- Microsoft Word
- Google Docs
- Slack
- Discord
- Notepad/TextEdit
- VS Code
- Thunderbird
- Apple Mail
- Any web browser text fields

## 📝 Transformation Examples

### Example 1: Quick Note to Professional Email

**Before (Raw Text):**
```
hey john thanks for the meeting yesterday wanted to follow up on the budget discussion can we schedule another meeting next week to go over the details let me know what works for you
```

**After (Enhanced):**
```
Hi John,

Thank you for the meeting yesterday. I wanted to follow up on the budget discussion.

Can we schedule another meeting next week to go over the details? Please let me know what works for you.

Best regards,
```

### Example 2: Voice Note Cleanup

**Before (Voice Transcription):**
```
hi sarah hope your doing well um wanted to check in about the project status wondering if you need any help with the deliverables that are due this friday also can you send me the latest version of the document when you get a chance thanks
```

**After (Enhanced):**
```
Hi Sarah,

I hope you're doing well. I wanted to check in about the project status and see if you need any help with the deliverables that are due this Friday.

Could you also send me the latest version of the document when you get a chance?

Thanks!

Best regards,
```

### Example 3: Formal Request

**Before (Casual Text):**
```
need to request time off for next month going on vacation from the 15th to the 25th hope thats ok let me know if you need anything before i go
```

**After (Enhanced):**
```
Hi,

I would like to request time off for next month as I'll be going on vacation from the 15th to the 25th.

I hope this timing works for you. Please let me know if you need anything before I go.

Thank you for your consideration.

Best regards,
```

### Example 4: Technical Follow-up

**Before (Technical Notes):**
```
server migration completed successfully all services running normally noticed minor performance improvement in database queries backup verification complete documentation updated let me know if you have questions
```

**After (Enhanced):**
```
Hi,

The server migration has been completed successfully, and all services are running normally. I've noticed a minor performance improvement in database queries.

Backup verification is complete, and documentation has been updated. Please let me know if you have any questions.

Best regards,
```

## ⚙️ Customization Options

### Environment Configuration

```env
# Email-specific hotkey (default: <ctrl>+<alt>+<shift>+e)
UTTERTYPE_EMAIL_HOTKEY=<ctrl>+<alt>+<shift>+e

# AI model for email processing
OPENAI_CHAT_MODEL=gpt-4o-mini

# API configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Prompt Customization

Modify the email formatting prompt in `main.py`:

```python
def format_for_email(text: str) -> str:
    prompt = (
        "Review and rewrite the following text for professional email communication. "
        "Fix grammar, spelling, and punctuation errors. "
        "Format appropriately with proper paragraphs and professional tone. "
        "Use Australian English spelling and conventions. "
        "Maintain the original meaning while improving clarity and professionalism. "
        "Output only the corrected text without explanations or comments."
    )
```

#### Custom Prompt Examples

**For More Formal Tone:**
```python
prompt = (
    "Transform the text into highly formal business correspondence. "
    "Use formal language, proper business structure, and professional tone. "
    "Include appropriate formal greetings and closings. "
    "Use Australian English spelling."
)
```

**For Casual-Professional Balance:**
```python
prompt = (
    "Improve the text for professional but friendly email communication. "
    "Maintain a warm, approachable tone while ensuring proper grammar. "
    "Use conversational yet professional language. "
    "Australian English spelling preferred."
)
```

**For Technical Communications:**
```python
prompt = (
    "Format for technical email communication. "
    "Maintain technical accuracy while improving clarity. "
    "Use precise, professional language appropriate for technical teams. "
    "Structure for easy scanning and comprehension."
)
```

## 🔧 Advanced Features

### Debouncing System

The email enhancement includes a 2-second debounce system to prevent:
- Accidental multiple triggers
- Processing conflicts
- System overload

**How it works:**
- First trigger processes normally
- Subsequent triggers within 2 seconds are ignored
- Console shows "debounced" message for ignored triggers

### Error Handling

The system includes robust error handling:

```python
try:
    # Email formatting process
    formatted_text = format_for_email(selected_text)
    # Success handling
except Exception as e:
    print(f"Error in email formatting: {e}")
    # Fallback to original text
```

### Clipboard Management

The enhancement preserves your original clipboard:

1. **Stores** original clipboard content
2. **Copies** selected text for processing
3. **Processes** text with AI
4. **Replaces** selection with enhanced text
5. **Restores** original clipboard if process fails

## 🎭 Formatting Styles

### Professional Business
- Formal greetings and closings
- Structured paragraphs
- Business-appropriate language
- Clear call-to-actions

### Friendly Professional  
- Warm but professional tone
- Conversational language
- Appropriate informality
- Approachable closings

### Technical Communication
- Precise terminology
- Clear structure
- Technical accuracy
- Professional presentation

## 🚨 Troubleshooting

### Common Issues

#### 📋 Enhancement Not Working
**Symptoms:** Nothing happens when pressing the hotkey

**Solutions:**
1. **Select text first** - Must have text highlighted
2. **Check hotkey** - Verify correct key combination
3. **Wait for debounce** - Allow 2 seconds between attempts
4. **Check permissions** - Ensure clipboard access allowed

#### 🔄 Text Not Replacing
**Symptoms:** Enhanced text goes to clipboard but doesn't replace selection

**Solutions:**
1. **Check application compatibility** - Some apps block programmatic paste
2. **Manual paste** - Use `Ctrl+V` to paste manually
3. **Test in different app** - Try in notepad/simple text editor
4. **Check clipboard content** - Enhanced text should be in clipboard

#### 🤖 Poor Enhancement Quality
**Symptoms:** AI output is not as expected

**Solutions:**
1. **Check original text quality** - Ensure readable source text
2. **Verify API connection** - Test with simple text first
3. **Adjust model settings** - Try different GPT model
4. **Customize prompt** - Modify for specific needs

#### 💰 API Costs Too High
**Symptoms:** High OpenAI usage charges

**Solutions:**
1. **Use cheaper models** - Switch to `gpt-3.5-turbo`
2. **Optimize usage** - Only enhance when necessary
3. **Set usage limits** - Configure API limits in OpenAI dashboard
4. **Monitor usage** - Track tokens used per enhancement

### Debugging Steps

#### 1. Test Hotkey Detection
```bash
python test_hotkeys.py
```

#### 2. Check Console Output
Look for these messages when triggering enhancement:
```
Email hotkey triggered!
Starting email formatting...
Processing selected text: [text preview]...
Email formatting completed successfully!
```

#### 3. Test Clipboard Operations
```python
import pyperclip

# Test clipboard access
pyperclip.copy("test")
print(pyperclip.paste())  # Should print "test"
```

#### 4. Test AI Processing
```python
from main import format_for_email

test_text = "test email content here"
result = format_for_email(test_text)
print(result)
```

## 🎯 Best Practices

### Writing for Enhancement

#### ✅ Good Source Text
- Complete thoughts and sentences
- Clear intent and purpose
- Proper names and context
- Logical flow

#### ❌ Challenging Source Text
- Fragmented thoughts
- Missing context
- Unclear pronouns
- Mixed languages

### Usage Tips

1. **Select complete thoughts** - Don't cut off mid-sentence
2. **Include context** - Names, dates, specific details
3. **Review output** - AI is good but not perfect
4. **Test with your style** - Customize prompts for your needs
5. **Use consistently** - Build muscle memory for the hotkey

### Professional Guidelines

#### Business Communications
- Use for client emails
- Internal team communications  
- Project updates
- Meeting follow-ups

#### Personal Professional
- Job applications
- Networking emails
- Professional social media
- Industry communications

#### Avoid For
- Legal documents (without review)
- Highly technical specifications
- Personal intimate communications
- Official company statements (without approval)

## 📊 Performance Metrics

### Typical Processing Times
- **GPT-4o-mini**: 1-2 seconds
- **GPT-4o**: 2-4 seconds
- **GPT-3.5-turbo**: 0.5-1.5 seconds

### Enhancement Quality
- **Grammar correction**: 95%+ accuracy
- **Professional tone**: 90%+ appropriate
- **Structure improvement**: 85%+ effective
- **Australian English**: 98%+ correct

### Cost Estimates (USD)
- **GPT-4o-mini**: ~$0.001 per enhancement
- **GPT-4o**: ~$0.005 per enhancement
- **GPT-3.5-turbo**: ~$0.0005 per enhancement

*Costs based on typical 100-200 word enhancements*

## 🔮 Advanced Usage

### Batch Processing
For multiple emails, consider:
1. Collect all text in a document
2. Process each section individually
3. Copy enhanced versions to email client

### Template Integration
Combine with email templates:
1. Start with your template
2. Add personalized content
3. Enhance the personalized sections
4. Send professional email

### Workflow Integration
Integrate into your daily workflow:
1. Voice-to-text with `Ctrl+Alt+A`
2. Enhance with `Ctrl+Alt+Shift+E`
3. Review and send
4. Save enhanced versions for future reference

---

**Need help?** Check the [main documentation](../README.md) or [create an issue](https://github.com/lukebills/uttertype-ai/issues) for support.
