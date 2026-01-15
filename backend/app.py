# This file is for Hugging Face Spaces compatibility
# The main application is in api.py
# This allows Hugging Face to recognize the application

import os
from api import app

# Hugging Face Spaces typically runs on port 7860
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)