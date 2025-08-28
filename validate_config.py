#!/usr/bin/env python3
"""
Configuration validation utility for UtterType AI.

This script validates your configuration and helps troubleshoot issues.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main validation function."""
    print("🔧 UtterType AI Configuration Validator")
    print("=" * 50)
    
    try:
        # Load environment variables first
        from dotenv import load_dotenv
        load_dotenv()
        
        from config import get_config, ConfigurationError, validate_environment
        from logging_config import get_logger
        
        logger = get_logger(__name__)
        
        # Check if .env file exists
        env_file = Path('.env')
        if not env_file.exists():
            print("\n⚠️  WARNING: No .env file found")
            print("   Create one by copying .env.template or .env.example")
            print("   Example: copy .env.template .env")
        else:
            print("\n✅ Found .env file")
        
        # Load and validate configuration
        print("\n🔍 Loading configuration...")
        config = get_config()
        
        print("✅ Configuration loaded successfully!")
        
        # Display configuration summary
        print("\n📋 Configuration Summary:")
        print("-" * 30)
        summary = config.get_summary()
        for key, value in summary.items():
            if key == 'api_key_set':
                print(f"  {key}: {'✅ Set' if value else '❌ Not Set'}")
            elif key == 'validation_warnings_count':
                if value > 0:
                    print(f"  {key}: ⚠️ {value} warnings")
                else:
                    print(f"  {key}: ✅ No warnings")
            elif key == 'validated':
                print(f"  {key}: {'✅ Yes' if value else '❌ No'}")
            else:
                print(f"  {key}: {value}")
        
        # Show warnings if any
        if config._validation_warnings:
            print(f"\n⚠️  Configuration Warnings ({len(config._validation_warnings)}):")
            print("-" * 40)
            for i, warning in enumerate(config._validation_warnings, 1):
                print(f"  {i}. {warning}")
        
        # Test configuration
        print("\n🧪 Testing configuration...")
        
        # Test logging
        try:
            logger.info("Configuration validation test log entry")
            print("✅ Logging system working")
        except Exception as e:
            print(f"❌ Logging system error: {e}")
        
        # Test OpenAI configuration (basic)
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=config.openai_api_key,
                base_url=config.openai_base_url
            )
            print("✅ OpenAI client configuration valid")
        except Exception as e:
            print(f"❌ OpenAI client configuration error: {e}")
        
        print("\n🎉 Configuration validation completed!")
        print("\nTo start UtterType AI, run: python main.py")
        
    except ConfigurationError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your .env file exists")
        print("2. Verify OPENAI_API_KEY is set correctly")
        print("3. Review configuration values for typos")
        print("4. Run 'python -c \"from config import UtterTypeConfig; print(UtterTypeConfig().to_env_file())\"' for a template")
        sys.exit(1)
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check you're in the correct directory")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print("\n🔧 Please check the logs for more details")
        sys.exit(1)


if __name__ == "__main__":
    main()
