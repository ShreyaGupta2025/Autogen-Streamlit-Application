import streamlit as st
import asyncio
import json
import os
import tempfile
from typing import Optional, Dict, Any, List, AsyncGenerator
from dataclasses import dataclass

# Helper to extract text from agent responses
def extract_text_from_message_content(content):
    # If content is a dict, try to extract the 'content' field
    if isinstance(content, dict):
        # Try to get the assistant's message from OpenAI/Groq style response
        if "response" in content and "choices" in content["response"]:
            try:
                return content["response"]["choices"][0]["message"]["content"]
            except Exception:
                pass
        # Fallback: just get 'content' if present
        return content.get("content", str(content))
    # If content is a JSON string, try to parse it
    if isinstance(content, str):
        try:
            data = json.loads(content)
            return extract_text_from_message_content(data)
        except Exception:
            return content
    # Fallback: return as string
    return str(content)

# Try to import AutogenStudio components, fallback gracefully
try:
    from autogen_agentchat.agents._user_proxy_agent import UserProxyAgent as NewUserProxyAgent
    from autogenstudio.teammanager import TeamManager
    AUTOGENSTUDIO_AVAILABLE = True
    # st.success("✅ AutogenStudio components loaded successfully!")
except ImportError:
    from autogen import AssistantAgent, UserProxyAgent
    AUTOGENSTUDIO_AVAILABLE = False
    st.warning("⚠️ AutogenStudio not available. Install autogen-agentchat and autogenstudio for full functionality.")
    
    # Create mock TeamManager for fallback
    class TeamManager:
        def __init__(self):
            pass
        
        async def run_stream(self, task: str, team_config: str, **kwargs):
            yield type('Message', (), {'content': f"Mock response to: {task}"})()

@dataclass
class ChatMessage:
    """Message structure similar to server.py"""
    type: str
    content: str
    sender: Optional[str] = None


# st.write("""# AutoGen Chat Agents (AutogenStudio Pattern)""")
# st.write("""
# # AgenticSquad  
# _Autonomous Multi-Agent Chat Studio_
# """)



class StreamlitChatManager:
    """
    Chat manager that mimics server.py TeamManager pattern for Streamlit.
    Uses AutogenStudio's TeamManager for orchestrating multi-agent conversations.
    """
    
    def __init__(self):
        self.team_manager = TeamManager()
        self.config_from_file = None
        self.team_config_path = None
        self.chat_history = []
        self.input_queue = asyncio.Queue()
        self.current_task = None
        
    async def save_and_validate_config(self, uploaded_file) -> bool:
        """Save uploaded config to temporary file like server.py"""
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            self.config_from_file = json.load(uploaded_file)
            
            # Create temporary team config file (server.py pattern)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(self.config_from_file, f, indent=2)
                self.team_config_path = f.name
                
            st.success(f"✅ Team config saved: {os.path.basename(self.team_config_path)}")
            
            # Validate config structure
            if not self._validate_team_config():
                return False
                
            return True
            
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file. Please upload a valid team configuration.")
            return False
        except Exception as e:
            st.error(f"❌ Error processing config: {str(e)}")
            return False
    
    def _validate_team_config(self) -> bool:
        """Validate team configuration structure"""
        try:
            if 'config' not in self.config_from_file:
                st.error("❌ Missing 'config' key in team configuration")
                return False
                
            if 'participants' not in self.config_from_file['config']:
                st.error("❌ Missing 'participants' in team configuration")
                return False
                
            participants = self.config_from_file['config']['participants']
            if not participants:
                st.error("❌ No participants defined in team configuration")
                return False
                
            st.success(f"✅ Team config validated: {len(participants)} participants found")
            return True
            
        except Exception as e:
            st.error(f"❌ Config validation error: {str(e)}")
            return False
    
    async def run_team_chat_stream(self, user_message: str) -> AsyncGenerator[ChatMessage, None]:
        """
        Run team chat using AutogenStudio TeamManager (server.py pattern).
        Yields messages as they are generated.
        """
        try:
            if not self.team_config_path:
                raise ValueError("No team configuration loaded")
            
            # Add user message to history
            self.add_message("user", user_message)
            yield ChatMessage(type="user_message", content=user_message, sender="user")
            
            # Use TeamManager to run the conversation (server.py pattern)
            async for message in self.team_manager.run_stream(
                task=user_message,
                team_config=self.team_config_path
            ):
                # Filter and process messages like server.py
                if hasattr(message, 'content') and message.content:
                    # Add to history
                    sender_name = getattr(message, 'sender', 'assistant')
                    self.add_message(sender_name, message.content)
                    
                    # Yield formatted message
                    yield ChatMessage(
                        type="ai_message", 
                        content=message.content, 
                        sender=sender_name
                    )
                    
        except Exception as e:
            error_msg = f"❌ Team chat error: {str(e)}"
            st.error(error_msg)
            yield ChatMessage(type="error", content=error_msg)
    
    def add_message(self, role: str, content: str):
        """Add message to chat history (server.py pattern)"""
        self.chat_history.append({
            "role": role,
            "content": content,
            "type": "ai_message" if role != "user" else "user_message"
        })
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """Get recent messages for display"""
        return self.chat_history[-limit:] if self.chat_history else []
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
    
    def cleanup(self):
        """Cleanup temporary files"""
        if self.team_config_path and os.path.exists(self.team_config_path):
            try:
                os.unlink(self.team_config_path)
                st.info(f"🧹 Cleaned up: {os.path.basename(self.team_config_path)}")
            except Exception as e:
                st.warning(f"⚠️ Cleanup warning: {str(e)}")

class StreamlitWebSocketSimulator:
    """
    Simulates WebSocket functionality for Streamlit (server.py pattern).
    This class can be easily converted to actual WebSocket for FastAPI.
    """
    
    def __init__(self, chat_manager: StreamlitChatManager):
        self.chat_manager = chat_manager
        self.input_queue = asyncio.Queue()
        self.is_connected = False
    
    async def accept(self):
        """Simulate WebSocket accept"""
        self.is_connected = True
        return True
    
    async def send_json(self, data: Dict):
        """Simulate sending JSON data (for FastAPI conversion)"""
        # In Streamlit, we display the message directly
        if data.get("type") == "ai_message":
            with st.chat_message("assistant"):
                st.markdown(data.get("text", ""))
        elif data.get("type") == "error":
            st.error(data.get("text", "Unknown error"))
    
    async def receive_json(self) -> Dict:
        """Simulate receiving JSON data"""
        # In Streamlit, this would be handled by chat_input
        return await self.input_queue.get()
    
    async def put_user_response(self, message: str):
        """Put user response into queue (server.py pattern)"""
        await self.input_queue.put({"type": "user_response", "text": message})

# FastAPI-ready API class (server.py pattern)
class ChatAPI:
    """
    API-ready functions that mirror server.py endpoints.
    Can be easily converted to FastAPI endpoints.
    """
    
    @staticmethod
    def health_check() -> Dict[str, Any]:
        """Health check endpoint (server.py pattern)"""
        return {
            "message": "Agentic AI Streamlit Server is running",
            "status": "healthy",
            "service": "agentic-ai-streamlit",
            "autogenstudio_available": AUTOGENSTUDIO_AVAILABLE
        }
    
    @staticmethod
    async def validate_team_config(config_data: Dict[Any, Any]) -> Dict[str, Any]:
        """Validate team configuration (FastAPI ready)"""
        try:
            # Create temporary manager for validation
            temp_manager = StreamlitChatManager()
            
            # Create temporary file for validation
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(config_data, f)
                f.seek(0)
                
                # Validate using the manager
                if await temp_manager.save_and_validate_config(f):
                    temp_manager.cleanup()
                    return {"status": "valid", "message": "Team configuration is valid"}
                else:
                    temp_manager.cleanup()
                    return {"status": "invalid", "error": "Team configuration validation failed"}
                    
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    @staticmethod
    async def process_chat_message(config_path: str, message: str) -> Dict[str, Any]:
        """Process chat message (FastAPI WebSocket ready)"""
        try:
            manager = TeamManager()
            responses = []
            
            async for msg in manager.run_stream(task=message, team_config=config_path):
                if hasattr(msg, 'content'):
                    responses.append({
                        "type": "ai_message",
                        "content": msg.content,
                        "sender": getattr(msg, 'sender', 'assistant')
                    })
            
            return {"status": "success", "messages": responses}
            
        except Exception as e:
            return {"status": "error", "error": str(e)}

# Enhanced Trackable Agents (fallback for classic AutoGen)
if not AUTOGENSTUDIO_AVAILABLE:
    class TrackableAssistantAgent(AssistantAgent):
        def __init__(self, chat_manager=None, **kwargs):
            super().__init__(**kwargs)
            self.chat_manager = chat_manager
        
        def _process_received_message(self, message, sender, silent):
            with st.chat_message(sender.name):
                st.markdown(message)
            
            if self.chat_manager:
                self.chat_manager.add_message(sender.name, message)
                
            return super()._process_received_message(message, sender, silent)

    class TrackableUserProxyAgent(UserProxyAgent):
        def __init__(self, chat_manager=None, **kwargs):
            super().__init__(**kwargs)
            self.chat_manager = chat_manager
        
        def _process_received_message(self, message, sender, silent):
            with st.chat_message(sender.name):
                st.markdown(message)
            
            if self.chat_manager:
                self.chat_manager.add_message(sender.name, message)
                
            return super()._process_received_message(message, sender, silent)

# Initialize session state
if 'chat_manager' not in st.session_state:
    st.session_state.chat_manager = StreamlitChatManager()

if 'websocket_sim' not in st.session_state:
    st.session_state.websocket_sim = StreamlitWebSocketSimulator(st.session_state.chat_manager)

with st.sidebar:
    st.header("AgenticSquad")

    
    # Health check display (server.py pattern)
    health_status = ChatAPI.health_check()
    with st.expander("🏥 System Health"):
        st.json(health_status)


    
    st.markdown("---")
    
    # Team configuration uploader
    st.subheader("📁 Team Configuration")
    uploaded_file = st.file_uploader(
        "Upload Team Config JSON", 
        type=['json'],
        help="Upload your AutogenStudio team configuration file"
    )
    
    if uploaded_file is not None:
        # Process config using ChatManager (server.py pattern)
        if asyncio.run(st.session_state.chat_manager.save_and_validate_config(uploaded_file)):
            st.success("🚀 Team configuration loaded and validated!")
            
            # Show team info
            if st.session_state.chat_manager.config_from_file:
                config = st.session_state.chat_manager.config_from_file
                participants = config.get('config', {}).get('participants', [])
                
                st.info(f"👥 Team has {len(participants)} participants")
                
                # Show participant details
                with st.expander("👥 Team Participants"):
                    for i, participant in enumerate(participants):
                        agent_config = participant.get('config', {})
                        agent_name = agent_config.get('name', f'Agent_{i+1}')
                        agent_type = participant.get('provider', 'Unknown').split('.')[-1]
                        st.text(f"• {agent_name} ({agent_type})")
                
                # Config debug (hide sensitive info)
        
    else:
        st.info("📤 Upload your team configuration to start")
        
        # Show expected team config format (server.py documentation style)
        with st.expander("📋 Team Config Format"):
            st.markdown("**AutogenStudio Team Configuration:**")
            st.code('''
{
  "provider": "autogen_agentchat.teams.SelectorGroupChat",
  "config": {
    "participants": [
      {
        "provider": "autogen_agentchat.agents.AssistantAgent",
        "config": {
          "name": "Assistant",
          "model_client": {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "config": {
              "model": "llama3-70b-8192",
              "api_key": "your-api-key",
              "base_url": "your-base-url"
            }
          }
        }
      }
    ]
  }
}
            ''', language='json')

# Chat History & Status (server.py pattern)
with st.sidebar:
    
    # Recent messages preview
    if st.session_state.chat_manager.chat_history:
        with st.expander("� Recent Messages"):
            recent = st.session_state.chat_manager.get_recent_messages(5)
            for msg in recent:
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                st.text(f"{role_icon} {msg['role']}: {msg['content'][:50]}...")
    
    # Chat controls
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset Chat"):
            st.session_state.chat_manager.clear_history()
            st.rerun()
    
    with col2:
        if st.button("🧹 Cleanup"):
            st.session_state.chat_manager.cleanup()
            st.success("Cleaned up!")


with st.container():
    # Display existing chat history
    if st.session_state.chat_manager.chat_history:
        for msg in st.session_state.chat_manager.chat_history:
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"]):
                st.markdown(f"{role_icon} **{msg['role'].title()}**")
                st.markdown(extract_text_from_message_content(msg["content"]))

# Footer with system information (server.py pattern)

# Place "Powered by AgenticSquad" just above the chat input at the very bottom
# st.caption("Powered by AgenticSquad")

# Place chat input at the very bottom of the app
user_input = st.chat_input("💬 Message your team...")

if user_input:
    # Check if team is configured
    if not st.session_state.chat_manager.team_config_path:
        st.warning('⚠️ Please upload a team configuration file first!', icon="⚠️")
        st.stop()
    # Process message using TeamManager (server.py pattern)
    try:
        # Use WebSocket simulator to handle the conversation
        asyncio.run(st.session_state.websocket_sim.accept())
        # Stream team conversation using TeamManager
        with st.spinner("🤖 Team is thinking..."):
            # Use async generator for streaming responses (server.py pattern)
            async def process_team_chat():
                displayed_messages = set()
                async for message in st.session_state.chat_manager.run_team_chat_stream(user_input):
                    # Only display each message once
                    msg_id = f"{message.type}:{message.sender}:{extract_text_from_message_content(message.content)}"
                    if msg_id in displayed_messages:
                        continue
                    displayed_messages.add(msg_id)
                    if message.type == "user_message":
                        # User message already displayed by chat_input
                        pass
                    elif message.type == "ai_message":
                        # Display AI responses as they come
                        with st.chat_message("assistant"):
                            st.markdown(f"🤖 **{message.sender or 'Assistant'}**")
                            st.markdown(extract_text_from_message_content(message.content))
                    elif message.type == "error":
                        st.error(extract_text_from_message_content(message.content))
            # Run the async chat processing
            asyncio.run(process_team_chat())
    except Exception as e:
        st.error(f"❌ Team chat error: {str(e)}")
        # Enhanced error handling and suggestions
        with st.expander("🔧 Troubleshooting"):
            st.markdown("""
            **Common Issues:**
            1. **Team Config Issues**: 
               - Ensure your team.json has valid participant configurations
               - Check that all required model_client configs are present
            2. **API Connection Issues**:
               - Verify API keys are valid and have sufficient credits
               - Check internet connection and API endpoint availability
            3. **AutogenStudio Issues**:
               - Install: `pip install autogen-agentchat autogenstudio`
               - Ensure team configuration matches AutogenStudio format
            4. **Rate Limiting**:
               - Wait a moment before trying again
               - Consider using different models or providers
            """)
            # Show current configuration status
            st.markdown("**Current Status:**")
            st.text(f"• AutogenStudio Available: {AUTOGENSTUDIO_AVAILABLE}")
            st.text(f"• Team Config Path: {st.session_state.chat_manager.team_config_path or 'None'}")
            st.text(f"• Chat History Length: {len(st.session_state.chat_manager.chat_history)}")