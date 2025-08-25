import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
import secrets

# File-based authentication system
AUTH_FILE = "config/users.json"
SESSION_FILE = "config/sessions.json"

def ensure_config_dir():
    """Ensure config directory exists"""
    os.makedirs("config", exist_ok=True)

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    ensure_config_dir()
    try:
        if os.path.exists(AUTH_FILE):
            with open(AUTH_FILE, 'r') as f:
                return json.load(f)
        else:
            # Create default users if file doesn't exist
            default_users = {
                "admin": {
                    "password_hash": hash_password("admin123"),
                    "role": "Admin",
                    "district": "Mumbai",
                    "name": "System Administrator",
                    "created": datetime.now().isoformat()
                },
                "analyst": {
                    "password_hash": hash_password("analyst123"),
                    "role": "Analyst",
                    "district": "Mumbai",
                    "name": "Data Analyst",
                    "created": datetime.now().isoformat()
                },
                "officer": {
                    "password_hash": hash_password("officer123"),
                    "role": "Officer",
                    "district": "Bangalore",
                    "name": "Welfare Officer",
                    "created": datetime.now().isoformat()
                }
            }
            save_users(default_users)
            return default_users
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")
        return {}

def save_users(users):
    """Save users to JSON file"""
    ensure_config_dir()
    try:
        with open(AUTH_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        st.error(f"Error saving users: {str(e)}")

def authenticate_user(username: str, password: str):
    """Authenticate user with username and password"""
    users = load_users()
    
    if username in users:
        stored_hash = users[username]["password_hash"]
        if stored_hash == hash_password(password):
            return {
                "username": username,
                "role": users[username]["role"],
                "district": users[username]["district"],
                "name": users[username]["name"]
            }
    return None

def create_session(user_info):
    """Create a session for authenticated user"""
    session_id = secrets.token_urlsafe(32)
    session_data = {
        "session_id": session_id,
        "user_info": user_info,
        "created": datetime.now().isoformat(),
        "expires": (datetime.now() + timedelta(hours=8)).isoformat()
    }
    
    # Store in session state
    st.session_state.session_id = session_id
    st.session_state.user_authenticated = True
    st.session_state.user_role = user_info["role"]
    st.session_state.user_district = user_info["district"]
    st.session_state.user_name = user_info["name"]
    st.session_state.username = user_info["username"]
    
    return session_id

def logout_user():
    """Logout current user"""
    # Clear session state
    st.session_state.session_id = None
    st.session_state.user_authenticated = False
    st.session_state.user_role = None
    st.session_state.user_district = None
    st.session_state.user_name = None
    st.session_state.username = None

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('user_authenticated', False)

def require_auth(allowed_roles=None):
    """Decorator/function to require authentication"""
    if not is_authenticated():
        return False
    
    if allowed_roles:
        user_role = st.session_state.get('user_role')
        if user_role not in allowed_roles:
            return False
    
    return True

def show_login_page():
    """Display the login page"""
    st.title("🏛️ Welfare Data Assistant")
    st.subheader("Secure Login")
    
    # Create columns for centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.markdown("### Login to your account")
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submit_button = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit_button:
                if username and password:
                    user_info = authenticate_user(username, password)
                    if user_info:
                        create_session(user_info)
                        st.success(f"Welcome back, {user_info['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
        
        # Show demo credentials
        with st.expander("🔑 Demo Credentials"):
            st.markdown("""
            **Demo Accounts:**
            
            **Administrator:**
            - Username: `admin`
            - Password: `admin123`
            - Role: Admin (Full Access)
            
            **Data Analyst:**
            - Username: `analyst`
            - Password: `analyst123`
            - Role: Analyst (Reports + Database)
            
            **Welfare Officer:**
            - Username: `officer`
            - Password: `officer123`
            - Role: Officer (Basic Access)
            """)
        
        # System info
        st.markdown("---")
        st.markdown("**System Features:**")
        st.markdown("• 🔒 Secure file-based authentication")
        st.markdown("• 👥 Role-based access control")
        st.markdown("• 🗄️ Database integration ready")
        st.markdown("• 🎤 Voice-enabled queries")

def show_user_profile():
    """Show user profile in sidebar"""
    if is_authenticated():
        st.sidebar.markdown("---")
        st.sidebar.markdown("**👤 User Profile**")
        st.sidebar.markdown(f"**Name:** {st.session_state.get('user_name', 'Unknown')}")
        st.sidebar.markdown(f"**Role:** {st.session_state.get('user_role', 'Unknown')}")
        st.sidebar.markdown(f"**District:** {st.session_state.get('user_district', 'Unknown')}")
        
        if st.sidebar.button("🚪 Logout", type="primary"):
            logout_user()
            st.rerun()

def add_user(username: str, password: str, role: str, district: str, name: str):
    """Add a new user (Admin only)"""
    if not require_auth(['Admin']):
        return False, "Admin access required"
    
    users = load_users()
    
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        "password_hash": hash_password(password),
        "role": role,
        "district": district,
        "name": name,
        "created": datetime.now().isoformat()
    }
    
    save_users(users)
    return True, "User created successfully"

def update_user_password(username: str, new_password: str):
    """Update user password"""
    current_user = st.session_state.get('username')
    user_role = st.session_state.get('user_role')
    
    # Users can update their own password, or admins can update any password
    if current_user != username and user_role != 'Admin':
        return False, "Permission denied"
    
    users = load_users()
    
    if username not in users:
        return False, "User not found"
    
    users[username]["password_hash"] = hash_password(new_password)
    users[username]["modified"] = datetime.now().isoformat()
    
    save_users(users)
    return True, "Password updated successfully"

def list_users():
    """List all users (Admin only)"""
    if not require_auth(['Admin']):
        return []
    
    users = load_users()
    user_list = []
    
    for username, user_data in users.items():
        user_list.append({
            "username": username,
            "name": user_data["name"],
            "role": user_data["role"],
            "district": user_data["district"],
            "created": user_data.get("created", "Unknown")
        })
    
    return user_list
