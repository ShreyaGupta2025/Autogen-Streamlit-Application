import os
import streamlit as st
from src.logo_title import logo_title

# Page configuration
st.set_page_config(
    page_title="Agentic AI Application",
    page_icon="🦜",
    layout="wide"
)

# Logo and title
logo_title("🦜🔗 Agentic AI Application")

# Welcome message
st.markdown("""
## Welcome to Agentic AI Application

This application provides a comprehensive platform for creating, managing, and deploying AI agents using **AutoGen** and **AutogenStudio** frameworks. Build sophisticated multi-agent systems with intuitive interfaces and powerful automation capabilities.
""")

# Application overview
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 **What You Can Do**
    
    **🎨 Agent Designer**
    - Create custom AI agents with specific roles
    - Configure agent personalities and behaviors
    - Design multi-agent workflows and interactions
    - Test and validate agent configurations
    
    **💬 Team Chat**
    - Deploy and run your configured agent teams
    - Real-time multi-agent conversations
    - Stream responses from agent interactions
    - Monitor team performance and outputs
    """)

with col2:
    st.markdown("""
    ### 🚀 **Key Features**
    
    **AutogenStudio Integration**
    - Visual agent design interface
    - Drag-and-drop workflow creation
    - Pre-built agent templates
    - Configuration export/import
    
    **Multi-Agent Orchestration**
    - Team-based problem solving
    - Collaborative AI workflows
    - Role-based agent interactions
    - Scalable agent deployments
    """)

# Getting started guide
st.markdown("---")
st.subheader("🏁 Getting Started Guide")

tab1, tab2, tab3 = st.tabs(["📋 Prerequisites", "🎨 Using Agent Designer", "💬 Running Team Chat"])

with tab1:
    st.markdown("""
    ### Prerequisites & Setup
    
    **1. Install Required Packages**
    ```bash
    # Core AutoGen packages
    pip install pyautogen autogen-agentchat
    
    # AutogenStudio for visual design
    pip install autogenstudio
    
    # Streamlit for web interface
    pip install streamlit
    ```
    
    **2. API Configuration**
    - Set up API keys for your preferred LLM providers (OpenAI, Azure, Groq, etc.)
    - Configure model endpoints and authentication
    - Ensure sufficient API credits and rate limits
    
    **3. Start AutogenStudio Server** (Optional but recommended)
    ```bash
    autogenstudio ui --port 8080
    ```
    """)

with tab2:
    st.markdown("""
    ### Using the Agent Designer
    
    **Step 1: Access the Designer**
    - Navigate to the **"Agent Designer"** page from the sidebar
    - Click **"🚀 Open AutogenStudio Designer"** to launch the visual interface
    
    **Step 2: Create Your Agents**
    - Use the visual interface to design custom agents
    - Configure agent roles, personalities, and capabilities
    - Set up model connections and API configurations
    - Define agent interaction patterns and workflows
    
    **Step 3: Save & Export**
    - Save your agent configurations
    - Export team configurations as JSON files
    - Test agent interactions within the designer
    
    **Step 4: Deploy to Chat**
    - Export your team configuration
    - Upload it to the Team Chat interface for deployment
    """)

with tab3:
    st.markdown("""
    ### Running Team Chat
    
    **Step 1: Prepare Team Configuration**
    - Create or obtain a team configuration JSON file
    - Ensure all agents have proper model client configurations
    - Validate API keys and endpoint settings
    
    **Step 2: Upload Configuration**
    - Navigate to the **"chat"** page
    - Upload your team configuration JSON file
    - Wait for validation and team initialization
    
    **Step 3: Start Conversations**
    - Send messages to your agent team
    - Monitor real-time agent interactions and responses
    - Observe how agents collaborate to solve problems
    
    **Step 4: Monitor & Optimize**
    - Review conversation history and agent performance
    - Adjust configurations based on results
    - Iterate and improve your agent designs
    """)

# Quick navigation
st.markdown("---")
st.subheader("🧭 Quick Navigation")

# Initialize session state for documentation
if 'show_documentation' not in st.session_state:
    st.session_state.show_documentation = False

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎨 Go to Agent Designer", use_container_width=True):
        st.switch_page("pages/1_Agent_Designer.py")

with col2:
    if st.button("💬 Go to Agentic Squad", use_container_width=True):
        st.switch_page("pages/4_AgenticSquad.py")

with col3:
    if st.button("📚 View Documentation", use_container_width=True):
        st.session_state.show_documentation = not st.session_state.show_documentation

# Display documentation iframe if toggled on
if st.session_state.show_documentation:
    st.markdown("---")
    st.subheader("📚 AutoGen Documentation")
    
    # Close button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("❌ Close Documentation", use_container_width=True):
            st.session_state.show_documentation = False
            st.rerun()
    
    st.markdown("---")
    
    # Embed the AutoGen documentation
    documentation_url = "https://microsoft.github.io/autogen/stable//index.html"
    
    st.components.v1.iframe(
        src=documentation_url,
        width=None,  # Full width
        height=700,  # Good height for documentation
        scrolling=True
    )

# Tips and best practices
st.markdown("---")
with st.expander("💡 Tips & Best Practices"):
    st.markdown("""
    ### Agent Design Best Practices
    
    **🎯 Clear Role Definition**
    - Give each agent a specific, well-defined role
    - Avoid overlapping responsibilities between agents
    - Create complementary skill sets within teams
    
    **🔄 Iterative Development**
    - Start with simple agent configurations
    - Test frequently with basic interactions
    - Gradually add complexity and capabilities
    
    **📊 Performance Monitoring**
    - Monitor API usage and costs
    - Track conversation quality and relevance
    - Optimize model selection for different agent roles
    
    **🛡️ Error Handling**
    - Configure robust error handling and fallbacks
    - Set appropriate timeout and retry settings
    - Plan for API rate limit scenarios
    
    ### Technical Considerations
    
    **🔐 Security**
    - Keep API keys secure and never commit them to version control
    - Use environment variables for sensitive configuration
    - Regularly rotate API keys and access tokens
    
    **💰 Cost Management**
    - Choose appropriate models for different agent roles
    - Monitor token usage and API costs
    - Implement conversation length limits when appropriate
    """)

# Developer Information Panel
with st.expander("🚀 Developer: FastAPI Integration Ready"):
    st.markdown("""
    **This implementation is designed for easy FastAPI conversion:**
    
    ### Key Components:
    
    1. **StreamlitChatManager**: Core orchestration logic
       - `run_team_chat_stream()`: Async message streaming
       - `save_and_validate_config()`: Config management
       - Easily convertible to FastAPI dependencies
    
    2. **StreamlitWebSocketSimulator**: WebSocket abstraction
       - `accept()`, `send_json()`, `receive_json()` methods
       - Direct mapping to FastAPI WebSocket methods
    
    3. **ChatAPI**: Static API methods ready for FastAPI
       - `health_check()`: GET /health endpoint
       - `validate_team_config()`: POST /validate-config endpoint
       - `process_chat_message()`: WebSocket message handler
    
    ### Server.py Pattern Compliance:
    
    ✅ **TeamManager Integration**: Uses AutogenStudio's TeamManager  
    ✅ **Async Streaming**: Mimics `run_stream()` from server.py  
    ✅ **WebSocket Simulation**: Ready for real WebSocket conversion  
    ✅ **Health Endpoints**: Standard server monitoring  
    ✅ **Error Handling**: Structured error responses  
    ✅ **Config Management**: Team configuration validation  
    """)
    
    # FastAPI Preview Section
    st.markdown("---")
    st.markdown("### 🚀 FastAPI Preview")
    st.caption("Test endpoints that will be available in FastAPI")
    
    # FastAPI conversion guide
    st.markdown("**Ready for FastAPI conversion:**")
    st.markdown("""
    1. **Health Check**: `GET /health`
    2. **Config Validation**: `POST /validate-config`
    3. **WebSocket Chat**: `WebSocket /ws/chat`
    4. **Team Chat**: `POST /team-chat`
    
    All core logic is in modular classes ready for API endpoints.
    """)
    
    # Show FastAPI conversion example
    st.markdown("### FastAPI Conversion Example:")
    st.code("""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agentic AI Server", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Convert StreamlitChatManager to FastAPI dependency
manager = StreamlitChatManager()

@app.get("/")
async def root():
    return ChatAPI.health_check()

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        async for message in manager.run_team_chat_stream(user_input):
            await websocket.send_json({
                "type": message.type,
                "content": message.content,
                "sender": message.sender
            })
    except WebSocketDisconnect:
        pass

@app.post("/validate-config")
async def validate_config(config: dict):
    return await ChatAPI.validate_team_config(config)
    """, language="python")
    
    st.info("💡 All core logic is modular and ready for production FastAPI deployment!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <strong>🦜🔗 Agentic AI Application</strong><br>
    <small>Powered by AutoGen, AutogenStudio & Streamlit | Build intelligent multi-agent systems with ease</small>
</div>
""", unsafe_allow_html=True)