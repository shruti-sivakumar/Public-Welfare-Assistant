"""
Role-Based Access Control (RBAC) Components for In-App Auth0
Provides Azure AD-like role management and access control
"""

import streamlit as st
from typing import List, Dict, Optional

# Import the in-app auth manager
try:
    from in_app_auth import auth_manager
except ImportError:
    # Fallback if in_app_auth not available
    auth_manager = None

class RBACManager:
    """Role-Based Access Control Manager"""
    
    def __init__(self):
        # Define application roles similar to Azure AD groups
        self.available_roles = {
            'admin': {
                'display_name': 'Administrator',
                'description': 'Full system access with user management capabilities',
                'color': '#ff4444',
                'icon': 'Admin'
            },
            'analyst': {
                'display_name': 'Data Analyst',
                'description': 'Access to data analysis and reporting features',
                'color': '#4444ff',
                'icon': 'Analyst'
            },
            'officer': {
                'display_name': 'Welfare Officer',
                'description': 'Access to welfare data and basic reporting',
                'color': '#44ff44',
                'icon': 'Officer'
            },
            'user': {
                'display_name': 'Basic User',
                'description': 'Basic system access with limited permissions',
                'color': '#888888',
                'icon': 'User'
            }
        }
        
        # Define feature access matrix
        self.feature_access = {
            'database_query': ['admin', 'analyst'],
            'natural_language_query': ['admin', 'analyst', 'officer'],
            'data_export': ['admin', 'analyst', 'officer'],
            'user_management': ['admin'],
            'system_settings': ['admin'],
            'view_reports': ['admin', 'analyst', 'officer'],
            'create_reports': ['admin', 'analyst'],
            'delete_data': ['admin'],
            'modify_data': ['admin'],
            'view_audit_logs': ['admin'],
            'welfare_operations': ['admin', 'analyst', 'officer'],
            'citizen_data_access': ['admin', 'analyst', 'officer']
        }
    
    def check_feature_access(self, feature: str) -> bool:
        """Check if current user has access to a specific feature"""
        if not auth_manager or not auth_manager.is_authenticated():
            return False
        
        user_roles = auth_manager.get_user_roles()
        allowed_roles = self.feature_access.get(feature, [])
        
        # Check if user has any of the required roles
        return any(role.lower() in [r.lower() for r in allowed_roles] for role in user_roles)
    
    def require_feature_access(self, feature: str, show_error: bool = True) -> bool:
        """Require access to a specific feature"""
        if not self.check_feature_access(feature):
            if show_error:
                allowed_roles = self.feature_access.get(feature, [])
                roles_display = [self.available_roles.get(role, {}).get('display_name', role) for role in allowed_roles]
                
                st.error(f"**Access Denied**")
                st.warning(f"This feature requires one of the following roles: **{', '.join(roles_display)}**")
                st.info("Contact your administrator to request access.")
            return False
        return True
    
    def show_user_roles_badge(self):
        """Display user roles as badges"""
        if not auth_manager or not auth_manager.is_authenticated():
            return
        
        user_roles = auth_manager.get_user_roles()
        
        if user_roles:
            st.markdown("**Your Roles:**")
            cols = st.columns(len(user_roles))
            
            for idx, role in enumerate(user_roles):
                role_info = self.available_roles.get(role.lower(), {
                    'display_name': role,
                    'color': '#666666',
                    'icon': 'Role'
                })
                
                with cols[idx]:
                    st.markdown(f"""
                    <div style="
                        background-color: {role_info['color']};
                        color: white;
                        padding: 8px 12px;
                        border-radius: 20px;
                        text-align: center;
                        font-weight: bold;
                        margin: 2px;
                    ">
                        {role_info['icon']} {role_info['display_name']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No roles assigned. Contact your administrator.")
    
    def show_permissions_matrix(self):
        """Show permissions matrix for current user"""
        if not auth_manager or not auth_manager.is_authenticated():
            st.error("Authentication required to view permissions")
            return
        
        st.markdown("### Your Permissions")
        
        user_roles = auth_manager.get_user_roles()
        
        # Create permissions matrix
        permissions_data = []
        for feature, allowed_roles in self.feature_access.items():
            has_access = self.check_feature_access(feature)
            permissions_data.append({
                'Feature': feature.replace('_', ' ').title(),
                                'Access': 'Yes' if has_access else 'No',
                'Required Roles': ', '.join([self.available_roles.get(role, {}).get('display_name', role) for role in allowed_roles])
            })
        
        # Display as table
        import pandas as pd
        df = pd.DataFrame(permissions_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

# Global RBAC manager
rbac = RBACManager()

def require_role(role: str):
    """Decorator function to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if auth_manager and auth_manager.has_role(role):
                return func(*args, **kwargs)
            else:
                st.stop()
        return wrapper
    return decorator

def require_any_role(roles: List[str]):
    """Decorator function to require any of the specified roles"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if auth_manager and any(auth_manager.has_role(role) for role in roles):
                return func(*args, **kwargs)
            else:
                st.stop()
        return wrapper
    return decorator

def require_feature(feature: str):
    """Decorator function to require specific feature access"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if rbac.require_feature_access(feature):
                return func(*args, **kwargs)
            else:
                st.stop()
        return wrapper
    return decorator

def show_access_control_panel():
    """Show access control panel for administrators"""
    if not auth_manager or not auth_manager.has_role('admin'):
        st.error("Admin role required")
        return
    
    st.markdown("### Access Control Management")
    
    tab1, tab2, tab3 = st.tabs(["Role Overview", "Feature Matrix", "User Management"])
    
    with tab1:
        st.markdown("#### Available Roles")
        for role_key, role_info in rbac.available_roles.items():
            icon = role_info.get('icon', '👤')
            with st.expander(f"{icon} {role_info['display_name']}"):
                st.markdown(f"**Description:** {role_info['description']}")
                
                # Show features this role can access
                accessible_features = [feature for feature, roles in rbac.feature_access.items() if role_key in roles]
                if accessible_features:
                    st.markdown("**Accessible Features:**")
                    for feature in accessible_features:
                        st.markdown(f"• {feature.replace('_', ' ').title()}")
                else:
                    st.info("No special features assigned to this role")
    
    with tab2:
        st.markdown("#### Feature Access Matrix")
        rbac.show_permissions_matrix()
    
    with tab3:
        st.markdown("#### User Role Management")
        st.info("Role assignment should be done through the Auth0 Dashboard")
        st.markdown("""
        **To assign roles to users:**
        1. Go to your Auth0 Dashboard
        2. Navigate to User Management → Users
        3. Select a user
        4. Go to the Roles tab
        5. Assign appropriate roles
        
        **Available roles in this system:**
        """)
        
        for role_key, role_info in rbac.available_roles.items():
            st.markdown(f"• **{role_info['display_name']}**: {role_info['description']}")

def show_role_guard(required_roles: List[str], content_func, alternative_content=None):
    """Show content only if user has required roles"""
    if not auth_manager:
        st.error("Authentication not available")
        return
        
    user_roles = auth_manager.get_user_roles()
    has_access = any(role.lower() in [r.lower() for r in required_roles] for role in user_roles)
    
    if has_access:
        content_func()
    else:
        if alternative_content:
            alternative_content()
        else:
            st.warning(f"Access restricted to: {', '.join(required_roles)}")

def show_feature_guard(feature: str, content_func, alternative_content=None):
    """Show content only if user has feature access"""
    if rbac.check_feature_access(feature):
        content_func()
    else:
        if alternative_content:
            alternative_content()
        else:
            allowed_roles = rbac.feature_access.get(feature, [])
            roles_display = [rbac.available_roles.get(role, {}).get('display_name', role) for role in allowed_roles]
            st.warning(f"This feature requires: {', '.join(roles_display)}")

# Utility functions for quick access checks
def is_admin() -> bool:
    """Check if current user is admin"""
    return auth_manager.has_role('admin') if auth_manager else False

def is_analyst() -> bool:
    """Check if current user is analyst"""
    return auth_manager.has_role('analyst') if auth_manager else False

def is_officer() -> bool:
    """Check if current user is officer"""
    return auth_manager.has_role('officer') if auth_manager else False

def is_user() -> bool:
    """Check if current user is basic user"""
    return auth_manager.has_role('user') if auth_manager else False

def can_query_database() -> bool:
    """Check if user can query database"""
    return rbac.check_feature_access('database_query')

def can_export_data() -> bool:
    """Check if user can export data"""
    return rbac.check_feature_access('data_export')

def can_manage_users() -> bool:
    """Check if user can manage users"""
    return rbac.check_feature_access('user_management')

def can_access_welfare_operations() -> bool:
    """Check if user can access welfare operations"""
    return rbac.check_feature_access('welfare_operations')