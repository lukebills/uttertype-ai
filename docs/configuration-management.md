# Environment Variable Validation & Configuration Management

## Overview

**Improvement 1.2** introduces a comprehensive configuration management system that validates environment variables, provides sensible defaults, and offers clear error messages for misconfiguration.

## Features

### 🔧 Centralized Configuration

- **Single Source of Truth**: All configuration managed through `config.py`
- **Environment Variable Loading**: Automatic .env file loading with validation
- **Type Safety**: Validated configuration with proper type checking
- **Default Values**: Sensible defaults for all optional settings

### 📋 Configuration Options

#### Required Configuration
- `OPENAI_API_KEY`: Your OpenAI API key (required)

#### OpenAI API Configuration
- `OPENAI_BASE_URL`: API endpoint (default: `https://api.openai.com/v1`)
- `OPENAI_CHAT_MODEL`: GPT model for AI formatting (default: `gpt-4o-mini`)
- `OPENAI_MODEL_NAME`: Whisper model name (default: `whisper-1`)

#### Hotkey Configuration
- `UTTERTYPE_RECORD_HOTKEYS`: Voice recording hotkey (default: `<ctrl>+<alt>+q`)
- `UTTERTYPE_AI_HOTKEYS`: AI formatting hotkey (default: `<ctrl>+<alt>+a`)
- `UTTERTYPE_EMAIL_HOTKEY`: Email formatting hotkey (default: `<ctrl>+<alt>+<shift>+e`)

#### Audio Configuration
- `UTTERTYPE_MIN_TRANSCRIPTION_SIZE_MS`: Minimum speech duration (default: `1500`)
- `UTTERTYPE_AUDIO_DEVICE_INDEX`: Specific audio device (default: system default)

#### AI Configuration
- `UTTERTYPE_AI_TEMPERATURE`: AI creativity level (default: `0.3`)
- `UTTERTYPE_EMAIL_TEMPERATURE`: Email formatting temperature (default: `0.2`)
- `UTTERTYPE_MAX_TOKENS`: Maximum AI response tokens (default: `1000`)

#### Application Configuration
- `UTTERTYPE_LOG_LEVEL`: Logging level (default: `INFO`)
- `UTTERTYPE_VAD_ENABLED`: Voice Activity Detection (default: prompt user)

#### Advanced Configuration
- `UTTERTYPE_DEBOUNCE_TIME_SEC`: Hotkey debounce time (default: `2.0`)
- `UTTERTYPE_MAX_DISPLAY_TEXT_LENGTH`: Console text truncation (default: `50`)
- `UTTERTYPE_CONSOLE_REFRESH_DELAY`: UI refresh rate (default: `0.1`)

### ✅ Validation Features

#### Comprehensive Validation
- **Required Field Checks**: Ensures OPENAI_API_KEY is present
- **Type Validation**: Validates integers, floats, booleans
- **Range Validation**: Ensures values are within acceptable ranges
- **Format Validation**: Basic hotkey and URL format checking

#### Error Handling
- **Clear Error Messages**: Specific guidance for configuration issues
- **Validation Warnings**: Non-critical issues logged as warnings
- **Graceful Degradation**: Application provides helpful error messages

#### Configuration Summary
- **Safe Logging**: Configuration summary without sensitive data
- **Validation Status**: Clear indication of validation results
- **Warning Counts**: Summary of any configuration warnings

## Usage

### Setup Configuration

1. **Copy Template**:
   ```bash
   copy .env.template .env
   ```

2. **Edit Configuration**:
   ```bash
   # Edit .env file with your settings
   OPENAI_API_KEY=your_api_key_here
   UTTERTYPE_LOG_LEVEL=DEBUG
   ```

3. **Validate Configuration**:
   ```bash
   python validate_config.py
   ```

### Configuration Validation Script

The `validate_config.py` script provides comprehensive configuration testing:

```bash
python validate_config.py
```

**Output Example**:
```
🔧 UtterType AI Configuration Validator
==================================================
✅ Found .env file
🔍 Loading configuration...
✅ Configuration loaded successfully!

📋 Configuration Summary:
------------------------------
  openai_chat_model: gpt-4o-mini
  log_level: INFO
  api_key_set: ✅ Set
  validation_warnings_count: ✅ No warnings
  validated: ✅ Yes

🧪 Testing configuration...
✅ Logging system working
✅ OpenAI client configuration valid
🎉 Configuration validation completed!
```

### Programmatic Usage

```python
from config import get_config, ConfigurationError

try:
    config = get_config()
    print(f"Using model: {config.openai_chat_model}")
    print(f"Hotkey: {config.record_hotkeys}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Implementation Details

### Configuration Class

The `UtterTypeConfig` dataclass provides:
- **Type Hints**: All configuration values are properly typed
- **Validation**: Built-in validation with detailed error messages
- **Serialization**: Can export configuration to .env format
- **Singleton Pattern**: Global configuration instance management

### Validation System

#### Multi-level Validation
1. **Parse Level**: Type conversion with error handling
2. **Value Level**: Range and format validation
3. **System Level**: Integration testing capabilities

#### Error Categories
- **ConfigurationError**: Critical configuration issues
- **Validation Warnings**: Non-critical issues that should be reviewed
- **Import Errors**: Missing dependencies or files

### Integration Points

All modules now use the centralized configuration:
- **main.py**: Application startup with configuration validation
- **transcriber.py**: Audio processing with configurable parameters
- **key_listener.py**: Hotkey configuration from settings
- **table_interface.py**: Display configuration and formatting
- **logging_config.py**: Log level configuration

## Benefits

### 🛡️ Reliability
- **Input Validation**: Prevents runtime errors from invalid configuration
- **Type Safety**: Catches configuration type mismatches early
- **Clear Errors**: Helpful error messages for troubleshooting

### 🔧 Maintainability
- **Centralized Management**: All configuration in one place
- **Documentation**: Self-documenting configuration options
- **Extensibility**: Easy to add new configuration options

### 👤 User Experience
- **Easy Setup**: Template files and validation scripts
- **Clear Guidance**: Helpful error messages and examples
- **Flexible**: Supports both .env files and environment variables

### 🧪 Testing
- **Configuration Validation**: Dedicated testing script
- **Environment Isolation**: Test configurations without affecting main setup
- **Validation Reporting**: Comprehensive validation results

## Migration from Previous Version

The new configuration system is **backward compatible**:

1. **Existing .env files**: Continue to work without changes
2. **Environment Variables**: Still supported for deployment scenarios
3. **Default Values**: Maintain previous behavior when no configuration is specified

## Files Added/Modified

### New Files
- `config.py`: Centralized configuration management
- `validate_config.py`: Configuration validation utility
- `.env.template`: Comprehensive configuration template

### Modified Files
- `main.py`: Updated to use centralized configuration
- `transcriber.py`: Configuration-driven audio processing
- `key_listener.py`: Hotkey configuration from settings
- `table_interface.py`: Display configuration integration
- `.env.example`: Updated with all configuration options

## Next Steps

This configuration system provides the foundation for:
- **Dynamic Configuration**: Runtime configuration updates
- **Configuration Profiles**: Multiple environment configurations
- **Advanced Validation**: Custom validation rules
- **Configuration UI**: Graphical configuration management

The centralized configuration management significantly improves the reliability, maintainability, and user experience of UtterType AI.
