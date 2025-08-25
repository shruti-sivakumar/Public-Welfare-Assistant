import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
from io import BytesIO
import requests

# Import our modules
from frontend.database import get_database
from frontend.database_config import show_database_config, check_database_connection
from frontend.auth import (
    show_login_page, 
    is_authenticated, 
    require_auth, 
    show_user_profile,
    logout_user,
    add_user,
    update_user_password,
    list_users
)

# Page config
st.set_page_config(
    page_title="Welfare Database Interface",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    if 'db_connected' not in st.session_state:
        st.session_state.db_connected = False
    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = False

# Check API connection
def check_api_connection():
    """Check if the FastAPI backend is running"""
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=30)
        if response.status_code == 200:
            st.session_state.api_connected = True
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
    
    # Show status in sidebar
    with st.sidebar:
        st.divider()
        st.subheader("🔗 API Connection Status")
        
        if is_connected:
            st.success("✅ FastAPI Backend Connected")
            st.write("Backend URL: http://127.0.0.1:8080")
        else:
            st.error("❌ FastAPI Backend Disconnected")
            st.warning("Please start the FastAPI server")
            
            with st.expander("📋 How to start the backend"):
                st.code("""
# Navigate to project directory
cd "C:\\Users\\vidan\\Desktop\\SEM-5\\DBMS\\DBMS + CLOUD"

# Activate virtual environment
.venv\\Scripts\\activate

# Start FastAPI server
cd app
uvicorn main:app --reload
                """, language="bash")
        
        # Refresh button
        if st.button("🔄 Refresh Connection", type="secondary"):
            st.rerun()
    
    # Show modal-style notification if disconnected
    if not is_connected:
        # Use a container for better visibility
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.error("⚠️ API Backend Not Available")
                st.info("Some features may not work properly without the FastAPI backend connection.")
    
    return is_connected

init_session_state()

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

# Authentication
def show_login():
    """Redirect to new authentication system"""
    show_login_page()

# Sidebar
def create_sidebar():
    with st.sidebar:
        # Logo and title
        st.header("🏛️ Welfare Database")
        
        # Show user profile
        show_user_profile()
        
        st.divider()
        
        # Global filters
        st.subheader("🔍 Global Filters")
        
        # Date range
        date_from = st.date_input("From Date", datetime.now() - timedelta(days=30))
        date_to = st.date_input("To Date", datetime.now())
        
        # Scheme filter with error handling
        try:
            scheme_options = schemes_data['name'].tolist() if not schemes_data.empty else []
            default_schemes = scheme_options[:3] if len(scheme_options) > 3 else scheme_options  # Limit defaults to avoid UI clutter
            
            selected_schemes = st.multiselect(
                "Schemes",
                options=scheme_options,
                default=default_schemes
            )
        except Exception as e:
            st.error(f"Error loading schemes: {str(e)}")
            selected_schemes = []
        
        # Region filter with robust error handling
        try:
            user_district = st.session_state.get('user_district', '')
            
            # Ensure we have districts list
            if not districts_list:
                st.warning("No districts available")
                selected_regions = []
            else:
                # Check if user district is valid
                if user_district and user_district in districts_list:
                    default_regions = [user_district]
                else:
                    # Safe fallback to first few districts
                    default_regions = districts_list[:1]  # Just use first district as default
                
                selected_regions = st.multiselect(
                    "Regions",
                    options=districts_list,
                    default=default_regions,
                    help="Select one or more districts to filter data"
                )
        except Exception as e:
            st.error(f"Error loading regions: {str(e)}")
            selected_regions = []
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🆕 New Query", use_container_width=True):
                st.session_state.current_query = ""
        with col2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.chat_history = []
        
        if st.button("📊 Export Data", use_container_width=True):
            st.info("Export functionality will be implemented")
            st.rerun()
    
    return selected_schemes, selected_regions, date_from, date_to


# Main pages
def ask_page(selected_schemes):
    st.header("💬 Database Query Interface")
    
    # Show connection status
    api_connected = st.session_state.get('api_connected', False)
    db_connected = st.session_state.get('db_connected', False)
    
    if api_connected:
        st.success("🚀 Using FastAPI Backend for enhanced query processing")
    elif db_connected:
        st.info("📊 Using direct database connection")
    else:
        st.warning("⚠️ Limited functionality - No backend connection")
    

    # Speech-to-text uploader
    st.subheader("🎤 Voice Query (Speech-to-Text)")
    audio_file = st.file_uploader("Upload a .wav file for voice query", type=["wav"], key="voice_query_upload")
    transcribed_text = ""
    if audio_file:
        files = {"file": audio_file}
        try:
            response = requests.post("http://127.0.0.1:8080/speech-to-text", files=files, timeout=30)
            if response.status_code == 200:
                transcribed_text = response.json().get("text", "")
                st.success(f"Transcribed Text: {transcribed_text}")
                # Option to use transcribed text as query
                if st.button("Use as Query"):
                    st.session_state.current_query = transcribed_text
            else:
                st.error(f"Speech-to-text API error: {response.status_code}")
        except Exception as e:
            st.error(f"Speech-to-text request failed: {str(e)}")

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
            response = requests.post(
                "http://127.0.0.1:8080/nl2sql",
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
        # Add to chat history
        st.session_state.chat_history.append({
            'timestamp': datetime.now(),
            'query': query,
            'response': None,
            'source': 'api' if api_connected else 'db'
        })
        
        # Get response
        with st.spinner("Querying database..."):
            response = None
            
            if api_connected:
                # Use FastAPI backend
                api_response = query_api_backend(query)
                if api_response and api_response.get('success'):
                    response = {
                        'summary': api_response.get('summary', 'Query executed successfully'),
                        'data': pd.DataFrame(api_response.get('data', [])),
                        'sql': api_response.get('sql', ''),
                        'chart_type': api_response.get('chart_type', 'table')
                    }
                else:
                    st.error("Failed to get response from API backend")
                    st.session_state.chat_history.pop()
                    
            elif db_connected:
                # Fallback to direct database connection
                try:
                    db = get_database()
                    response = db.natural_language_query(query)
                    st.session_state.chat_history[-1]['response'] = response
                except Exception as e:
                    st.error(f"Database query failed: {str(e)}")
                    st.session_state.chat_history.pop()
            else:
                st.warning("No backend connection available. Please start the FastAPI server or configure database connection.")
                st.session_state.chat_history.pop()
            
            if response:
                st.session_state.chat_history[-1]['response'] = response
    
    # Display query results
    st.subheader("� Query Results")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        # User query
        with st.chat_message("user"):
            st.write(f"**{chat['timestamp'].strftime('%H:%M')}:** {chat['query']}")
        
        # Database response
        if chat['response']:
            with st.chat_message("assistant"):
                st.write(chat['response']['summary'])
            
            # Query details
            with st.expander("📊 View Details", expanded=(i == 0)):
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["📋 Table", "📈 Chart", "💾 SQL"])
                
                with tab1:
                    if not chat['response']['data'].empty:
                        st.dataframe(chat['response']['data'], use_container_width=True)
                        
                        # Download options
                        col1, col2 = st.columns(2)
                        with col1:
                            csv = chat['response']['data'].to_csv(index=False)
                            st.download_button("📄 Download CSV", csv, f"query_result_{i}.csv", "text/csv")
                        with col2:
                            buffer = BytesIO()
                            chat['response']['data'].to_excel(buffer, index=False)
                            st.download_button("📊 Download Excel", buffer.getvalue(), f"query_result_{i}.xlsx")
                
                with tab2:
                    if not chat['response']['data'].empty:
                        chart_type = chat['response']['chart_type']
                        data = chat['response']['data']
                        
                        if chart_type == 'bar' and len(data.columns) >= 2:
                            fig = px.bar(data, x=data.columns[0], y=data.columns[-1])
                            st.plotly_chart(fig, use_container_width=True)
                        elif chart_type == 'pie' and len(data.columns) >= 2:
                            fig = px.pie(data, names=data.columns[0], values=data.columns[-1])
                            st.plotly_chart(fig, use_container_width=True)
                        elif chart_type == 'metric':
                            st.metric(label="Result", value=data.iloc[0, 0])
                        else:
                            st.info("No chart available for this data type")
                
                with tab3:
                    st.code(chat['response']['sql'], language='sql')
                
                # Query information
                with st.expander("ℹ️ Query Information"):
                    source = chat.get('source', 'db')
                    if source == 'api':
                        st.write("**Data Source:** FastAPI Backend")
                        st.write("**Processing:** Enhanced AI Query Processing")
                    else:
                        st.write("**Data Source:** Direct Database Connection")
                        st.write("**Processing:** Local Query Processing")
                    st.write(f"**Filters Applied:** {', '.join(selected_schemes) if selected_schemes else 'None'}")
                    st.write(f"**Timestamp:** {chat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

def reports_page():
    st.header("📊 Reports & Dashboards")
    
    # Get real data if database is connected
    db = get_database()
    if st.session_state.get('db_connected', False):
        try:
            # Load real metrics from database
            total_citizens = db.get_citizens_count()
            schemes_real = db.get_schemes()
            disbursements_real = db.get_disbursements_summary()
            
            # Calculate metrics
            total_enrollments = schemes_real['total_enrollments'].sum() if not schemes_real.empty else 0
            total_disbursements = schemes_real['total_disbursements'].sum() if not schemes_real.empty else 0
            active_schemes = len(schemes_real) if not schemes_real.empty else 0
            
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
            
            st.success("📊 Displaying real-time data from connected database")
            
            # Use real data for charts
            chart_data = schemes_real if not schemes_real.empty else schemes_data
            
        except Exception as e:
            st.error(f"Error loading real data: {str(e)}")
            # Fall back to sample data
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
            
            st.info("📊 Displaying sample data. Connect to database for real-time metrics.")
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
        
        st.info("📊 Displaying sample data. Connect to database for real-time metrics.")
        chart_data = schemes_data
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Scheme Comparison")
        enrollments_col = 'total_enrollments' if 'total_enrollments' in chart_data.columns else 'enrollments'
        if enrollments_col in chart_data.columns:
            fig = px.bar(chart_data, x='name', y=enrollments_col, title="Enrollments by Scheme")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Enrollment data not available")
    
    with col2:
        st.subheader("🥧 Disbursement Distribution")
        disbursement_col = 'total_disbursements' if 'total_disbursements' in chart_data.columns else 'disbursements'
        if disbursement_col in chart_data.columns:
            fig = px.pie(chart_data, names='name', values=disbursement_col, title="Disbursements by Scheme")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Disbursement data not available")
    
    # Export dashboard
    if st.button("📥 Export Dashboard"):
        st.success("Dashboard export feature will be implemented")
    
    # Add citizen search section
    st.divider()
    st.subheader("🔍 Citizen Search")
    
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
    if st.session_state.user_role not in ['Analyst', 'Admin']:
        st.error("Access denied. This page is only available for Analysts and Admins.")
        return
    
    st.header("🗄️ Database Explorer")
    
    # Check database connection
    if not st.session_state.get('db_connected', False):
        st.warning("⚠️ Database not connected. Please configure your database connection first.")
        if st.button("Go to Database Configuration"):
            st.session_state.current_page = "Database Config"
            st.rerun()
        return
    
    db = get_database()
    
    # Get list of tables from database
    try:
        tables_query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE' 
        ORDER BY TABLE_NAME
        """
        tables_result = db.execute_query(tables_query)
        if tables_result is not None and not tables_result.empty:
            available_tables = tables_result['TABLE_NAME'].tolist()
        else:
            available_tables = ['citizens', 'schemes', 'enrollments', 'disbursements', 'officers', 'states', 'districts', 'villages']
    except Exception as e:
        st.error(f"Error fetching table list: {str(e)}")
        available_tables = ['citizens', 'schemes', 'enrollments', 'disbursements', 'officers', 'states', 'districts', 'villages']
    
    # Left pane: Tables list
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("📋 Database Tables")
        if available_tables:
            selected_table = st.selectbox("Select Table", available_tables)
            
            # Show table count
            try:
                count_query = f"SELECT COUNT(*) as row_count FROM [{selected_table}]"
                count_result = db.execute_query(count_query)
                if count_result is not None and not count_result.empty:
                    row_count = count_result['row_count'].iloc[0]
                    st.metric("Total Rows", f"{row_count:,}")
            except Exception as e:
                st.error(f"Error counting rows: {str(e)}")
        else:
            st.info("No tables found in database")
            return
    
    with col2:
        st.subheader(f"📊 Table: {selected_table}")
        
        # Add controls for data viewing
        col2a, col2b = st.columns([2, 1])
        with col2a:
            limit = st.selectbox("Show rows:", [10, 25, 50, 100, 500], index=1)
        with col2b:
            if st.button("🔄 Refresh Data"):
                st.cache_data.clear()
        
        # Show table data
        try:
            # Get table data with limit
            data_query = f"SELECT TOP {limit} * FROM [{selected_table}] ORDER BY 1"
            table_data = db.execute_query(data_query)
            
            if table_data is not None and not table_data.empty:
                st.dataframe(table_data, use_container_width=True, height=400)
                
                # Download option
                csv = table_data.to_csv(index=False)
                st.download_button(
                    label=f"📥 Download {selected_table} data",
                    data=csv,
                    file_name=f"{selected_table}_data.csv",
                    mime="text/csv"
                )
            else:
                st.info(f"No data found in {selected_table} table")
                
        except Exception as e:
            st.error(f"Error loading table data: {str(e)}")
        
        # Table schema information
        with st.expander("🔍 Table Schema"):
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
                schema_result = db.execute_query(schema_query)
                if schema_result is not None and not schema_result.empty:
                    st.dataframe(schema_result, use_container_width=True)
                else:
                    st.info("Schema information not available")
            except Exception as e:
                st.error(f"Error loading schema: {str(e)}")
        
        # Table relationships
        with st.expander("🔗 Relationships"):
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
                fk_result = db.execute_query(fk_query)
                if fk_result is not None and not fk_result.empty:
                    st.dataframe(fk_result, use_container_width=True)
                else:
                    st.info("No foreign key relationships found")
            except Exception as e:
                st.error(f"Error loading relationships: {str(e)}")
    
    # Quick analytics section
    st.divider()
    st.subheader("📈 Quick Analytics")
    
    analytics_col1, analytics_col2, analytics_col3 = st.columns(3)
    
    with analytics_col1:
        st.write("**Data Distribution**")
        if selected_table == 'citizens':
            try:
                gender_query = "SELECT gender, COUNT(*) as count FROM citizens GROUP BY gender"
                gender_data = db.execute_query(gender_query)
                if gender_data is not None and not gender_data.empty:
                    fig = px.pie(gender_data, names='gender', values='count', title="Citizens by Gender")
                    st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Gender distribution chart not available")
        elif selected_table == 'schemes':
            try:
                sector_query = "SELECT sector, COUNT(*) as count FROM schemes GROUP BY sector"
                sector_data = db.execute_query(sector_query)
                if sector_data is not None and not sector_data.empty:
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
                    result = db.execute_query(count_query)
                    if result is not None and not result.empty:
                        counts.append({'Table': table, 'Count': result['count'].iloc[0]})
                except:
                    continue
            
            if counts:
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
    if not require_auth(['Admin']):
        st.error("Access denied. This page is only available for Admins.")
        return
    
    st.header("⚙️ Admin & User Management")
    
    # Tab navigation for admin functions
    tab1, tab2, tab3 = st.tabs(["👥 User Management", "📊 System Monitoring", "🔧 Settings"])
    
    with tab1:
        st.subheader("User Management")
        
        # User list
        st.markdown("### Current Users")
        users = list_users()
        if users:
            users_df = pd.DataFrame(users)
            st.dataframe(users_df, use_container_width=True)
        else:
            st.info("No users found")
        
        st.divider()
        
        # Add new user
        st.markdown("### Add New User")
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username")
                new_name = st.text_input("Full Name")
                new_role = st.selectbox("Role", ["Officer", "Analyst", "Admin"])
            
            with col2:
                new_password = st.text_input("Password", type="password")
                new_district = st.selectbox("District", districts_list)
            
            if st.form_submit_button("Add User", type="primary"):
                if new_username and new_password and new_name:
                    success, message = add_user(new_username, new_password, new_role, new_district, new_name)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all required fields")
        
        st.divider()
        
        # Change password
        st.markdown("### Change User Password")
        with st.form("change_password_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                target_username = st.selectbox("Select User", [user['username'] for user in users] if users else [])
            
            with col2:
                new_password = st.text_input("New Password", type="password", key="change_pwd")
            
            if st.form_submit_button("Update Password"):
                if target_username and new_password:
                    success, message = update_user_password(target_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Please select user and enter new password")
    
    with tab2:
        st.subheader("System Monitoring")
        
        # Service health
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Database Status", "🟢 Connected" if st.session_state.get('db_connected') else "� Disconnected")
            st.metric("Active Users", len(users) if users else 0)
        
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
            'Status': ['✅ Success', '✅ Success', '✅ Success', '✅ Success']
        })
        st.dataframe(activity_data, use_container_width=True)
    
    with tab3:
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
            if st.button("🧹 Clear All Sessions", type="secondary"):
                st.info("All user sessions cleared")
            
            if st.button("🗑️ Clear Chat History", type="secondary"):
                st.session_state.chat_history = []
                st.success("Chat history cleared")
        
        with col2:
            if st.button("📊 Generate System Report", type="secondary"):
                st.info("System report generated")
            
            if st.button("🔄 Restart Application", type="secondary"):
                st.warning("Application restart requested")

def help_page():
    st.header("❓ Help & About")
    
    # How to ask questions
    st.subheader("💡 How to Ask Good Questions")
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
    st.subheader("📚 Glossary")
    
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
    # Check authentication first
    if not is_authenticated():
        show_login()
        return
    
    # Show API connection status popup
    show_api_status_popup()
    
    selected_schemes, selected_regions, date_from, date_to = create_sidebar()
    
    # Navigation with database config for all users
    page_options = {
        "Officer": ["Query", "Reports", "Database Config", "Help"],
        "Analyst": ["Query", "Reports", "Database Config", "Database", "Help"],
        "Admin": ["Query", "Reports", "Database Config", "Database", "Admin", "Help"]
    }
    
    pages = page_options[st.session_state.user_role]
    
    # Add connection status to navigation
    db_status = "🟢 Connected" if st.session_state.get('db_connected', False) else "🔴 Not Connected"
    api_status = "🟢 Connected" if st.session_state.get('api_connected', False) else "🔴 Disconnected"
    st.sidebar.markdown(f"**Database:** {db_status}")
    st.sidebar.markdown(f"**API Backend:** {api_status}")
    
    selected_page = st.selectbox("Navigate to:", pages, label_visibility="collapsed")
    
    # Page routing
    if selected_page == "Query":
        ask_page(selected_schemes)
    elif selected_page == "Reports":
        reports_page()
    elif selected_page == "Database Config":
        show_database_config()
    elif selected_page == "Database":
        database_page()
    elif selected_page == "Admin":
        admin_page()
    elif selected_page == "Help":
        help_page()

if __name__ == "__main__":
    main()
