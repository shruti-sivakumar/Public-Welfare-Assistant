import streamlit as st
from frontend.database import get_database

def show_database_config():
    """Display database configuration page"""
    st.title("🗄️ Database Configuration")
    
    db = get_database()
    
    with st.form("database_config"):
        st.subheader("Database Connection Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            server = st.text_input(
                "Server Name", 
                value=st.session_state.get('db_server', 'localhost'),
                help="Enter your SQL Server instance name (e.g., localhost, .\\SQLEXPRESS, or IP address)"
            )
            
            database = st.text_input(
                "Database Name", 
                value=st.session_state.get('db_name', 'WelfareDB'),
                help="Enter the name of your welfare database"
            )
        
        with col2:
            auth_type = st.radio(
                "Authentication Type",
                ["Windows Authentication", "SQL Server Authentication"],
                index=0
            )
            
            if auth_type == "SQL Server Authentication":
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
            else:
                username = None
                password = None
        
        submitted = st.form_submit_button("Test Connection", type="primary")
        
        if submitted:
            # Store connection details in session state
            st.session_state.db_server = server
            st.session_state.db_name = database
            
            # Configure and test connection
            if auth_type == "Windows Authentication":
                db.configure_connection(server, database, trusted_connection=True)
            else:
                db.configure_connection(server, database, username, password, trusted_connection=False)
            
            with st.spinner("Testing database connection..."):
                if db.connect():
                    st.success("✅ Database connection successful!")
                    st.session_state.db_connected = True
                    
                    # Test with a simple query
                    try:
                        schemes = db.get_schemes()
                        if schemes is not None and not schemes.empty:
                            st.info(f"Found {len(schemes)} welfare schemes in the database")
                            with st.expander("Preview Schemes Data"):
                                st.dataframe(schemes)
                        else:
                            st.warning("Database connected but no schemes found. Make sure your database is populated with sample data.")
                    except Exception as e:
                        st.warning(f"Connected to database but unable to query schemes: {str(e)}")
                else:
                    st.error("❌ Database connection failed. Please check your settings.")
                    st.session_state.db_connected = False
    
    # Connection status
    if st.session_state.get('db_connected', False):
        st.success("✅ Database is connected and ready to use!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Connection"):
                # Force reconnection
                db.disconnect()
                if db.connect():
                    st.success("Connection refreshed successfully!")
                else:
                    st.error("Failed to refresh connection")
                    st.session_state.db_connected = False
        
        with col2:
            if st.button("❌ Disconnect"):
                db.disconnect()
                st.session_state.db_connected = False
                st.info("Database disconnected")
                st.rerun()
    else:
        st.info("Please configure and test your database connection above.")
    
    # Database setup instructions
    with st.expander("📚 Database Setup Instructions"):
        st.markdown("""
        ### Setting up your SQL Server Database:
        
        1. **Install SQL Server** (if not already installed):
           - Download SQL Server Developer Edition (free)
           - Or use SQL Server Express (free, limited features)
        
        2. **Create the Database**:
           - Run the schema script: `database/01_schema.sql`
           - Populate with sample data: `database/02_sample_data.sql`
           - Or use the comprehensive data: `database/DBMS_Synthetic_data.sql`
        
        3. **Connection Strings**:
           - **Local SQL Server Express**: `.\\SQLEXPRESS`
           - **Local SQL Server**: `localhost` or `.`
           - **Remote Server**: Use IP address or server name
        
        4. **Authentication**:
           - **Windows Authentication** (recommended for local development)
           - **SQL Server Authentication** (for remote or specific user accounts)
        
        ### Troubleshooting:
        - Ensure SQL Server is running
        - Check Windows Firewall settings
        - Verify SQL Server Browser service is running (for named instances)
        - Make sure TCP/IP is enabled in SQL Server Configuration Manager
        """)

def check_database_connection():
    """Check if database is connected and ready"""
    if not st.session_state.get('db_connected', False):
        st.warning("⚠️ Database not connected. Please configure your database connection first.")
        if st.button("Go to Database Configuration"):
            st.session_state.current_page = "Database Config"
            st.rerun()
        return False
    return True
