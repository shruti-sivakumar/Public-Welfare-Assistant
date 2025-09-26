"""
In-App Authentication System
Simple authentication system that works within Streamlit without external redirects
"""

import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
import re

class InAppAuthManager:
    """Simple in-app authentication manager"""
    
    def __init__(self):
        self.users_file = "users.json"  # Store in current directory
        
        # Initialize session state if needed
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
            
        self._ensure_users_file_exists()
    
    def _ensure_users_file_exists(self):
        """Ensure users file exists with default admin user"""
        if not os.path.exists(self.users_file):
            # Only create directory if the file path contains a directory
            dir_path = os.path.dirname(self.users_file)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            default_users = {
                "admin@company.com": {
                    "password_hash": self._hash_password("admin123"),
                    "name": "System Administrator",
                    "roles": ["admin"],
                    "created_at": datetime.now().isoformat(),
                    "last_login": None,
                    "active": True
                },
                "analyst@company.com": {
                    "password_hash": self._hash_password("analyst123"),
                    "name": "Data Analyst",
                    "roles": ["analyst"],
                    "created_at": datetime.now().isoformat(),
                    "last_login": None,
                    "active": True
                },
                "officer@company.com": {
                    "password_hash": self._hash_password("officer123"),
                    "name": "Welfare Officer",
                    "roles": ["officer"],
                    "created_at": datetime.now().isoformat(),
                    "last_login": None,
                    "active": True
                },
                "user@company.com": {
                    "password_hash": self._hash_password("user123"),
                    "name": "Basic User",
                    "roles": ["user"],
                    "created_at": datetime.now().isoformat(),
                    "last_login": None,
                    "active": True
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self) -> dict:
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_users(self, users: dict):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_password(self, password: str) -> tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        return True, ""
    
    def authenticate_user(self, email: str, password: str) -> bool:
        """Authenticate user with email and password"""
        users = self._load_users()
        
        if email in users:
            user_data = users[email]
            if user_data.get('active', True):
                password_hash = self._hash_password(password)
                if user_data['password_hash'] == password_hash:
                    # Update last login
                    users[email]['last_login'] = datetime.now().isoformat()
                    self._save_users(users)
                    
                    # Store user session
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_data = user_data
                    return True
        return False
    
    def create_user(self, email: str, password: str, name: str, roles: list = None) -> tuple[bool, str]:
        """Create new user"""
        if not self._validate_email(email):
            return False, "Invalid email format"
        
        is_valid, error_msg = self._validate_password(password)
        if not is_valid:
            return False, error_msg
        
        users = self._load_users()
        
        if email in users:
            return False, "User already exists"
        
        if roles is None:
            roles = ["user"]
        
        users[email] = {
            "password_hash": self._hash_password(password),
            "name": name,
            "roles": roles,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "active": True
        }
        
        self._save_users(users)
        return True, "User created successfully"
    
    def is_authenticated(self) -> bool:
        """Check if current session is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> dict:
        """Get current user data"""
        if self.is_authenticated():
            user_data = st.session_state.get('user_data', {}).copy()
            user_data['email'] = st.session_state.get('user_email', '')
            return user_data
        return {}
    
    def logout(self):
        """Logout current user"""
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.user_data = None
    
    def has_role(self, role: str) -> bool:
        """Check if current user has specific role"""
        if not self.is_authenticated():
            return False
        
        user_data = self.get_current_user()
        user_roles = user_data.get('roles', [])
        return role.lower() in [r.lower() for r in user_roles]
    
    def get_user_roles(self) -> list:
        """Get current user roles"""
        if not self.is_authenticated():
            return []
        
        user_data = st.session_state.get('user_data', {})
        return user_data.get('roles', [])
    
    def has_role(self, role: str) -> bool:
        """Check if current user has specific role"""
        user_roles = self.get_user_roles()
        return role.lower() in [r.lower() for r in user_roles]
    
    def get_all_users(self) -> dict:
        """Get all users (admin only)"""
        if not self.has_role('admin'):
            return {}
        return self._load_users()
    
    def create_user(self, email: str, password: str, name: str, roles: list) -> bool:
        """Create a new user (admin only)"""
        if not self.has_role('admin'):
            return False
        
        users = self._load_users()
        if email in users:
            return False  # User already exists
        
        users[email] = {
            "password_hash": self._hash_password(password),
            "name": name,
            "roles": roles,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "active": True
        }
        
        self._save_users(users)
        return True
    
    def update_user(self, email: str, name: str = None, roles: list = None, active: bool = None) -> bool:
        """Update user details (admin only)"""
        if not self.has_role('admin'):
            return False
        
        users = self._load_users()
        if email not in users:
            return False
        
        if name is not None:
            users[email]["name"] = name
        if roles is not None:
            users[email]["roles"] = roles
        if active is not None:
            users[email]["active"] = active
        
        self._save_users(users)
        return True
    
    def delete_user(self, email: str) -> bool:
        """Delete a user (admin only)"""
        if not self.has_role('admin'):
            return False
        
        # Prevent deleting yourself
        current_user = self.get_current_user()
        if current_user and current_user.get('email') == email:
            return False
        
        users = self._load_users()
        if email not in users:
            return False
        
        del users[email]
        self._save_users(users)
        return True
    
    def reset_user_password(self, email: str, new_password: str) -> bool:
        """Reset user password (admin only)"""
        if not self.has_role('admin'):
            return False
        
        users = self._load_users()
        if email not in users:
            return False
        
        users[email]["password_hash"] = self._hash_password(new_password)
        self._save_users(users)
        return True
        
# Global auth manager instance
auth_manager = InAppAuthManager()

def show_login_form():
    """Display login form without st.form"""
    st.markdown("""
    <style>
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 40px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    .auth-header {
        margin-bottom: 30px;
    }
    .auth-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 12px;
        margin: 0 auto 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
        font-weight: bold;
        border: 3px solid #f1f5f9;
    }
    .auth-logo::before {
        content: "PWA";
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="auth-container">
            <div class="auth-header">
                <div class="auth-logo"></div>
                <h2>Public Welfare Assistant</h2>
                <p style="color: #666;">Secure access to your database analytics</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Login/Signup tabs
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.markdown("### Sign In to Your Account")
            
            # Use regular input fields instead of form
            email = st.text_input("Email Address", placeholder="your.email@company.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                remember_me = st.checkbox("Remember me")
            
            if st.button("Sign In", key="signin_btn", type="primary", use_container_width=True):
                if email and password:
                    if auth_manager.authenticate_user(email, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.warning("Please enter both email and password")
            
            st.markdown("---")
            st.info("**Test Accounts:**\n- Admin: admin@company.com / admin123\n- Analyst: analyst@company.com / analyst123\n- Officer: officer@company.com / officer123\n- User: user@company.com / user123")
        
        with tab2:
            st.markdown("### Create New Account")
            
            name = st.text_input("Full Name", placeholder="Your full name", key="signup_name")
            email = st.text_input("Email Address", placeholder="your.email@company.com", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="Create a strong password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
            
            role = st.selectbox("Role", ["user", "officer", "analyst", "admin"], key="signup_role", 
                              help="Select your role - admin accounts require approval")
            
            if st.button("Create Account", key="signup_btn", type="primary", use_container_width=True):
                if name and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("Passwords don't match")
                    else:
                        success, message = auth_manager.create_user(email, password, name, [role])
                        if success:
                            st.success(f"{message}")
                            st.info("You can now sign in with your new account")
                        else:
                            st.error(f"{message}")
                else:
                    st.warning("Please fill in all fields")

def show_user_profile_sidebar():
    """Show user profile in sidebar"""
    if not auth_manager.is_authenticated():
        return
    
    user_data = auth_manager.get_current_user()
    
    with st.sidebar:
        # Last login info
        last_login = user_data.get('last_login')
        if last_login:
            try:
                login_date = datetime.fromisoformat(last_login.replace('Z', '+00:00'))
                st.caption(f"Last login: {login_date.strftime('%Y-%m-%d %H:%M')}")
            except:
                st.caption("Last login: Recently")
        
        # Logout button
        if st.button("Logout", key="sidebar_logout"):
            auth_manager.logout()
            st.rerun()

def require_in_app_authentication():
    """Require authentication for the app"""
    if not auth_manager.is_authenticated():
        show_login_form()
        st.stop()
    return True

def get_current_user():
    """Get current authenticated user"""
    return auth_manager.get_current_user()

def has_role(role: str):
    """Check if current user has role"""
    return auth_manager.has_role(role)

def is_authenticated():
    """Check if user is authenticated"""
    return auth_manager.is_authenticated()