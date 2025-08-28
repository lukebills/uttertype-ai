"""
Centralized logging configuration for UtterType AI.

This module provides a unified logging setup that can be used across all modules
to replace print statements and provide structured logging with configurable levels.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional


class UtterTypeLogger:
    """Custom logger class for UtterType AI with enhanced functionality."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.setup_logging()
            self._initialized = True
    
    def setup_logging(self, log_level: Optional[str] = None, log_file: Optional[Path] = None):
        """
        Setup centralized logging configuration.
        
        Args:
            log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Custom log file path
        """
        # Get log level from environment or use provided value
        if log_level is None:
            log_level = os.getenv('UTTERTYPE_LOG_LEVEL', 'INFO').upper()
        
        # Validate log level
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            log_level = 'INFO'
        
        # Setup log file path
        if log_file is None:
            log_dir = Path.home() / '.uttertype'
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / 'uttertype.log'
        
        # Clear any existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            '%(levelname)s - %(name)s - %(message)s'
        )
        
        # Setup handlers
        handlers = []
        
        # File handler - always enabled for persistent logging
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)  # File gets all messages
            file_handler.setFormatter(detailed_formatter)
            handlers.append(file_handler)
        except (PermissionError, OSError) as e:
            # If we can't write to the log file, just use console
            print(f"Warning: Could not create log file {log_file}: {e}")
        
        # Console handler - respects log level setting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level))
        console_handler.setFormatter(console_formatter)
        handlers.append(console_handler)
        
        # Configure root logger
        logging.basicConfig(
            level=logging.DEBUG,  # Root level - handlers filter appropriately
            handlers=handlers,
            force=True  # Override any existing configuration
        )
        
        # Set levels for third-party libraries to reduce noise
        logging.getLogger('openai').setLevel(logging.WARNING)
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        
        # Log the initialization
        logger = logging.getLogger(__name__)
        logger.info(f"UtterType AI logging initialized - Level: {log_level}, File: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the specified module.
    
    Args:
        name: Usually __name__ from the calling module
        
    Returns:
        Configured logger instance
    """
    # Ensure logging is initialized
    UtterTypeLogger()
    
    # Return logger for the module
    return logging.getLogger(name)


def set_log_level(level: str):
    """
    Change the log level at runtime.
    
    Args:
        level: New log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    level = level.upper()
    if level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise ValueError(f"Invalid log level: {level}")
    
    # Update console handler level
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
            handler.setLevel(getattr(logging, level))
    
    logger = get_logger(__name__)
    logger.info(f"Log level changed to {level}")


def log_function_call(func):
    """
    Decorator to log function calls with arguments (for debugging).
    
    Usage:
        @log_function_call
        def my_function(arg1, arg2):
            pass
    """
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with error: {e}", exc_info=True)
            raise
    return wrapper


def log_performance(func):
    """
    Decorator to log function performance timing.
    
    Usage:
        @log_performance
        def slow_function():
            pass
    """
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"{func.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{func.__name__} failed after {duration:.3f}s: {e}")
            raise
    return wrapper


# Initialize logging when module is imported
UtterTypeLogger()
