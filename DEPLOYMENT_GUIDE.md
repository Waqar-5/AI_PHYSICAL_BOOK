# Deploying Your DocBook Backend

Your backend is now configured to use Google's Gemini API and is ready for deployment. Here's how to deploy it:

## Option 1: Deploy to Render (Recommended)

1. **Prepare your repository**:
   - Push your code to a GitHub repository
   - Make sure the `render.yaml` file is in the root directory

2. **Deploy on Render**:
   - Go to https://render.com
   - Connect your GitHub account
   - Create a new Web Service
   - Select your repository
   - Render will automatically detect the `render.yaml` file
   - Add the required environment variables when prompted:
     - `GEMINI_API_KEY`: Your Google Gemini API key
     - `QDRANT_API_KEY`: Your Qdrant API key
     - `QDRANT_URL`: Your Qdrant URL
     - `COHERE_API_KEY`: Your Cohere API key

3. **Access your live backend**:
   - Once deployed, Render will provide you with a URL like `https://your-app-name.onrender.com`

## Option 2: Deploy to Railway

1. **Install Railway CLI** or use the web interface
2. **Create a new project** and connect to your GitHub repo
3. **Set environment variables**:
   ```
   GEMINI_API_KEY=your_actual_gemini_key
   QDRANT_API_KEY=your_qdrant_key
   QDRANT_URL=your_qdrant_url
   COHERE_API_KEY=your_cohere_key
   QDRANT_COLLECTION_NAME=document_chunks
   GEMINI_MODEL=gemini-pro
   ```
4. **Deploy** and get your live URL

## Option 3: Deploy to Heroku

1. **Install Heroku CLI**
2. **Create a new app**:
   ```bash
   heroku create your-app-name
   ```
3. **Set config vars**:
   ```bash
   heroku config:set GEMINI_API_KEY=your_actual_gemini_key
   heroku config:set QDRANT_API_KEY=your_qdrant_key
   heroku config:set QDRANT_URL=your_qdrant_url
   heroku config:set COHERE_API_KEY=your_cohere_key
   heroku config:set QDRANT_COLLECTION_NAME=document_chunks
   heroku config:set GEMINI_MODEL=gemini-pro
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

## Local Testing

Before deploying, you can test locally:

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   uvicorn api:app --reload
   ```

3. **Test the endpoints**:
   - Health check: `GET http://localhost:8000/health`
   - Root endpoint: `GET http://localhost:8000/`
   - Query endpoint: `POST http://localhost:8000/query`

## API Endpoints

Once deployed, your backend will have these endpoints:

- `GET /` - Root endpoint to check if API is running
- `GET /health` - Health check endpoint
- `POST /query` - Main endpoint for querying the Gemini agent

Example query request:
```json
{
  "query": "What is artificial intelligence?",
  "metadata": {
    "session_id": "abc123",
    "user_id": "user456"
  }
}
```

## Frontend Integration

To update your frontend to use the new live backend URL:

1. In your Docusaurus frontend, update the API endpoint in the ChatBot component
2. Change the URL from `http://localhost:8000/query` to your deployed backend URL

Your backend is now ready for deployment! Choose the platform that best suits your needs.