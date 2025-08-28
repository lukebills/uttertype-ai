"""
Centralized configuration management for UtterType AI.

This module provides validated configuration loading from environment variables
with sensible defaults and clear error messages for misconfiguration.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from pathlib import Path
from logging_config import get_logger

# Auto-load .env file when module is imported
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, environment variables must be set manually
    pass

logger = get_logger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing required values."""
    pass


@dataclass
class UtterTypeConfig:
    """
    Centralized configuration management for UtterType AI.
    
    All configuration values are loaded from environment variables with
    validation and sensible defaults.
    """
    
    # OpenAI API Configuration (Required)
    openai_api_key: str
    openai_base_url: str = "https://api.openai.com/v1"
    openai_chat_model: str = "gpt-4o-mini"
    openai_model_name: str = "whisper-1"
    
    # Hotkey Configuration
    record_hotkeys: str = "<ctrl>+<alt>+q"
    ai_hotkeys: str = "<ctrl>+<alt>+a" 
    email_hotkey: str = "<ctrl>+<alt>+<shift>+e"
    
    # Audio Configuration
    min_transcription_size_ms: int = 1500
    audio_device_index: Optional[int] = None  # None = use default device
    
    # AI Configuration
    ai_temperature: float = 0.3
    email_temperature: float = 0.2
    max_tokens: int = 1000
    
    # Application Configuration
    log_level: str = "INFO"
    vad_enabled: Optional[bool] = None  # None = prompt user on startup
    
    # Advanced Configuration
    debounce_time_sec: float = 2.0
    max_display_text_length: int = 50
    console_refresh_delay: float = 0.1
    
    # Validation flags (populated during validation)
    _validated: bool = field(default=False, init=False)
    _validation_warnings: list = field(default_factory=list, init=False)
    
    @classmethod
    def from_env(cls, validate: bool = True) -> 'UtterTypeConfig':
        """
        Load configuration from environment variables.
        
        Args:
            validate: Whether to validate the configuration
            
        Returns:
            UtterTypeConfig instance
            
        Raises:
            ConfigurationError: If required configuration is missing or invalid
        """
        logger.debug("Loading configuration from environment variables")
        
        # Required configuration
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ConfigurationError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )
        
        # Load all configuration with defaults
        config = cls(
            # OpenAI API
            openai_api_key=api_key,
            openai_base_url=os.getenv('OPENAI_BASE_URL', cls.openai_base_url),
            openai_chat_model=os.getenv('OPENAI_CHAT_MODEL', cls.openai_chat_model),
            openai_model_name=os.getenv('OPENAI_MODEL_NAME', cls.openai_model_name),
            
            # Hotkeys
            record_hotkeys=os.getenv('UTTERTYPE_RECORD_HOTKEYS', cls.record_hotkeys),
            ai_hotkeys=os.getenv('UTTERTYPE_AI_HOTKEYS', cls.ai_hotkeys),
            email_hotkey=os.getenv('UTTERTYPE_EMAIL_HOTKEY', cls.email_hotkey),
            
            # Audio
            min_transcription_size_ms=cls._parse_int(
                'UTTERTYPE_MIN_TRANSCRIPTION_SIZE_MS', 
                cls.min_transcription_size_ms
            ),
            audio_device_index=cls._parse_optional_int('UTTERTYPE_AUDIO_DEVICE_INDEX'),
            
            # AI
            ai_temperature=cls._parse_float('UTTERTYPE_AI_TEMPERATURE', cls.ai_temperature),
            email_temperature=cls._parse_float('UTTERTYPE_EMAIL_TEMPERATURE', cls.email_temperature),
            max_tokens=cls._parse_int('UTTERTYPE_MAX_TOKENS', cls.max_tokens),
            
            # Application
            log_level=os.getenv('UTTERTYPE_LOG_LEVEL', cls.log_level).upper(),
            vad_enabled=cls._parse_optional_bool('UTTERTYPE_VAD_ENABLED'),
            
            # Advanced
            debounce_time_sec=cls._parse_float('UTTERTYPE_DEBOUNCE_TIME_SEC', cls.debounce_time_sec),
            max_display_text_length=cls._parse_int('UTTERTYPE_MAX_DISPLAY_TEXT_LENGTH', cls.max_display_text_length),
            console_refresh_delay=cls._parse_float('UTTERTYPE_CONSOLE_REFRESH_DELAY', cls.console_refresh_delay),
        )
        
        if validate:
            config.validate()
        
        logger.info("Configuration loaded successfully")
        logger.debug(f"Using OpenAI model: {config.openai_chat_model}")
        logger.debug(f"Log level: {config.log_level}")
        
        return config
    
    @staticmethod
    def _parse_int(env_var: str, default: int) -> int:
        """Parse integer from environment variable with validation."""
        value = os.getenv(env_var)
        if value is None:
            return default
        
        try:
            return int(value)
        except ValueError:
            raise ConfigurationError(
                f"Invalid integer value for {env_var}: '{value}'. Must be a number."
            )
    
    @staticmethod
    def _parse_float(env_var: str, default: float) -> float:
        """Parse float from environment variable with validation."""
        value = os.getenv(env_var)
        if value is None:
            return default
        
        try:
            return float(value)
        except ValueError:
            raise ConfigurationError(
                f"Invalid float value for {env_var}: '{value}'. Must be a number."
            )
    
    @staticmethod
    def _parse_optional_int(env_var: str) -> Optional[int]:
        """Parse optional integer from environment variable."""
        value = os.getenv(env_var)
        if value is None:
            return None
        
        try:
            return int(value)
        except ValueError:
            raise ConfigurationError(
                f"Invalid integer value for {env_var}: '{value}'. Must be a number."
            )
    
    @staticmethod
    def _parse_optional_bool(env_var: str) -> Optional[bool]:
        """Parse optional boolean from environment variable."""
        value = os.getenv(env_var)
        if value is None:
            return None
        
        value = value.lower()
        if value in ('true', '1', 'yes', 'on', 'enabled'):
            return True
        elif value in ('false', '0', 'no', 'off', 'disabled'):
            return False
        else:
            raise ConfigurationError(
                f"Invalid boolean value for {env_var}: '{value}'. "
                f"Use: true/false, 1/0, yes/no, on/off, enabled/disabled"
            )
    
    def validate(self) -> None:
        """
        Validate the configuration and set warnings for potential issues.
        
        Raises:
            ConfigurationError: If configuration is critically invalid
        """
        logger.debug("Validating configuration")
        self._validation_warnings.clear()
        
        # Validate OpenAI API key format (basic check)
        if not self.openai_api_key.startswith(('sk-', 'sk-proj-')):
            self._validation_warnings.append(
                "OpenAI API key format appears invalid. Should start with 'sk-' or 'sk-proj-'"
            )
        
        # Validate OpenAI base URL
        if not self.openai_base_url.startswith(('http://', 'https://')):
            raise ConfigurationError(
                f"Invalid OpenAI base URL: {self.openai_base_url}. Must start with http:// or https://"
            )
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level not in valid_log_levels:
            raise ConfigurationError(
                f"Invalid log level: {self.log_level}. Must be one of: {', '.join(valid_log_levels)}"
            )
        
        # Validate temperature ranges
        if not 0.0 <= self.ai_temperature <= 2.0:
            raise ConfigurationError(
                f"AI temperature must be between 0.0 and 2.0, got: {self.ai_temperature}"
            )
        
        if not 0.0 <= self.email_temperature <= 2.0:
            raise ConfigurationError(
                f"Email temperature must be between 0.0 and 2.0, got: {self.email_temperature}"
            )
        
        # Validate positive numeric values
        if self.min_transcription_size_ms <= 0:
            raise ConfigurationError(
                f"Minimum transcription size must be positive, got: {self.min_transcription_size_ms}"
            )
        
        if self.max_tokens <= 0:
            raise ConfigurationError(
                f"Max tokens must be positive, got: {self.max_tokens}"
            )
        
        if self.debounce_time_sec < 0:
            raise ConfigurationError(
                f"Debounce time must be non-negative, got: {self.debounce_time_sec}"
            )
        
        # Validate hotkey formats (basic check)
        for hotkey_name, hotkey_value in [
            ("record_hotkeys", self.record_hotkeys),
            ("ai_hotkeys", self.ai_hotkeys), 
            ("email_hotkey", self.email_hotkey)
        ]:
            if not self._is_valid_hotkey_format(hotkey_value):
                self._validation_warnings.append(
                    f"Hotkey format may be invalid: {hotkey_name}='{hotkey_value}'. "
                    f"Expected format: '<modifier>+<key>' (e.g., '<ctrl>+<alt>+q')"
                )
        
        # Performance warnings
        if self.ai_temperature > 1.0:
            self._validation_warnings.append(
                f"High AI temperature ({self.ai_temperature}) may produce inconsistent results"
            )
        
        if self.max_tokens > 2000:
            self._validation_warnings.append(
                f"High max tokens ({self.max_tokens}) may increase API costs"
            )
        
        # Log warnings
        for warning in self._validation_warnings:
            logger.warning(f"Configuration warning: {warning}")
        
        self._validated = True
        logger.debug("Configuration validation completed")
    
    @staticmethod
    def _is_valid_hotkey_format(hotkey: str) -> bool:
        """Basic validation of hotkey format."""
        if not hotkey:
            return False
        
        # Check for basic format patterns
        valid_patterns = [
            '<ctrl>+<alt>+',
            '<ctrl>+<shift>+',
            '<alt>+<shift>+',
            '<ctrl>+',
            '<alt>+',
            '<shift>+',
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
        ]
        
        hotkey_lower = hotkey.lower()
        return any(pattern in hotkey_lower for pattern in valid_patterns) or hotkey_lower.startswith('f')
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the current configuration (safe for logging)."""
        return {
            'openai_base_url': self.openai_base_url,
            'openai_chat_model': self.openai_chat_model,
            'openai_model_name': self.openai_model_name,
            'record_hotkeys': self.record_hotkeys,
            'ai_hotkeys': self.ai_hotkeys,
            'email_hotkey': self.email_hotkey,
            'min_transcription_size_ms': self.min_transcription_size_ms,
            'audio_device_index': self.audio_device_index,
            'ai_temperature': self.ai_temperature,
            'email_temperature': self.email_temperature,
            'max_tokens': self.max_tokens,
            'log_level': self.log_level,
            'vad_enabled': self.vad_enabled,
            'api_key_set': bool(self.openai_api_key),
            'validation_warnings_count': len(self._validation_warnings),
            'validated': self._validated
        }
    
    def to_env_file(self, file_path: Optional[Path] = None) -> str:
        """
        Generate .env file content from current configuration.
        
        Args:
            file_path: Optional path to write the file to
            
        Returns:
            String content for .env file
        """
        env_content = f"""# UtterType AI Configuration
# Generated on {os.path.basename(__file__)}

# OpenAI API Configuration (Required)
OPENAI_API_KEY={self.openai_api_key}
OPENAI_BASE_URL={self.openai_base_url}
OPENAI_CHAT_MODEL={self.openai_chat_model}
OPENAI_MODEL_NAME={self.openai_model_name}

# Hotkey Configuration
UTTERTYPE_RECORD_HOTKEYS={self.record_hotkeys}
UTTERTYPE_AI_HOTKEYS={self.ai_hotkeys}
UTTERTYPE_EMAIL_HOTKEY={self.email_hotkey}

# Audio Configuration
UTTERTYPE_MIN_TRANSCRIPTION_SIZE_MS={self.min_transcription_size_ms}
{"UTTERTYPE_AUDIO_DEVICE_INDEX=" + str(self.audio_device_index) if self.audio_device_index is not None else "# UTTERTYPE_AUDIO_DEVICE_INDEX=0"}

# AI Configuration
UTTERTYPE_AI_TEMPERATURE={self.ai_temperature}
UTTERTYPE_EMAIL_TEMPERATURE={self.email_temperature}
UTTERTYPE_MAX_TOKENS={self.max_tokens}

# Application Configuration
UTTERTYPE_LOG_LEVEL={self.log_level}
{"UTTERTYPE_VAD_ENABLED=" + str(self.vad_enabled).lower() if self.vad_enabled is not None else "# UTTERTYPE_VAD_ENABLED=true"}

# Advanced Configuration
UTTERTYPE_DEBOUNCE_TIME_SEC={self.debounce_time_sec}
UTTERTYPE_MAX_DISPLAY_TEXT_LENGTH={self.max_display_text_length}
UTTERTYPE_CONSOLE_REFRESH_DELAY={self.console_refresh_delay}
"""
        
        if file_path:
            file_path.write_text(env_content, encoding='utf-8')
            logger.info(f"Configuration written to {file_path}")
        
        return env_content


# Global configuration instance
_config: Optional[UtterTypeConfig] = None


def get_config(reload: bool = False) -> UtterTypeConfig:
    """
    Get the global configuration instance.
    
    Args:
        reload: Whether to reload configuration from environment
        
    Returns:
        UtterTypeConfig instance
    """
    global _config
    
    if _config is None or reload:
        try:
            _config = UtterTypeConfig.from_env()
        except ConfigurationError as e:
            logger.error(f"Configuration error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading configuration: {e}")
            raise ConfigurationError(f"Failed to load configuration: {e}")
    
    return _config


def validate_environment() -> bool:
    """
    Validate the current environment configuration without loading it.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        config = UtterTypeConfig.from_env(validate=True)
        return True
    except ConfigurationError as e:
        logger.error(f"Environment validation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during validation: {e}")
        return False


def reset_config():
    """Reset the global configuration (useful for testing)."""
    global _config
    _config = None
