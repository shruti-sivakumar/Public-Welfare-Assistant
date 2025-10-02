import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
from io import BytesIO
import requests
import uuid
import hashlib

# Import our modules
from azure_db import init_database_connection, test_connection, execute_query
from azure_openai import natural_language_to_sql, test_openai_connection

# Try to import database module with fallback
try:
    from database import get_database
except ImportError as e:
    st.error(f"Database module import error: {e}")
    def get_database():
        return None

from in_app_auth import (
    require_in_app_authentication, 
    show_user_profile_sidebar,
    get_current_user,
    has_role,
    is_authenticated
)
from rbac import rbac, show_access_control_panel, show_role_guard, show_feature_guard, can_query_database, can_export_data, is_admin, is_analyst, is_officer
from access_logger import (
    access_logger, 
    log_login, 
    log_logout, 
    log_query, 
    log_export, 
    log_page_access, 
    log_admin_action, 
    log_security_event
)

# Page config
st.set_page_config(
    page_title="Public Welfare Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .status-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .user-info {
        background: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .professional-table {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_district' not in st.session_state:
        st.session_state.user_district = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_query' not in st.session_state:
        st.session_state.current_query = ""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    # Global database connection flag
    if 'global_db_connected' not in st.session_state:
        st.session_state.global_db_connected = False
    
    # Session tracking for access logs
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'session_start_time' not in st.session_state:
        st.session_state.session_start_time = datetime.now()
    if 'last_login_logged' not in st.session_state:
        st.session_state.last_login_logged = False

# Auto-connect to Azure Database BEFORE login
def auto_connect_database():
    """Automatically connect to Azure Database when app starts - before login"""
    # Use a simple global connection flag
    if not st.session_state.get('global_db_connected', False):
        with st.spinner("Connecting to Azure SQL Database..."):
            # Initialize the connection (cached)
            conn = init_database_connection()
            if conn:
                # Test the connection
                if test_connection(show_messages=False):
                    st.session_state.global_db_connected = True
                    st.session_state.db_connected = True
                    st.success("Azure Database connected successfully!")
                    return True
                else:
                    st.error("Database connection test failed!")
                    return False
            else:
                st.error("Failed to establish database connection!")
                return False
    return True

    if 'db_connected' not in st.session_state:
        st.session_state.db_connected = False
    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = False

# Check API connection
def check_api_connection():
    """Check if the FastAPI backend is running"""
    try:
        # Use Azure backend URL instead of localhost
        backend_url = "https://welfare-app-anech0dsctemhwbq.centralindia-01.azurewebsites.net"
        response = requests.get(f"{backend_url}/health", timeout=30)
        if response.status_code == 200:
            st.session_state.api_connected = True
            st.session_state.backend_url = backend_url
            return True
    except Exception as e:
        st.session_state.api_connected = False
        return False
    return False

# API Connection Status Modal
def show_api_status_popup():
    """Show API connection status popup"""
    # Check connection
    is_connected = check_api_connection()
    
    # API connection status is now handled in create_sidebar()
    
    # Show modal-style notification if disconnected
    if not is_connected:
        # Use a container for better visibility
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.error("API Backend Not Available")
                st.info("Some features may not work properly without the FastAPI backend connection.")
    
    return is_connected

init_session_state()

# Auto-connect to Azure Database BEFORE any user interaction
auto_connect_database()

# Load data from database or fallback to sample data
@st.cache_data
def load_data_from_db():
    """Load data from database or use sample data if not connected"""
    # Always use sample data for demonstration purposes
    # Remove database dependency
    
    # Sample welfare schemes data
    schemes = pd.DataFrame({
        'scheme_id': [1, 2, 3, 4, 5],
        'name': ['MGNREGA', 'PMAY', 'Ujjwala Yojana', 'Ayushman Bharat', 'NSAP'],
        'sector': ['Employment', 'Housing', 'Energy', 'Healthcare', 'Social Security'],
        'total_enrollments': [65, 42, 38, 32, 28],
        'total_disbursements': [1250000, 5040000, 76000, 480000, 67200]
    })
    
    # All 80 districts from the comprehensive welfare database
    districts = [
        # Uttar Pradesh
        'Agra', 'Lucknow', 'Kanpur', 'Varanasi', 'Allahabad',
        # Maharashtra  
        'Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad',
        # Bihar
        'Patna', 'Gaya', 'Muzaffarpur', 'Bhagalpur', 'Darbhanga',
        # West Bengal
        'Kolkata', 'Darjeeling', 'Howrah', 'Siliguri', 'Asansol',
        # Madhya Pradesh
        'Bhopal', 'Indore', 'Gwalior', 'Jabalpur', 'Ujjain',
        # Tamil Nadu
        'Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli',
        # Rajasthan
        'Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer',
        # Karnataka
        'Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum',
        # Gujarat
        'Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar',
        # Andhra Pradesh
        'Hyderabad', 'Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore',
        # Odisha
        'Bhubaneswar', 'Cuttack', 'Rourkela', 'Berhampur', 'Sambalpur',
        # Telangana
        'Warangal', 'Nizamabad', 'Khammam', 'Karimnagar', 'Ramagundam',
        # Kerala
        'Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur', 'Kollam',
        # Jharkhand
        'Ranchi', 'Jamshedpur', 'Dhanbad', 'Bokaro', 'Deoghar',
        # Assam
        'Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat', 'Nagaon'
    ]
    
    return schemes, districts

schemes_data, districts_list = load_data_from_db()

# Authentication (In-App Auth0)
def show_login():
    """Show in-app authentication page"""
    require_in_app_authentication()

# Sidebar
def create_sidebar():
    with st.sidebar:
        # Public Welfare Assistant at the very top
        st.markdown("# Public Welfare Assistant")
        st.markdown("**System Administrator**")
        
        # Show user email right after title
        user = get_current_user()
        if user:
            st.markdown(f"**{user.get('email', 'No email')}**")
            
            st.divider()
            
            # API Connection Status right after user info
            st.subheader("API Connection Status")
            
            # Backend API Status
            try:
                backend_url = st.session_state.get('backend_url', 'https://welfare-app-anech0dsctemhwbq.centralindia-01.azurewebsites.net')
                response = requests.get(f"{backend_url}/health", timeout=2)
                if response.status_code == 200:
                    st.success("FastAPI Backend Connected")
                    st.write(f"Backend URL: {backend_url}")
                else:
                    st.error("FastAPI Backend Not Connected")
            except:
                st.error("FastAPI Backend Not Connected")
            
            if st.button("Refresh Connection", type="secondary", key="sidebar_refresh"):
                st.rerun()
            
            st.divider()
            
            # System Administrator role display
            st.markdown(f"**{user.get('name', 'User')}**")
            
            # Show user roles
            roles = user.get('roles', [])
            if roles:
                role_display = ', '.join([role.title() for role in roles])
                st.markdown(f"**Role:** {role_display}")
            
            # Show access level
            st.markdown("**Access Level:**")
            if is_admin():
                st.success("Administrator")
            elif is_analyst():
                st.info("Data Analyst")
            elif is_officer():
                st.warning("Welfare Officer")
            else:
                st.write("Basic User")
            
            # Show last login (but NOT logout button here)
            if hasattr(st.session_state, 'last_login'):
                st.write(f"Last login: {st.session_state.last_login}")
        
        st.divider()
        

        
        # Quick actions
        st.subheader("Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Query", use_container_width=True, key="sidebar_new_query"):
                # Clear the query input by resetting session state
                if 'query_input' in st.session_state:
                    st.session_state['query_input'] = ""
                if 'current_query' in st.session_state:
                    st.session_state['current_query'] = ""
                if 'transcribed_text' in st.session_state:
                    st.session_state['transcribed_text'] = ""
                st.success("New query started!")
        with col2:
            if st.button("Clear History", use_container_width=True, key="sidebar_clear_history"):
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history = []
                st.success("Chat history cleared!")
        
        if st.button("Export Data", use_container_width=True, key="sidebar_export_data"):
            # Create a simple export of current session data
            try:
                user = get_current_user()
                export_data = {
                    'timestamp': datetime.now().isoformat(),
                    'user': user.get('name', 'Unknown') if user else 'Unknown',
                    'email': user.get('email', 'No email') if user else 'No email',
                    'role': ', '.join([role.title() for role in user.get('roles', [])]) if user else 'Unknown',
                    'chat_history_count': len(st.session_state.get('chat_history', [])),
                    'session_info': 'Public Welfare Assistant Session Data'
                }
                import json
                st.download_button(
                    label="Download Session Data",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"pwa_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
        
        # Add space before logout button at the very bottom
        st.markdown("---")
        
        # Logout button at the very bottom
        if st.button("Logout", type="primary", use_container_width=True, key="sidebar_logout"):
            # Log logout before clearing session
            current_user = get_current_user()
            if current_user:
                log_logout(current_user)
            
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Logged out successfully!")
            st.rerun()
    
    # Return empty values since filters are removed
    return [], [], datetime.now() - timedelta(days=30), datetime.now()


# Main pages
def ask_page(selected_schemes):
    st.header("Database Query Interface")
    
    # Show connection status
    api_connected = st.session_state.get('api_connected', False)
    db_connected = st.session_state.get('db_connected', False)
    
    # Test OpenAI connection
    openai_connected = test_openai_connection()
    
    # Status indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        if db_connected:
            st.success("Azure SQL: Connected")
        else:
            st.error("Azure SQL: Disconnected")
    
    with col2:
        if openai_connected:
            st.success("Azure OpenAI: Connected")
        else:
            st.error("Azure OpenAI: Disconnected")
    
    with col3:
        if api_connected:
            st.success("FastAPI: Connected")
        else:
            st.warning("FastAPI: Optional")
    
    if db_connected and openai_connected:
        st.info("Full Azure Stack Ready: Natural Language → SQL → Results")
    elif db_connected:
        st.warning("Limited functionality: Database only (no AI processing)")
    else:
        st.error("No database connection available")
    

    # Speech-to-text direct recording using Azure Speech Service
    st.subheader("Voice Query (Speech-to-Text)")
    st.info("Click the microphone button below to record your voice query directly")
    
    # Initialize session state for audio processing
    if 'last_audio_hash' not in st.session_state:
        st.session_state.last_audio_hash = None
    if 'transcribed_text' not in st.session_state:
        st.session_state.transcribed_text = ""
    
    # Direct voice recording
    audio_data = st.audio_input("Record your voice query", key="voice_query_record")
    
    if audio_data:
        # Create hash of audio data to detect if it's new
        import hashlib
        # Read the audio data as bytes for hashing
        audio_bytes = audio_data.read()
        audio_data.seek(0)  # Reset file pointer for later use
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        
        # Only process if this is new audio
        if st.session_state.get('last_audio_hash') != audio_hash:
            st.session_state.last_audio_hash = audio_hash
            
            # Use Azure Speech Service for transcription
            try:
                from azure_speech import transcribe_audio
                
                with st.spinner("Transcribing your voice with Azure Speech Service..."):
                    transcribed_text = transcribe_audio(audio_data)
                    
                if transcribed_text and not transcribed_text.startswith("Error") and not transcribed_text.startswith("Azure Speech Service not available"):
                    st.session_state.transcribed_text = transcribed_text
                    st.success(f"Transcribed Text: {transcribed_text}")
                    
                    # Auto-populate the query field
                    if transcribed_text.strip():
                        st.session_state.query_input = transcribed_text
                        st.info("Voice query has been automatically loaded. You can edit it below if needed.")
                else:
                    st.error(f"Speech recognition failed: {transcribed_text}")
                    
            except ImportError:
                st.error("Azure Speech Service not available. Please check installation.")
            except Exception as e:
                st.error(f"Speech recognition error: {str(e)}")
                    
            except Exception as e:
                st.error(f"Speech-to-text request failed: {str(e)}")
        
        # Show the transcribed text if available
        if st.session_state.transcribed_text:
            st.success(f"Transcribed Text: **{st.session_state.transcribed_text}**")
            st.info("Voice query has been automatically loaded. You can edit it below if needed.")

    # Text input for queries
    query = st.text_input(
        "Enter your database query:",
        value=st.session_state.current_query,
        placeholder="e.g., 'Show citizen count', 'List all schemes', 'Show disbursements'",
        key="query_input"
    )
    
    # Query API backend function
    def query_api_backend(user_query):
        """Query the FastAPI backend"""
        try:
            backend_url = st.session_state.get('backend_url', 'https://welfare-app-anech0dsctemhwbq.centralindia-01.azurewebsites.net')
            response = requests.post(
                f"{backend_url}/nl2sql",
                json={"query": user_query},
                timeout=10
            )
            
            if response.status_code == 200:
                api_response = response.json()
                if api_response.get('success'):
                    return api_response
                else:
                    st.error(f"API Error: {api_response.get('message', 'Unknown error')}")
                    return None
            else:
                st.error(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Failed to connect to API: {str(e)}")
            return None
    
    # Process query
    if query and st.button("Execute Query"):
        # Log the query execution
        log_query(query)
        
        # Add to chat history
        st.session_state.chat_history.append({
            'timestamp': datetime.now(),
            'query': query,
            'response': None,
            'source': 'azure_openai'
        })
        
        # Get response using Azure OpenAI + Azure SQL
        with st.spinner("Converting natural language to SQL..."):
            # Step 1: Convert natural language to SQL using Azure OpenAI
            openai_result = natural_language_to_sql(query, show_reasoning=True)
            
            if "error" in openai_result:
                error_msg = openai_result['error']
                st.error(f"OpenAI Error: {error_msg}")
                st.session_state.chat_history.pop()
            else:
                sql_query = openai_result.get('sql_query', '')
                explanation = openai_result.get('explanation', 'Query executed')
                
                st.info(f"Generated SQL: `{sql_query}`")
                
                # Step 2: Execute the SQL query against Azure SQL Database
                with st.spinner("Executing SQL query..."):
                    try:
                        query_result = execute_query(sql_query)
                        
                        if query_result:
                            # Convert to DataFrame for display
                            df = pd.DataFrame(query_result)
                            
                            response = {
                                'summary': f"✅ {explanation}. Found {len(df)} results.",
                                'data': df,
                                'sql': sql_query,
                                'chart_type': 'table',
                                'openai_explanation': explanation
                            }
                            
                            st.session_state.chat_history[-1]['response'] = response
                            st.success(f"Query executed successfully! {len(df)} results found.")
                            
                        else:
                            st.warning("Query executed but returned no results.")
                            response = {
                                'summary': f"✅ {explanation}. No results found.",
                                'data': pd.DataFrame(),
                                'sql': sql_query,
                                'chart_type': 'table',
                                'openai_explanation': explanation
                            }
                            st.session_state.chat_history[-1]['response'] = response
                            
                    except Exception as e:
                        st.error(f"SQL Execution Error: {str(e)}")
                        st.session_state.chat_history.pop()
    
    # Display query results
    st.subheader(" Query Results")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        # User query
        with st.chat_message("user"):
            st.write(f"**{chat['timestamp'].strftime('%H:%M')}:** {chat['query']}")
        
        # Database response
        if chat['response']:
            with st.chat_message("assistant"):
                st.write(chat['response']['summary'])
            
            # Query details
            with st.expander("View Details", expanded=(i == 0)):
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["Table", "Chart", "SQL"])
                
                with tab1:
                    if not chat['response']['data'].empty:
                        st.dataframe(chat['response']['data'], use_container_width=True)
                        
                        # Download options - only for users with export permission
                        if can_export_data():
                            col1, col2 = st.columns(2)
                            with col1:
                                csv = chat['response']['data'].to_csv(index=False)
                                if st.download_button("Download CSV", csv, f"query_result_{i}.csv", "text/csv"):
                                    log_export("CSV")
                            with col2:
                                buffer = BytesIO()
                                chat['response']['data'].to_excel(buffer, index=False, engine='openpyxl')
                                buffer.seek(0)  # Reset buffer position
                                if st.download_button("Download Excel", buffer.getvalue(), f"query_result_{i}.xlsx"):
                                    log_export("Excel")
                        else:
                            st.info("Data export requires analyst or admin role. Contact your administrator for access.")
                
                with tab2:
                    # Chart visualization
                    if not chat['response']['data'].empty:
                        df = chat['response']['data']
                        
                        # Show data info for debugging
                        with st.expander("🔍 Data Debug Info", expanded=False):
                            st.write("**Column Information:**")
                            for col in df.columns:
                                dtype = str(df[col].dtype)
                                sample_values = df[col].dropna().head(3).tolist()
                                st.write(f"- **{col}** ({dtype}): {sample_values}")
                        
                        # More flexible column detection
                        if len(df.columns) >= 2:
                            # Get all possible numeric columns (including those that can be converted)
                            numeric_cols = []
                            categorical_cols = []
                            
                            for col in df.columns:
                                # Try to identify numeric columns more flexibly
                                if df[col].dtype in ['int64', 'float64', 'int32', 'float32', 'int16', 'float16']:
                                    numeric_cols.append(col)
                                elif df[col].dtype == 'object':
                                    # Check if object column contains numbers
                                    try:
                                        # Try to convert to numeric
                                        pd.to_numeric(df[col].dropna().head(5))
                                        numeric_cols.append(col)
                                    except (ValueError, TypeError):
                                        # It's categorical
                                        categorical_cols.append(col)
                                else:
                                    # String, datetime, or other types - treat as categorical
                                    categorical_cols.append(col)
                            
                            st.write(f"**Detected:** {len(numeric_cols)} numeric, {len(categorical_cols)} categorical columns")
                            
                            if len(numeric_cols) > 0 and len(categorical_cols) > 0:
                                # Allow user to select columns
                                col1, col2 = st.columns(2)
                                with col1:
                                    selected_label = st.selectbox("Label Column:", categorical_cols, 
                                                                index=0, key=f"label_{i}")
                                with col2:
                                    selected_value = st.selectbox("Value Column:", numeric_cols, 
                                                                index=0, key=f"value_{i}")
                                
                                # Create pie chart
                                try:
                                    # Convert value column to numeric if needed
                                    if df[selected_value].dtype == 'object':
                                        df[selected_value] = pd.to_numeric(df[selected_value], errors='coerce')
                                    
                                    # Remove any null values
                                    clean_df = df[[selected_label, selected_value]].dropna()
                                    
                                    if len(clean_df) == 0:
                                        st.error("No valid data after cleaning nulls")
                                    else:
                                        # Aggregate data by label (sum values for each category)
                                        chart_data = clean_df.groupby(selected_label)[selected_value].sum().reset_index()
                                        
                                        # Filter out zero or negative values for pie chart
                                        chart_data = chart_data[chart_data[selected_value] > 0]
                                        
                                        if len(chart_data) == 0:
                                            st.warning("No positive values found for pie chart")
                                        elif len(chart_data) > 20:
                                            # Too many categories, show top 20
                                            chart_data = chart_data.nlargest(20, selected_value)
                                            st.info("Showing top 20 categories")
                                        
                                        # Create pie chart
                                        fig = px.pie(chart_data, 
                                                   values=selected_value, 
                                                   names=selected_label,
                                                   title=f"Distribution of {selected_value} by {selected_label}")
                                        
                                        fig.update_traces(textposition='inside', textinfo='percent+label')
                                        fig.update_layout(height=500, showlegend=True)
                                        
                                        st.plotly_chart(fig, use_container_width=True)
                                        
                                        # Show summary stats
                                        total_value = chart_data[selected_value].sum()
                                        st.info(f"**Total {selected_value}:** {total_value:,.2f} | **Categories:** {len(chart_data)}")
                                        
                                except Exception as e:
                                    st.error(f"Chart generation failed: {str(e)}")
                                    st.info("**Troubleshooting:**")
                                    st.info("• Check if numeric column contains valid numbers")
                                    st.info("• Ensure categorical column has reasonable number of unique values")
                                    st.info("• Try different column combinations")
                            
                            elif len(numeric_cols) == 0:
                                st.warning("**No numeric columns detected** for pie chart values")
                                st.info("**Available columns:**")
                                for col in df.columns:
                                    dtype = str(df[col].dtype)
                                    st.write(f"• {col} ({dtype})")
                                st.info("💡 **Tip:** Pie charts need at least one numeric column for values")
                                
                            elif len(categorical_cols) == 0:
                                st.warning("**No categorical columns detected** for pie chart labels")
                                st.info("**Available columns:**")
                                for col in df.columns:
                                    dtype = str(df[col].dtype)
                                    st.write(f"• {col} ({dtype})")
                                st.info("💡 **Tip:** Pie charts need at least one text/categorical column for labels")
                                
                            else:
                                st.info("Unable to determine suitable columns for pie chart")
                                
                        else:
                            st.info("Chart visualization requires at least 2 columns of data.")
                            
                    else:
                        st.info("No data available for chart visualization.")
                
                with tab3:
                    st.code(chat['response']['sql'], language='sql')
                    # Show OpenAI explanation if available
                    if 'openai_explanation' in chat['response']:
                        st.info(f"AI Explanation: {chat['response']['openai_explanation']}")
                
                # Query information
                with st.expander("ℹ️ Query Information"):
                    source = chat.get('source', 'db')
                    if source == 'azure_openai':
                        st.write("**Data Source:** Azure SQL Database")
                        st.write("**AI Processing:** Azure OpenAI Service")
                        st.write("**Query Type:** Natural Language → SQL")
                    elif source == 'api':
                        st.write("**Data Source:** FastAPI Backend")
                        st.write("**Processing:** Enhanced AI Query Processing")
                    else:
                        st.write("**Data Source:** Direct Database Connection")
                        st.write("**Processing:** Local Query Processing")
                    st.write(f"**Filters Applied:** {', '.join(selected_schemes) if selected_schemes else 'None'}")
                    st.write(f"**Timestamp:** {chat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

def reports_page():
    st.header("Reports & Dashboards")
    
    # Get real data if database is connected
    db = get_database()
    if db is not None and st.session_state.get('db_connected', False):
        try:
            # Load real metrics from database using new methods
            total_citizens = db.get_citizens_count()
            total_disbursements = db.get_total_disbursements()
            active_schemes = db.get_active_schemes_count()
            total_enrollments = db.get_total_enrollments()
            
            schemes_real = db.get_schemes()
            disbursements_real = db.get_disbursements_summary()
            
            # KPI Cards with real data
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Citizens", f"{total_citizens:,}", "Real Data")
            
            with col2:
                st.metric("Total Disbursements", f"₹{total_disbursements:,.2f}", "Real Data")
            
            with col3:
                st.metric("Active Schemes", str(active_schemes), "Real Data")
            
            with col4:
                st.metric("Total Enrollments", f"{total_enrollments:,}", "Real Data")
            
            st.success("Displaying real-time data from connected database")
            
            # Use real data for charts
            chart_data = schemes_real if not schemes_real.empty else schemes_data
            
        except Exception as e:
            # Fall back to sample data silently
            chart_data = schemes_data
            
            # KPI Cards with sample data
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Enrollments", "205", "↗️ +12")
            
            with col2:
                disbursement_col = 'total_disbursements' if 'total_disbursements' in schemes_data.columns else 'disbursements'
                total_amount = schemes_data[disbursement_col].sum()
                st.metric("Total Disbursements", f"₹{total_amount:,.2f}", "↗️ Sample Data")
            
            with col3:
                st.metric("Active Schemes", "5", "→ 0")
            
            with col4:
                st.metric("Beneficiaries", "300", "↗️ +25")
            
            st.info("Displaying sample data. Connect to database for real-time metrics.")
    else:
        # Sample data KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Enrollments", "205", "↗️ +12")
        
        with col2:
            disbursement_col = 'total_disbursements' if 'total_disbursements' in schemes_data.columns else 'disbursements'
            total_amount = schemes_data[disbursement_col].sum()
            st.metric("Total Disbursements", f"₹{total_amount:,.2f}", "Sample Data")
        
        with col3:
            st.metric("Active Schemes", "5", "→ 0")
        
        with col4:
            st.metric("Beneficiaries", "300", "↗️ +25")
        
        st.info("Displaying sample data. Connect to database for real-time metrics.")
        chart_data = schemes_data
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Scheme Comparison")
        enrollments_col = 'total_enrollments' if 'total_enrollments' in chart_data.columns else 'enrollments'
        if enrollments_col in chart_data.columns:
            fig = px.bar(chart_data, x='scheme_name', y=enrollments_col, title="Enrollments by Scheme")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Enrollment data not available")
    
    with col2:
        st.subheader("Disbursement Distribution")
        disbursement_col = 'total_disbursements' if 'total_disbursements' in chart_data.columns else 'disbursements'
        if disbursement_col in chart_data.columns:
            fig = px.pie(chart_data, names='scheme_name', values=disbursement_col, title="Disbursements by Scheme")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Disbursement data not available")
    
    # Export dashboard
    if st.button("Export Dashboard"):
        st.success("Dashboard export feature will be implemented")
    
    # Add citizen search section
    st.divider()
    st.subheader("Citizen Search")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("Search by name or Aadhaar number", placeholder="Enter name or Aadhaar...")
    with col2:
        search_district = st.selectbox("Filter by district", ["All"] + districts_list)
    
    if search_term:
        db = get_database()
        if st.session_state.get('db_connected', False):
            try:
                search_district_filter = None if search_district == "All" else search_district
                results = db.search_citizens(search_term, search_district_filter)
                
                if results is not None and not results.empty:
                    st.success(f"Found {len(results)} citizen(s)")
                    st.dataframe(results, use_container_width=True)
                else:
                    st.info("No citizens found matching your search criteria")
            except Exception as e:
                st.error(f"Search error: {str(e)}")
        else:
            st.warning("Database not connected. Please configure database connection to search citizens.")

def database_page():
    # Check if user has database access using RBAC system
    if not rbac.check_feature_access('database_query'):
        st.error("Access denied. This page requires database query permissions.")
        rbac.require_feature_access('database_query')
        return
    
    st.header("Database Explorer")
    
    # Check if database is connected globally
    if not st.session_state.get('global_db_connected', False):
        st.error("Database connection failed. Please check your Azure SQL Database credentials.")
        return
    
    # Use Azure connection instead of old database module
    # Get list of tables from database
    try:
        tables_query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE' 
        ORDER BY TABLE_NAME
        """
        tables_result = execute_query(tables_query)
        if tables_result:
            available_tables = [row['TABLE_NAME'] for row in tables_result]
        else:
            available_tables = ['citizens', 'schemes', 'enrollments', 'disbursements', 'officers', 'states', 'districts', 'villages']
    except Exception as e:
        st.error(f"Error fetching table list: {str(e)}")
        available_tables = ['citizens', 'schemes', 'enrollments', 'disbursements', 'officers', 'states', 'districts', 'villages']
    
    # Left pane: Tables list
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Database Tables")
        if available_tables:
            selected_table = st.selectbox("Select Table", available_tables)
            
            # Show table count
            try:
                count_query = f"SELECT COUNT(*) as row_count FROM [{selected_table}]"
                count_result = execute_query(count_query)
                if count_result:
                    row_count = count_result[0]['row_count']
                    st.metric("Total Rows", f"{row_count:,}")
            except Exception as e:
                st.error(f"Error counting rows: {str(e)}")
        else:
            st.info("No tables found in database")
            return
    
    with col2:
        st.subheader(f"Table: {selected_table}")
        
        # Add controls for data viewing
        col2a, col2b = st.columns([2, 1])
        with col2a:
            limit = st.selectbox("Show rows:", [10, 25, 50, 100, 500], index=1)
        with col2b:
            if st.button("Refresh Data"):
                st.cache_data.clear()
        
        # Show table data
        try:
            # Get table data with limit
            data_query = f"SELECT TOP {limit} * FROM [{selected_table}] ORDER BY 1"
            table_data = execute_query(data_query)
            
            if table_data:
                # Convert to DataFrame for display
                import pandas as pd
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, height=400)
                
                # Download option - only for users with export permission
                if can_export_data():
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label=f"Download {selected_table} data",
                        data=csv,
                        file_name=f"{selected_table}_data.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("Data export requires analyst or admin role.")
            else:
                st.info(f"No data found in {selected_table} table")
                
        except Exception as e:
            st.error(f"Error loading table data: {str(e)}")
                
        except Exception as e:
            st.error(f"Error loading table data: {str(e)}")
        
        # Table schema information
        with st.expander("Table Schema"):
            try:
                schema_query = f"""
                SELECT 
                    COLUMN_NAME as 'Column Name',
                    DATA_TYPE as 'Data Type',
                    IS_NULLABLE as 'Nullable',
                    COLUMN_DEFAULT as 'Default Value'
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{selected_table}'
                ORDER BY ORDINAL_POSITION
                """
                schema_result = execute_query(schema_query)
                if schema_result:
                    import pandas as pd
                    schema_df = pd.DataFrame(schema_result)
                    st.dataframe(schema_df, use_container_width=True)
                else:
                    st.info("Schema information not available")
            except Exception as e:
                st.error(f"Error loading schema: {str(e)}")
        
        # Table relationships
        with st.expander("Relationships"):
            try:
                fk_query = f"""
                SELECT 
                    OBJECT_NAME(f.parent_object_id) AS 'Table',
                    COL_NAME(fc.parent_object_id, fc.parent_column_id) AS 'Column',
                    OBJECT_NAME(f.referenced_object_id) AS 'Referenced Table',
                    COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS 'Referenced Column'
                FROM sys.foreign_keys AS f
                INNER JOIN sys.foreign_key_columns AS fc ON f.object_id = fc.constraint_object_id
                WHERE OBJECT_NAME(f.parent_object_id) = '{selected_table}'
                   OR OBJECT_NAME(f.referenced_object_id) = '{selected_table}'
                """
                fk_result = execute_query(fk_query)
                if fk_result:
                    import pandas as pd
                    fk_df = pd.DataFrame(fk_result)
                    st.dataframe(fk_df, use_container_width=True)
                else:
                    st.info("No foreign key relationships found")
            except Exception as e:
                st.error(f"Error loading relationships: {str(e)}")
    
    # Quick analytics section
    st.divider()
    st.subheader("Quick Analytics")
    
    analytics_col1, analytics_col2, analytics_col3 = st.columns(3)
    
    with analytics_col1:
        st.write("**Data Distribution**")
        if selected_table == 'citizens':
            try:
                gender_query = "SELECT gender, COUNT(*) as count FROM citizens GROUP BY gender"
                gender_data = execute_query(gender_query)
                if gender_data:
                    import pandas as pd
                    gender_df = pd.DataFrame(gender_data)
                    fig = px.pie(gender_df, names='gender', values='count', title="Citizens by Gender")
                    st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Gender distribution chart not available")
        elif selected_table == 'schemes':
            try:
                sector_query = "SELECT sector, COUNT(*) as count FROM schemes GROUP BY sector"
                sector_data = execute_query(sector_query)
                if sector_data:
                    fig = px.bar(sector_data, x='sector', y='count', title="Schemes by Sector")
                    st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Sector distribution chart not available")
        else:
            st.info("Analytics not available for this table")
    
    with analytics_col2:
        st.write("**Record Counts**")
        try:
            # Get counts for all major tables
            tables_to_count = ['citizens', 'schemes', 'enrollments', 'disbursements']
            counts = []
            for table in tables_to_count:
                try:
                    count_query = f"SELECT COUNT(*) as count FROM [{table}]"
                    result = execute_query(count_query)
                    if result:
                        counts.append({'Table': table, 'Count': result[0]['count']})
                except:
                    continue
            
            if counts:
                import pandas as pd
                counts_df = pd.DataFrame(counts)
                st.dataframe(counts_df, use_container_width=True)
        except:
            st.info("Count summary not available")
    
    with analytics_col3:
        st.write("**Data Quality**")
        try:
            if selected_table in available_tables:
                # Check for null values in the selected table
                null_query = f"""
                SELECT 
                    SUM(CASE WHEN [name] IS NULL THEN 1 ELSE 0 END) as null_names
                FROM [{selected_table}]
                WHERE 'name' IN (SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{selected_table}')
                """
                # Simplified quality check
                quality_info = [
                    f"Table: {selected_table}",
                    f"Rows: {row_count:,}" if 'row_count' in locals() else "Rows: Unknown"
                ]
                for info in quality_info:
                    st.write(f"• {info}")
        except:
            st.info("Data quality metrics not available")

def admin_page():
    """Admin page with Auth0 integration and RBAC"""
    # Require admin role
    if not is_admin():
        st.error("**Access Denied**: Administrator role required")
        st.info("Contact your system administrator to request admin access.")
        return
    
    st.header("Admin & System Management")
    
    # Show current user info
    user = get_current_user()
    st.info(f"**Admin:** {user.get('name', 'Unknown')} ({user.get('email', 'No email')})")
    
    # Tab navigation for admin functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["User Management", "Access Control", "System Monitoring", "Access Logs", "Settings"])
    
    with tab1:
        st.subheader("User Management")
        
        # Import auth_manager for user management functions
        from in_app_auth import auth_manager
        
        # User management sub-tabs
        user_tab1, user_tab2, user_tab3 = st.tabs(["View Users", "Add User", "Edit Users"])
        
        with user_tab1:
            st.markdown("### Current Users")
            users = auth_manager.get_all_users()
            
            if users:
                # Create user table
                user_data = []
                for email, user_info in users.items():
                    user_data.append({
                        'Email': email,
                        'Name': user_info.get('name', ''),
                        'Roles': ', '.join(user_info.get('roles', [])),
                        'Status': 'Active' if user_info.get('active', True) else 'Inactive',
                        'Last Login': user_info.get('last_login', 'Never')[:19] if user_info.get('last_login') else 'Never',
                        'Created': user_info.get('created_at', '')[:19] if user_info.get('created_at') else ''
                    })
                
                df = pd.DataFrame(user_data)
                st.dataframe(df, use_container_width=True)
                
                st.info(f"Total Users: {len(users)}")
            else:
                st.warning("No users found.")
        
        with user_tab2:
            st.markdown("### Add New User")
            
            with st.form("add_user_form"):
                new_email = st.text_input("Email Address", placeholder="user@company.com")
                new_name = st.text_input("Full Name", placeholder="John Doe")
                new_password = st.text_input("Password", type="password", placeholder="Minimum 8 characters")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                # Role selection
                available_roles = ["admin", "analyst", "officer", "user"]
                selected_roles = st.multiselect("Assign Roles", available_roles, default=["user"])
                
                # Role descriptions
                st.markdown("""
                **Role Descriptions:**
                - **Admin**: Full system access, user management
                - **Analyst**: Data analysis and querying capabilities  
                - **Officer**: Welfare operations and citizen data access
                - **User**: Basic access with limited permissions
                """)
                
                submit_user = st.form_submit_button("Create User", type="primary")
                
                if submit_user:
                    # Validation
                    if not new_email or not new_name or not new_password:
                        st.error("Please fill in all required fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 8:
                        st.error("Password must be at least 8 characters long")
                    elif not selected_roles:
                        st.error("Please assign at least one role")
                    else:
                        success = auth_manager.create_user(new_email, new_password, new_name, selected_roles)
                        if success:
                            st.success(f"User {new_email} created successfully!")
                            st.rerun()
                        else:
                            st.error("User already exists or creation failed")
        
        with user_tab3:
            st.markdown("### Edit Existing Users")
            
            users = auth_manager.get_all_users()
            if users:
                # User selection
                user_emails = list(users.keys())
                selected_email = st.selectbox("Select User to Edit", user_emails)
                
                if selected_email:
                    user_info = users[selected_email]
                    
                    # Edit form
                    with st.form(f"edit_user_{selected_email}"):
                        st.markdown(f"**Editing:** {selected_email}")
                        
                        edit_name = st.text_input("Full Name", value=user_info.get('name', ''))
                        available_roles = ["admin", "analyst", "officer", "user"]
                        current_roles = user_info.get('roles', [])
                        edit_roles = st.multiselect("Roles", available_roles, default=current_roles)
                        edit_active = st.checkbox("Active User", value=user_info.get('active', True))
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            update_user = st.form_submit_button("Update User", type="primary")
                        
                        with col2:
                            reset_password = st.form_submit_button("Reset Password", type="secondary")
                        
                        with col3:
                            delete_user = st.form_submit_button("Delete User", type="secondary")
                        
                        if update_user:
                            success = auth_manager.update_user(selected_email, edit_name, edit_roles, edit_active)
                            if success:
                                st.success("User updated successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to update user")
                        
                        if reset_password:
                            new_temp_password = st.text_input("New Password", type="password", key="new_pwd")
                            if new_temp_password:
                                if len(new_temp_password) >= 8:
                                    success = auth_manager.reset_user_password(selected_email, new_temp_password)
                                    if success:
                                        st.success("Password reset successfully!")
                                    else:
                                        st.error("Failed to reset password")
                                else:
                                    st.error("Password must be at least 8 characters long")
                        
                        if delete_user:
                            if selected_email == auth_manager.get_current_user().get('email'):
                                st.error("Cannot delete your own account!")
                            else:
                                # Confirmation
                                if st.checkbox(f"I confirm deletion of {selected_email}", key="confirm_delete"):
                                    success = auth_manager.delete_user(selected_email)
                                    if success:
                                        st.success("User deleted successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete user")
            else:
                st.info("No users available to edit.")
    
    with tab2:
        st.subheader("Role-Based Access Control")
        show_access_control_panel()
    
    with tab3:
        st.subheader("System Monitoring")
        
        # Service health
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Database Status", "Connected" if st.session_state.get('db_connected') else "Disconnected")
            st.metric("Auth0 Status", "Connected")
        
        with col2:
            st.metric("Total Queries Today", "47", "↗️ +12")
            st.metric("Avg Response Time", "1.2s", "↓ -0.3s")
        
        with col3:
            st.metric("System Uptime", "99.9%", "↗️ +0.1%")
            st.metric("Error Rate", "0.1%", "↓ -0.05%")
        
        # Recent activity
        st.markdown("### Recent Activity")
        activity_data = pd.DataFrame({
            'Time': ['10:45 AM', '10:32 AM', '10:18 AM', '10:05 AM'],
            'User': ['analyst', 'officer', 'admin', 'analyst'],
            'Action': ['Query: citizen count', 'Login', 'User added', 'Database export'],
            'Status': ['Success', 'Success', 'Success', 'Success']
        })
        st.dataframe(activity_data, use_container_width=True)
    
    with tab4:
        st.subheader("Access Logs")
        
        # Access logs summary stats
        stats = access_logger.get_summary_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Events", stats['total_events'])
        with col2:
            st.metric("Unique Users", stats['unique_users'])
        with col3:
            st.metric("Login Events", stats['login_events'])
        with col4:
            st.metric("Recent Activity (24h)", stats['recent_activity'])
        
        st.divider()
        
        # Filters for log viewing
        col1, col2, col3 = st.columns(3)
        
        with col1:
            event_filter = st.selectbox(
                "Event Type:", 
                ["All", "login", "logout", "query", "export", "page_access", "admin_action", "security"],
                index=0
            )
        
        with col2:
            # Get list of users for filter
            all_logs = access_logger.get_logs(limit=1000)
            unique_users = list(set([log.get('user_email', 'Unknown') for log in all_logs if log.get('user_email') != 'Anonymous']))
            unique_users.insert(0, "All Users")
            user_filter = st.selectbox("User:", unique_users, index=0)
        
        with col3:
            days_back = st.selectbox("Time Range:", [1, 7, 30, 90, 365], index=1, format_func=lambda x: f"Last {x} days")
        
        # Apply filters
        event_type_filter = None if event_filter == "All" else event_filter
        user_email_filter = None if user_filter == "All Users" else user_filter
        start_date = (datetime.now() - timedelta(days=days_back)).date()
        
        # Get filtered logs
        logs_df = access_logger.get_logs_dataframe(
            limit=200,
            event_type=event_type_filter,
            user_email=user_email_filter,
            start_date=start_date
        )
        
        if not logs_df.empty:
            st.dataframe(logs_df, use_container_width=True, height=400)
            
            # Export logs functionality
            if st.button("Export Logs as CSV"):
                csv_data = logs_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"access_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                log_admin_action("Export access logs", "CSV export")
        else:
            st.info("No logs found matching the selected criteria.")
        
        # Real-time log monitoring toggle
        if st.checkbox("Enable Real-time Monitoring (refresh every 30 seconds)"):
            time.sleep(30)
            st.rerun()
    
    with tab5:
        st.subheader("System Settings")
        
        # Application settings
        st.markdown("### Application Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            session_timeout = st.number_input("Session Timeout (hours)", min_value=1, max_value=24, value=8)
            max_query_results = st.number_input("Max Query Results", min_value=10, max_value=1000, value=100)
        
        with col2:
            enable_voice = st.checkbox("Enable Voice Input", value=True)
            enable_exports = st.checkbox("Enable Data Exports", value=True)
        
        if st.button("Save Settings", type="primary"):
            st.success("Settings saved successfully!")
        
        st.divider()
        
        # System maintenance
        st.markdown("### System Maintenance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear All Sessions", type="secondary"):
                st.info("All user sessions cleared")
            
            if st.button("Clear Chat History", type="secondary"):
                st.session_state.chat_history = []
                st.success("Chat history cleared")
        
        with col2:
            if st.button("Generate System Report", type="secondary"):
                st.info("System report generated")
            
            if st.button("Restart Application", type="secondary"):
                st.warning("Application restart requested")

def help_page():
    st.header("Help & About")
    
    # How to ask questions
    st.subheader("How to Ask Good Questions")
    st.write("""
    **Good examples:**
    - "How many citizens are enrolled in MGNREGA?"
    - "Show me disbursements for PMAY in Maharashtra"
    - "List all schemes with their beneficiary counts"
    
    **Tips:**
    - Be specific about what you want to know
    - Mention scheme names clearly
    - Use simple, natural language
    """)
    
    st.divider()
    
    # Glossary
    st.subheader("Glossary")
    
    with st.expander("Welfare Schemes"):
        st.write("**MGNREGA:** Rural employment guarantee scheme")
        st.write("**PMAY:** Housing scheme for affordable homes")
        st.write("**Ujjwala:** LPG connection scheme for women")
        st.write("**Ayushman Bharat:** Health insurance scheme")
        st.write("**NSAP:** Social security pensions")
    
    with st.expander("Terms"):
        st.write("**Enrollment:** Registration in a welfare scheme")
        st.write("**Disbursement:** Payment made to beneficiary")
        st.write("**BPL:** Below Poverty Line")
        st.write("**APL:** Above Poverty Line")

# Main app logic
def main():
    # Check in-app authentication first
    if not require_in_app_authentication():
        return
    
    # Get current user for access logging
    current_user = get_current_user()
    
    # Log successful login (only once per session)
    if current_user and not st.session_state.get('last_login_logged', False):
        log_login(current_user)
        st.session_state.last_login_logged = True
    
    # Show API connection status popup
    show_api_status_popup()
    
    selected_schemes, selected_regions, date_from, date_to = create_sidebar()
    
    # Navigation with role-based access using RBAC system
    available_pages = []
    
    # Basic pages available to all authenticated users
    if rbac.check_feature_access('natural_language_query'):
        available_pages.append("Query")
    
    if rbac.check_feature_access('view_reports'):
        available_pages.append("Reports")
    
    # Advanced features based on permissions
    if rbac.check_feature_access('database_query'):
        available_pages.append("Database")
    
    # Admin-only features
    if rbac.check_feature_access('user_management'):
        available_pages.append("Admin")
    
    # Help is always available
    available_pages.append("Help")
    
    # If no pages available, show access denied
    if not available_pages:
        st.error("No accessible features. Contact your administrator.")
        return
    
    # Add connection status to navigation
    db_status = "Connected" if st.session_state.get('db_connected', False) else "Not Connected"
    api_status = "Connected" if st.session_state.get('api_connected', False) else "Disconnected"
    st.sidebar.markdown(f"**Database:** {db_status}")
    st.sidebar.markdown(f"**API Backend:** {api_status}")
    
    selected_page = st.selectbox("Navigate to:", available_pages, label_visibility="collapsed")
    
    # Log page access (only if different from last page)
    if st.session_state.get('current_page') != selected_page:
        log_page_access(selected_page)
        st.session_state.current_page = selected_page
    
    # Page routing with role-based access control
    if selected_page == "Query":
        # Check if user can access natural language queries
        if rbac.check_feature_access('natural_language_query'):
            ask_page(selected_schemes)
        else:
            log_security_event(f"Unauthorized access attempt to Query page")
            st.error("Access denied to Query feature")
    
    elif selected_page == "Reports":
        if rbac.check_feature_access('view_reports'):
            reports_page()  # Will implement this
        else:
            log_security_event(f"Unauthorized access attempt to Reports page")
            st.error("Access denied to Reports feature")
    
    elif selected_page == "Database":
        if rbac.check_feature_access('database_query'):
            database_page()  # Will implement this
        else:
            log_security_event(f"Unauthorized access attempt to Database page")
            st.error("Access denied to Database feature")
    
    elif selected_page == "Admin":
        if rbac.check_feature_access('user_management'):
            admin_page()
        else:
            log_security_event(f"Unauthorized access attempt to Admin panel")
            st.error("Access denied to Admin panel")
    
    elif selected_page == "Help":
        help_page()  # Will implement this

def help_page():
    """Help page"""
    st.header("Help & Documentation")
    st.markdown("""
    ## Getting Started
    
    Welcome to the Public Welfare Assistant! This platform provides secure access to database analytics with AI-powered natural language queries.
    
    ### Features:
    - **Natural Language Queries**: Ask questions in plain English
    - **Role-Based Access**: Different permissions based on your role
    - **Data Export**: Download results in CSV/Excel formats
    - **Real-time Analytics**: Live data insights and visualizations
    
    ### User Roles:
    - **Admin**: Full system access and user management
    - **Analyst**: Data analysis and advanced querying
    - **Viewer**: Read-only access to data and reports  
    - **User**: Basic access with limited permissions
    
    ### Support:
    For technical support or questions, contact your system administrator.
    """)

if __name__ == "__main__":
    main()
