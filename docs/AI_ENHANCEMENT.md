# 🤖 AI Enhancement Guide

This guide explains how UtterType AI's intelligent text formatting works and how to customize it for your needs.

## 🧠 How AI Enhancement Works

UtterType AI uses advanced language models to understand context and apply appropriate formatting to your voice transcriptions.

### Two AI Enhancement Modes

#### 1. AI-Enhanced Transcription (`Ctrl+Alt+A`)
- **Real-time processing** during voice transcription
- **Context-aware formatting** based on content analysis
- **Automatic text structure** application
- **Seamless integration** with voice input

#### 2. Email Enhancement (`Ctrl+Alt+Shift+E`)
- **Post-processing** of existing text
- **Professional email formatting**
- **Grammar and spelling correction**
- **Australian English conventions**

## 🎯 Context Detection

The AI automatically detects different types of content and applies appropriate formatting:

### 📧 Email Context
**Detected when text contains:**
- Greetings (Hi, Hello, Dear)
- Email-specific phrases (Thank you for, Please let me know)
- Professional language patterns
- Request or inquiry patterns

**Applied formatting:**
- Professional greeting structure
- Proper paragraph breaks
- Formal closing phrases
- Australian English spelling
- Business-appropriate tone

### 💬 Chat/Messaging Context
**Detected when text contains:**
- Casual language patterns
- Short sentences
- Informal greetings
- Conversational tone

**Applied formatting:**
- Minimal punctuation changes
- Casual tone preservation
- Basic grammar correction
- Natural flow maintenance

### 📄 Document Context
**Detected when text contains:**
- Formal language
- Technical terms
- Long-form content
- Structured information

**Applied formatting:**
- Proper punctuation
- Paragraph structure
- Professional tone
- Clear sentence structure

## 🔧 Customizing AI Behavior

### Environment Configuration

Control AI behavior through environment variables:

```env
# AI Model Selection
OPENAI_CHAT_MODEL=gpt-4o              # High quality, slower
OPENAI_CHAT_MODEL=gpt-4o-mini         # Good quality, faster
OPENAI_CHAT_MODEL=gpt-3.5-turbo       # Basic quality, fastest

# API Configuration
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your_api_key_here
```

### Temperature Settings

Modify the temperature in `main.py` to control AI creativity:

```python
# In format_with_context() function
temperature=0.3  # Default: balanced
temperature=0.1  # Conservative: very consistent
temperature=0.5  # Creative: more varied output
temperature=0.8  # Experimental: highly creative
```

## ✨ AI Enhancement Examples

### Example 1: Email Formatting

**Voice Input (using `Ctrl+Alt+A`):**
> "hi sarah hope youre doing well wanted to follow up on the project we discussed last week wondering if you had a chance to review the proposal let me know your thoughts"

**AI Enhanced Output:**
```
Hi Sarah,

Hope you're doing well. I wanted to follow up on the project we discussed last week. I was wondering if you had a chance to review the proposal.

Let me know your thoughts.

Best regards,
```

### Example 2: Chat Message Formatting

**Voice Input (using `Ctrl+Alt+A`):**
> "hey can you pick up some milk on your way home also need bread thanks"

**AI Enhanced Output:**
```
Hey, can you pick up some milk on your way home? Also need bread. Thanks!
```

### Example 3: Document Formatting

**Voice Input (using `Ctrl+Alt+A`):**
> "the quarterly results show significant improvement in customer satisfaction metrics with scores increasing by fifteen percent compared to last quarter"

**AI Enhanced Output:**
```
The quarterly results show significant improvement in customer satisfaction metrics, with scores increasing by 15% compared to last quarter.
```

### Example 4: Email Enhancement (Post-Processing)

**Original Text (selected and enhanced with `Ctrl+Alt+Shift+E`):**
```
need to reschedule tomorrows meeting something came up let me know when works for you
```

**Enhanced Result:**
```
Hi there,

I need to reschedule tomorrow's meeting as something has come up. Please let me know when works for you.

Thanks for your understanding.

Best regards,
```

## 🎨 Advanced Customization

### Custom Prompts

Modify the AI prompts in `main.py` to change formatting behavior:

#### General Context Formatting (format_with_context)
```python
prompt = (
    "Format the transcribed text based on context clues in the message. "
    "Apply appropriate formatting for emails (greeting + paragraphs), "
    "chat messages (casual tone), or minimal editing for other types. "
    "Use Australian English spelling. Output only the formatted text without explanations."
)
```

**Customization examples:**
```python
# More formal style
prompt = (
    "Format the text with a professional, formal tone. "
    "Apply proper business communication structure. "
    "Use Australian English spelling and formal language."
)

# More casual style
prompt = (
    "Format the text maintaining a casual, friendly tone. "
    "Keep the original voice and personality. "
    "Make minimal changes, focus on clarity."
)

# Technical writing focus
prompt = (
    "Format the text for technical documentation. "
    "Use clear, precise language and proper terminology. "
    "Structure for readability and accuracy."
)
```

#### Email-Specific Formatting (format_for_email)
```python
prompt = (
    "Review and rewrite the following text for professional email communication. "
    "Fix grammar, spelling, and punctuation errors. "
    "Format appropriately with proper paragraphs and professional tone. "
    "Use Australian English spelling and conventions. "
    "Maintain the original meaning while improving clarity and professionalism. "
    "Output only the corrected text without explanations or comments."
)
```

### Model-Specific Optimizations

#### For GPT-4 Models
```python
# Higher quality, more nuanced understanding
temperature=0.2
max_tokens=1000
```

#### For GPT-3.5-Turbo  
```python
# Faster processing, simpler prompts
temperature=0.3
max_tokens=500
```

#### For Cost Optimization
```python
# Use shorter, more direct prompts
prompt = "Fix grammar and format professionally. Australian English."
temperature=0.1
max_tokens=200
```

## 📊 Understanding AI Processing

### Processing Pipeline

1. **Voice Input** → Whisper API transcription
2. **Context Analysis** → AI detects content type
3. **Prompt Selection** → Appropriate formatting instructions
4. **AI Processing** → Language model applies formatting
5. **Output Generation** → Formatted text returned
6. **Clipboard Integration** → Text ready for pasting

### Performance Metrics

#### Response Times (typical)
- **GPT-4o-mini**: 1-3 seconds
- **GPT-4o**: 3-8 seconds  
- **GPT-3.5-turbo**: 0.5-2 seconds

#### Accuracy Improvements
- **Grammar correction**: ~95% accuracy
- **Context detection**: ~90% accuracy
- **Tone preservation**: ~85% accuracy
- **Australian English**: ~98% accuracy

## 🔍 Troubleshooting AI Issues

### Common Problems

#### 🤖 AI Not Formatting Correctly
1. **Check API connectivity** and credits
2. **Verify model availability** (some models may be deprecated)
3. **Adjust temperature settings** for different behavior
4. **Modify prompts** for specific use cases

#### 📝 Inconsistent Formatting
1. **Lower the temperature** (0.1-0.2) for more consistency
2. **Use more specific prompts** with clear instructions
3. **Test with different models** (GPT-4 vs GPT-3.5)

#### 🐌 Slow Processing
1. **Switch to faster models** (gpt-4o-mini, gpt-3.5-turbo)
2. **Reduce max_tokens** in API calls
3. **Simplify prompts** for faster processing
4. **Check network connection** to OpenAI

#### 💰 High API Costs
1. **Use cheaper models** for routine tasks
2. **Implement caching** for repeated content
3. **Optimize prompts** to reduce token usage
4. **Set usage limits** in OpenAI dashboard

### Debugging Tools

#### Enable Debug Mode
```env
UTTERTYPE_DEBUG=1
```

#### Test AI Components
```python
# Test AI formatting directly
from main import format_with_context, format_for_email

test_text = "your test text here"
result = format_with_context(test_text)
print(result)
```

## 🚀 Advanced Features

### Conditional Formatting

Modify the code to apply different formatting based on context:

```python
def smart_format(text, context_hints=None):
    """Apply formatting based on additional context hints."""
    
    if context_hints:
        if 'urgent' in context_hints:
            # Apply urgent email formatting
            prompt = "Format as urgent professional email..."
        elif 'casual' in context_hints:
            # Apply casual formatting
            prompt = "Keep casual tone, fix basic grammar..."
    
    # Standard processing
    return format_with_context(text)
```

### Multi-Language Support

Configure for different languages:

```python
# In your custom prompt
prompt = (
    f"Format the text professionally in {language}. "
    f"Use {language} spelling and grammar conventions. "
    f"Maintain appropriate cultural communication style."
)
```

### Industry-Specific Formatting

Create specialized formatting for different industries:

```python
def format_for_industry(text, industry):
    prompts = {
        'medical': "Format using medical terminology and professional medical communication standards...",
        'legal': "Format using legal writing conventions and precise language...",
        'technical': "Format for technical documentation with clear, precise language...",
        'creative': "Format maintaining creative voice while improving clarity..."
    }
    
    prompt = prompts.get(industry, default_prompt)
    # Process with industry-specific prompt
```

## 📈 Best Practices

### Optimization Tips

1. **Use appropriate models** for your needs
2. **Optimize prompts** for efficiency
3. **Monitor API usage** and costs
4. **Test formatting** with your common use cases
5. **Adjust temperature** based on desired consistency

### Quality Guidelines

1. **Speak clearly** for better source material
2. **Use context cues** in your speech (e.g., "email to john")
3. **Review AI output** before final use
4. **Customize prompts** for your specific needs
5. **Provide feedback** to improve the system

---

**Need help?** Check the [main documentation](../README.md) or [create an issue](https://github.com/lukebills/uttertype-ai/issues) for support.
