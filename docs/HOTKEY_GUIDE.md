# 🎹 Hotkey Configuration Guide

This guide covers all keyboard shortcuts and hotkey configuration options in UtterType AI.

## 📋 Default Hotkeys

| Hotkey | Function | Hold/Press | Description |
|--------|----------|------------|-------------|
| `Ctrl+Alt+Q` | Standard Transcription | **Hold** | Voice-to-text without AI formatting |
| `Ctrl+Alt+A` | AI-Enhanced Transcription | **Hold** | Voice-to-text with intelligent AI formatting |
| `Ctrl+Alt+Shift+E` | Email Enhancement | **Press** | Enhances selected text for professional emails |

## 🔧 How Hotkeys Work

### Hold-to-Record Hotkeys (`Ctrl+Alt+Q` and `Ctrl+Alt+A`)

These hotkeys use a **hold-to-record** mechanism:

1. **Press and hold** the hotkey combination
2. **Start speaking** immediately (recording begins)
3. **Continue holding** while you speak
4. **Release the keys** when finished (recording stops)
5. **Text appears** automatically at your cursor

#### Technical Details
- **Global hotkeys** - Work in any application
- **Real-time detection** - Recording starts immediately
- **Key release monitoring** - Stops when any key in the combination is released
- **Debouncing** - Prevents accidental multiple triggers

### Press-to-Trigger Hotkey (`Ctrl+Alt+Shift+E`)

The email enhancement hotkey uses a **press-to-trigger** mechanism:

1. **Select text** in any application first
2. **Press and release** `Ctrl+Alt+Shift+E` quickly
3. **AI processes** the selected text
4. **Enhanced text** replaces the original selection

#### Technical Details
- **2-second debounce** - Prevents rapid re-triggering
- **Background processing** - Runs in separate thread
- **Clipboard operations** - Uses system clipboard for text transfer
- **Cross-platform compatibility** - Works on Windows, macOS, and Linux

## ⚙️ Customizing Hotkeys

### Environment Variable Configuration

Add these variables to your `.env` file to customize hotkeys:

```env
# Standard voice transcription (default: <ctrl>+<alt>+q)
UTTERTYPE_RECORD_HOTKEYS=<ctrl>+<alt>+q

# AI-enhanced voice transcription (default: <ctrl>+<alt>+a)  
UTTERTYPE_AI_HOTKEYS=<ctrl>+<alt>+a

# Email enhancement (default: <ctrl>+<alt>+<shift>+e)
UTTERTYPE_EMAIL_HOTKEY=<ctrl>+<alt>+<shift>+e
```

### Hotkey Format

Use this format for defining custom hotkeys:

```
<modifier1>+<modifier2>+<key>
```

#### Available Modifiers
- `<ctrl>` - Control key
- `<alt>` - Alt key  
- `<shift>` - Shift key
- `<cmd>` - Command key (macOS only)

#### Available Keys
- **Letters**: `a`, `b`, `c`, ... `z`
- **Numbers**: `1`, `2`, `3`, ... `0`
- **Function keys**: `f1`, `f2`, ... `f12`
- **Special keys**: `space`, `tab`, `enter`, `esc`

### Example Custom Configurations

```env
# Use F1 for standard transcription
UTTERTYPE_RECORD_HOTKEYS=f1

# Use Ctrl+Shift+V for AI transcription
UTTERTYPE_AI_HOTKEYS=<ctrl>+<shift>+v

# Use Ctrl+E for email enhancement
UTTERTYPE_EMAIL_HOTKEY=<ctrl>+e

# Use Space for transcription (be careful with this!)
UTTERTYPE_RECORD_HOTKEYS=<space>
```

## 🖥️ Platform-Specific Considerations

### Windows
- **Administrator privileges** may be required for global hotkeys
- **Windows Security** might block hotkey registration
- **Conflicting software** (antivirus, system utilities) may interfere

### macOS
- **Accessibility permissions** required for global hotkeys
- **System Preferences → Security & Privacy → Accessibility**
- **Globe key support** available for compatible keyboards

### Linux
- **X11/Wayland compatibility** varies by distribution
- **Desktop environment** may have conflicting hotkeys
- **sudo privileges** might be needed for global hotkey access

## 🧪 Testing Your Hotkeys

Use the built-in test utility to verify your hotkeys work correctly:

```bash
python test_hotkeys.py
```

This will:
- ✅ Load your hotkey configuration
- ✅ Display current hotkey mappings  
- ✅ Test each hotkey individually
- ✅ Show success/failure status

### Sample Test Output
```
Testing hotkeys:
  Normal recording: <ctrl>+<alt>+q
  AI recording: <ctrl>+<alt>+a  
  Email formatting: <ctrl>+<alt>+<shift>+e

Press Ctrl+Alt+Q to test normal recording...
✅ Normal recording hotkey triggered!

Press Ctrl+Alt+A to test AI recording...
✅ AI recording hotkey triggered!

Press Ctrl+Alt+Shift+E to test email formatting...
✅ Email formatting hotkey triggered!
```

## 🚨 Troubleshooting Hotkeys

### Common Issues

#### ❌ Hotkeys Not Responding
1. **Check for conflicts** with other applications
2. **Verify permissions** (admin/accessibility)
3. **Test with simple combinations** first
4. **Restart the application** after configuration changes

#### ❌ Recording Doesn't Stop
1. **Release ALL keys** in the combination
2. **Check for sticky keys** in system settings
3. **Try pressing Escape** to force stop
4. **Restart the application** if unresponsive

#### ❌ Email Enhancement Not Working
1. **Select text first** before triggering
2. **Wait for debounce period** (2 seconds)
3. **Check clipboard permissions**
4. **Verify OpenAI API connectivity**

### Debugging Steps

1. **Enable verbose logging** by setting environment variable:
   ```env
   UTTERTYPE_DEBUG=1
   ```

2. **Check console output** for error messages

3. **Test individual components**:
   ```bash
   # Test audio devices
   python list_audio_devices.py
   
   # Test hotkeys only  
   python test_hotkeys.py
   ```

4. **Verify configuration** loading:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print(os.getenv('UTTERTYPE_RECORD_HOTKEYS'))
   ```

## 💡 Best Practices

### Choosing Good Hotkeys

1. **Avoid conflicts** with common application shortcuts
2. **Use intuitive combinations** that are easy to remember
3. **Consider ergonomics** - comfortable key positions
4. **Test thoroughly** before committing to a configuration

### Recommended Combinations

#### Conservative (Low Conflict Risk)
```env
UTTERTYPE_RECORD_HOTKEYS=<ctrl>+<alt>+q
UTTERTYPE_AI_HOTKEYS=<ctrl>+<alt>+a
UTTERTYPE_EMAIL_HOTKEY=<ctrl>+<alt>+<shift>+e
```

#### Alternative Options
```env
# Function key based
UTTERTYPE_RECORD_HOTKEYS=f9
UTTERTYPE_AI_HOTKEYS=f10
UTTERTYPE_EMAIL_HOTKEY=f11

# Different modifier combinations
UTTERTYPE_RECORD_HOTKEYS=<ctrl>+<shift>+q
UTTERTYPE_AI_HOTKEYS=<ctrl>+<shift>+a
UTTERTYPE_EMAIL_HOTKEY=<ctrl>+<shift>+e
```

#### Gaming/Streaming Friendly
```env
# Numpad based (keeps main keyboard free)
UTTERTYPE_RECORD_HOTKEYS=<ctrl>+<alt>+num_1
UTTERTYPE_AI_HOTKEYS=<ctrl>+<alt>+num_2
UTTERTYPE_EMAIL_HOTKEY=<ctrl>+<alt>+num_3
```

## 🔮 Advanced Configuration

### Multiple Hotkey Sets

You can define different hotkey sets for different contexts by using multiple `.env` files:

```bash
# Work environment
cp .env .env.work

# Gaming environment  
cp .env .env.gaming

# Switch between configurations
cp .env.work .env  # Activate work hotkeys
cp .env.gaming .env  # Activate gaming hotkeys
```

### Conditional Hotkeys

For advanced users, you can modify `key_listener.py` to implement conditional hotkeys based on:

- **Active application** (e.g., different hotkeys for different apps)
- **Time of day** (e.g., work hours vs. personal time)
- **System state** (e.g., different behavior when on battery)

### Hardware Integration

Consider using:
- **Dedicated macro keyboards** for hotkey activation
- **Foot pedals** for hands-free operation
- **Stream decks** for visual hotkey management
- **Gaming mice** with programmable buttons

---

**Need help?** Check the [main documentation](../README.md) or [create an issue](https://github.com/lukebills/uttertype-ai/issues) for support.
