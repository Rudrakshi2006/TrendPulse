import os
import sys
from dotenv import load_dotenv

def load_and_validate_env():
    """Load environment variables and validate required keys."""
    # Attempt to load from .env file
    load_dotenv()
    
    missing_keys = []
    
    tavily_key = os.getenv("TAVILY_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    groq_model = os.getenv("GROQ_MODEL")
    
    if not tavily_key:
        missing_keys.append("TAVILY_API_KEY")
    if not groq_key:
        missing_keys.append("GROQ_API_KEY")
    if not groq_model:
        missing_keys.append("GROQ_MODEL")
        
    if missing_keys:
        print("\n[!] Configuration Error")
        print("The following required environment variables are missing:")
        for key in missing_keys:
            print(f"  - {key}")
        print("\nPlease configure them in your .env file.")
        print("You can copy .env.example to .env and fill in the values.")
        sys.exit(1)
        
    # Optional parameters with defaults
    tavily_max_results = int(os.getenv("TAVILY_MAX_RESULTS", "5"))
    request_timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    return {
        "tavily_api_key": tavily_key,
        "groq_api_key": groq_key,
        "groq_model": groq_model,
        "tavily_max_results": tavily_max_results,
        "request_timeout": request_timeout
    }
