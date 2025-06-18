import streamlit as st
import os
import sys
import subprocess
import threading
import time
import requests
from utils.ai_client import AzureOpenAIClient

# Configure page
st.set_page_config(
    page_title="AI TaskMaster",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS for dark mode
def load_css():
    with open("static/dark_mode.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Check if dark mode is enabled
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Initialize AI client
@st.cache_resource
def get_ai_client():
    return AzureOpenAIClient()

# Start FastAPI backend if not running
def start_backend():
    if "backend_started" not in st.session_state:
        try:
            # Check if backend is already running
            response = requests.get("http://localhost:8000/health", timeout=2)
            st.session_state.backend_started = True
        except:
            # Start backend
            def run_backend():
                subprocess.run([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"])
            
            thread = threading.Thread(target=run_backend, daemon=True)
            thread.start()
            time.sleep(3)  # Give backend time to start
            st.session_state.backend_started = True

def render_readme():
    """Render comprehensive README with local setup instructions"""
    st.title("📚 AI TaskMaster - Local Setup Guide")
    
    st.markdown("""
    ## 🎯 Project Overview
    
    AI TaskMaster is a comprehensive learning platform that combines practical event management with AI-powered challenges. 
    The application demonstrates real-world software development skills including:
    
    - **Full-stack development** with Streamlit frontend and FastAPI backend
    - **Database operations** with SQLAlchemy ORM and SQLite
    - **AI integration** using Azure OpenAI's o3-mini model
    - **API design** with proper validation and error handling
    - **Modern Python practices** with async/await and type hints
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 🛠️ Local Development Setup
    
    ### Prerequisites
    
    Before running this project locally, ensure you have:
    
    1. **Python 3.8 or higher** installed on your system
    2. **Git** for cloning the repository
    3. **Azure OpenAI API access** with the following credentials:
       - API Key
       - Endpoint URL
       - Deployment name (o3-mini model)
    
    ### Step 1: Clone and Setup
    
    ```bash
    # Clone the repository
    git clone <your-repository-url>
    cd ai-taskmaster
    
    # Create a virtual environment (recommended)
    python -m venv venv
    
    # Activate virtual environment
    # On Windows:
    venv\\Scripts\\activate
    # On macOS/Linux:
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```
    
    ### Step 2: Environment Configuration
    
    Create a `.env` file in the project root directory:
    
    ```env
    # Azure OpenAI Configuration
    OPENAI_API_KEY=your_azure_openai_api_key_here
    OPENAI_API_BASE=https://your-endpoint.openai.azure.com/
    OPENAI_API_VERSION=2024-12-01-preview
    OPENAI_DEPLOYMENT=o3-mini
    
    # Database Configuration (optional - defaults to SQLite)
    DATABASE_URL=sqlite:///./events.db
    ```
    
    ### Step 3: Install Required Dependencies
    
    The project requires these main packages:
    
    ```bash
    pip install streamlit fastapi uvicorn sqlalchemy pandas pydantic
    pip install openai tiktoken pypdf2 python-multipart requests
    ```
    
    Or use the requirements file:
    
    ```bash
    pip install -r requirements.txt
    ```
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 🚀 Running the Application
    
    ### Method 1: Streamlit Only (Recommended for Development)
    
    ```bash
    # Run the main application
    streamlit run app.py --server.port 5000
    ```
    
    The application will automatically start the FastAPI backend on port 8000.
    
    ### Method 2: Manual Backend Start (Advanced)
    
    If you prefer to run the backend separately:
    
    ```bash
    # Terminal 1: Start FastAPI backend
    cd backend
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    
    # Terminal 2: Start Streamlit frontend
    streamlit run app.py --server.port 5000
    ```
    
    ### Accessing the Application
    
    - **Frontend**: http://localhost:5000
    - **Backend API**: http://localhost:8000
    - **API Documentation**: http://localhost:8000/docs
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 📁 Project Structure
    
    ```
    ai-taskmaster/
    ├── app.py                  # Main Streamlit application
    ├── requirements.txt        # Python dependencies
    ├── events.db              # SQLite database (auto-created)
    ├── replit.md              # Project documentation
    │
    ├── backend/               # FastAPI backend
    │   ├── main.py           # FastAPI application and routes
    │   ├── models.py         # SQLAlchemy database models
    │   ├── schemas.py        # Pydantic validation schemas
    │   └── database.py       # Database configuration
    │
    ├── pages/                # Streamlit page modules
    │   ├── event_management.py
    │   └── ai_challenges.py
    │
    ├── challenges/           # AI challenge implementations
    │   ├── challenge1.py     # Product Ideation
    │   ├── challenge2.py     # Parameter Tuning
    │   ├── challenge3.py     # Prompt Engineering
    │   └── challenge4.py     # RAG Security
    │
    └── utils/               # Utility modules
        ├── ai_client.py     # Azure OpenAI client wrapper
        └── prompt_templates.py
    ```
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 🔧 Configuration Details
    
    ### Database Setup
    
    The application uses SQLite by default with automatic table creation:
    
    - **Events table**: Stores event management data
    - **Hosts table**: Manages event host information
    - **Auto-migration**: Tables created automatically on first run
    
    ### Azure OpenAI Integration
    
    The application integrates with Azure OpenAI using the o3-mini model:
    
    - **Retry mechanism**: 3 attempts with exponential backoff
    - **Token optimization**: Configurable limits per challenge
    - **Error handling**: Comprehensive error messages and fallbacks
    
    ### API Endpoints
    
    The FastAPI backend provides these endpoints:
    
    - `GET /health` - Health check
    - `GET /events` - List all events
    - `POST /events` - Create new event
    - `GET /events/{id}` - Get specific event
    - `PUT /events/{id}` - Update event
    - `DELETE /events/{id}` - Delete event
    - `GET /hosts` - List all hosts
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 🧪 Testing the Setup
    
    ### 1. Verify Backend Connection
    
    Visit http://localhost:8000/health to ensure the API is running.
    
    ### 2. Test Event Management
    
    - Navigate to "Event Management" tab
    - Try creating, viewing, and editing events
    - Verify data persistence
    
    ### 3. Test AI Challenges
    
    - Navigate to "AI Challenges" tab
    - Test each challenge with sample inputs
    - Verify Azure OpenAI responses
    
    ### 4. Check Database
    
    The `events.db` file should be created in the project root with your test data.
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 🔍 Troubleshooting
    
    ### Common Issues
    
    **1. Azure OpenAI Connection Errors**
    - Verify your API key and endpoint in the `.env` file
    - Check that your Azure subscription has OpenAI access
    - Ensure the o3-mini model is deployed in your Azure OpenAI resource
    
    **2. Port Already in Use**
    ```bash
    # Kill processes on port 5000 or 8000
    # On Windows:
    netstat -ano | findstr :5000
    taskkill /PID <process_id> /F
    
    # On macOS/Linux:
    lsof -ti:5000 | xargs kill -9
    ```
    
    **3. Database Issues**
    - Delete `events.db` file to reset the database
    - Check file permissions in the project directory
    
    **4. Import Errors**
    - Ensure all dependencies are installed: `pip install -r requirements.txt`
    - Verify virtual environment is activated
    
    ### Getting Help
    
    If you encounter issues:
    1. Check the console output for error messages
    2. Verify all environment variables are set correctly
    3. Ensure all required ports (5000, 8000) are available
    4. Check that Azure OpenAI credentials are valid
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 🎓 Learning Objectives
    
    This project demonstrates:
    
    ### Technical Skills
    - **Frontend Development**: Streamlit for rapid web app creation
    - **Backend Development**: FastAPI for modern Python APIs
    - **Database Management**: SQLAlchemy ORM with SQLite
    - **AI Integration**: Azure OpenAI API implementation
    - **Error Handling**: Robust retry mechanisms and validation
    
    ### Software Engineering Practices
    - **Project Structure**: Modular code organization
    - **Configuration Management**: Environment-based settings
    - **API Design**: RESTful endpoints with proper HTTP methods
    - **Data Validation**: Pydantic schemas for type safety
    - **Documentation**: Comprehensive setup and usage guides
    
    ### AI/ML Concepts
    - **Prompt Engineering**: Systematic optimization techniques
    - **Parameter Tuning**: Understanding model configuration
    - **RAG Implementation**: Document processing and retrieval
    - **Token Management**: Cost optimization strategies
    """)
    
    st.success("✅ Setup guide complete! Follow the steps above to run the application locally.")

# Load CSS
load_css()

# Start backend
start_backend()

# Sidebar
with st.sidebar:
    st.title("🤖 AI TaskMaster")
    
    # Dark mode toggle
    dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.experimental_rerun()
    
    # Apply dark mode styling
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            .stApp {
                background-color: #1E1E1E !important;
                color: #FFFFFF !important;
            }
            .stSidebar {
                background-color: #2D2D2D !important;
            }
            .stSidebar .stMarkdown {
                color: #FFFFFF !important;
            }
            .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3 {
                color: #FFFFFF !important;
            }
            .stSidebar .stMarkdown p, .stSidebar .stMarkdown div, .stSidebar .stMarkdown span {
                color: #FFFFFF !important;
            }
            .stSidebar .stMarkdown ul, .stSidebar .stMarkdown li {
                color: #FFFFFF !important;
            }
            .stSidebar [data-testid="stMarkdownContainer"] {
                color: #FFFFFF !important;
            }
            .stSidebar .stRadio > div {
                color: #FFFFFF !important;
            }
            .stSidebar .stRadio label {
                color: #FFFFFF !important;
            }
            .stSidebar .stExpander {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
            }
            .stSidebar .stExpander .stMarkdown {
                color: #FFFFFF !important;
            }
            .stSidebar .stExpander summary {
                color: #FFFFFF !important;
            }
            .stHeader {
                background-color: #1E1E1E !important;
            }
            .stToolbar {
                background-color: #1E1E1E !important;
            }
            [data-testid="stHeader"] {
                background-color: #1E1E1E !important;
            }
            /* Main content text visibility */
            .main .block-container {
                background-color: #1E1E1E !important;
                color: #FFFFFF !important;
            }
            .stMarkdown, .stMarkdown p, .stMarkdown div {
                color: #FFFFFF !important;
            }
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
                color: #FFFFFF !important;
            }
            /* Form elements */
            .stTextInput input, .stTextArea textarea, .stSelectbox select {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
                border: 1px solid #444444 !important;
            }
            .stNumberInput input {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
                border: 1px solid #444444 !important;
            }
            /* Button styling */
            .stButton button {
                background-color: #FF6B6B !important;
                color: #FFFFFF !important;
                border: none !important;
            }
            /* Tab styling */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #2D2D2D !important;
            }
            .stTabs [data-baseweb="tab"] {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #FF6B6B !important;
                color: #FFFFFF !important;
            }
            /* Dataframe styling */
            .stDataFrame {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
            }
            /* Code blocks */
            .stCode {
                background-color: #1A1A1A !important;
                color: #FFFFFF !important;
                border: 1px solid #444444 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    tab_selection = st.radio(
        "Select Tab:",
        ["README", "Week 2/3 - Event Management", "Week 4 - AI Challenges"],
        index=0
    )
    
    st.markdown("---")

# Main content area
if tab_selection == "README":
    render_readme()
elif tab_selection == "Week 2/3 - Event Management":
    from pages.event_management import render_event_management
    render_event_management()
elif tab_selection == "Week 4 - AI Challenges":
    from pages.ai_challenges import render_ai_challenges
    render_ai_challenges()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        AI TaskMaster v1.0 | Built with Streamlit, FastAPI, and Azure OpenAI
    </div>
    """,
    unsafe_allow_html=True
)
