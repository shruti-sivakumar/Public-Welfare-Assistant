"""
Authentication module 
"""
from typing import Optional, Dict, Any
import logging
import os
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AuthManager:
    """Manages authentication and authorization"""
    
    def __init__(self):
        self.active_sessions = {}
        self.users = self._initialize_demo_users()
        
        
        # JWT settings
        self.jwt_secret = os.getenv('JWT_SECRET', 'demo_secret_key_change_in_production')
        self.jwt_algorithm = 'HS256'
        self.token_expiry_hours = int(os.getenv('TOKEN_EXPIRY_HOURS', '24'))
    
    def _initialize_demo_users(self) -> Dict[str, Dict[str, Any]]:
        """Initialize demo users for testing"""
        return {
            "admin": {
                "user_id": "admin",
                "username": "admin",
                "role": "administrator", 
                "permissions": ["read", "write", "admin", "query"],
                "email": "admin@company.com",
                "department": "IT"
            },
            "user1": {
                "user_id": "user1",
                "username": "user1",
                "role": "user",
                "permissions": ["read"],
                "email": "user1@company.com",
                "department": "Operations"
            },
            "analyst": {
                "user_id": "analyst",
                "username": "analyst", 
                "role": "analyst",
                "permissions": ["read", "query"],
                "email": "analyst@company.com",
                "department": "Analytics"
            },
            "officer": {
                "user_id": "officer",
                "username": "officer", 
                "role": "officer",
                "permissions": ["read", "write", "query"],
                "email": "officer@company.com",
                "department": "Field Operations"
            }
        }
    
    def _generate_jwt_token(self, user_info: Dict[str, Any]) -> str:
        """Generate JWT token for user"""
        try:
            payload = {
                'user_id': user_info['user_id'],
                'username': user_info['username'],
                'role': user_info['role'],
                'permissions': user_info['permissions'],
                'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
                'iat': datetime.utcnow(),
                'iss': 'data-interpreter-api'
            }
            
            # For demo purposes, use simple token generation
            # In production, use proper JWT library
            token = f"demo_jwt_{user_info['username']}_{int(datetime.utcnow().timestamp())}"
            return token
            
        except Exception as e:
            logger.error(f"Token generation error: {e}")
            return f"demo_token_{user_info['username']}_12345"
    
    

    def authenticate_user(self, username: str, password: str = None) -> Dict[str, Any]:
        """Authenticate user (demo implementation)"""
        try:
            # For demo purposes, accept any password for existing users
            if username in self.users:
                user_info = self.users[username].copy()
                
                # Generate JWT token
                token = self._generate_jwt_token(user_info)
                
                # Store session with additional metadata
                session_data = user_info.copy()
                session_data.update({
                    'login_time': datetime.utcnow().isoformat(),
                    'token_type': 'demo_jwt',
                    'expires_at': (datetime.utcnow() + timedelta(hours=self.token_expiry_hours)).isoformat()
                })
                
                self.active_sessions[token] = session_data
                
                # Store session
                self.active_sessions[token] = user_info
                
                return {
                    "status": "success",
                    "message": "Authentication successful",
                    "token": token,
                    "user": user_info
                }
            else:
                return {
                    "status": "error", 
                    "message": "Invalid username"
                }
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return {
                "status": "error",
                "message": f"Authentication failed: {str(e)}"
            }
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify authentication token"""
        try:
            if token in self.active_sessions:
                user_info = self.active_sessions[token]
                return {
                    "status": "success",
                    "valid": True,
                    "user": user_info
                }
            else:
                return {
                    "status": "error",
                    "valid": False,
                    "message": "Invalid or expired token"
                }
                
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return {
                "status": "error",
                "valid": False,
                "message": f"Token verification failed: {str(e)}"
            }
    
    def check_permission(self, token: str, required_permission: str) -> bool:
        """Check if user has required permission"""
        try:
            token_info = self.verify_token(token)
            
            if token_info["status"] == "success" and token_info["valid"]:
                user_permissions = token_info["user"]["permissions"]
                return required_permission in user_permissions
            
            return False
            
        except Exception as e:
            logger.error(f"Permission check error: {e}")
            return False
    
    def logout_user(self, token: str) -> Dict[str, Any]:
        """Logout user and invalidate token"""
        try:
            if token in self.active_sessions:
                del self.active_sessions[token]
                return {
                    "status": "success",
                    "message": "Logout successful"
                }
            else:
                return {
                    "status": "error",
                    "message": "Token not found"
                }
                
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return {
                "status": "error",
                "message": f"Logout failed: {str(e)}"
            }
    
    def get_user_info(self, token: str) -> Dict[str, Any]:
        """Get user information from token"""
        try:
            token_info = self.verify_token(token)
            
            if token_info["status"] == "success" and token_info["valid"]:
                return {
                    "status": "success",
                    "user": token_info["user"]
                }
            else:
                return {
                    "status": "error",
                    "message": "Invalid token"
                }
                
        except Exception as e:
            logger.error(f"Get user info error: {e}")
            return {
                "status": "error",
                "message": f"Failed to get user info: {str(e)}"
            }

# Global auth manager instance
auth_manager = AuthManager()

def authenticate(username: str, password: str = None):
    """Authenticate user"""
    return auth_manager.authenticate_user(username, password)

def verify_token(token: str):
    """Verify authentication token"""
    return auth_manager.verify_token(token)

def check_permission(token: str, permission: str):
    """Check user permission"""
    return auth_manager.check_permission(token, permission)
