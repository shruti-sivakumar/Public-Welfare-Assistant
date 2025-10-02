"""
Access Logger Module for Public Welfare Assistant
Tracks user logins, activities, and system access
"""

import json
import os
from datetime import datetime, timedelta
import streamlit as st
from pathlib import Path
import pandas as pd

class AccessLogger:
    def __init__(self, log_file="logs/access_logs.json"):
        self.log_file = log_file
        self.ensure_log_directory()
    
    def ensure_log_directory(self):
        """Ensure the logs directory exists"""
        log_dir = Path(self.log_file).parent
        log_dir.mkdir(exist_ok=True)
    
    def log_event(self, event_type, user_info=None, details=None):
        """Log an access event"""
        try:
            # Get current user if not provided
            if user_info is None:
                from in_app_auth import get_current_user
                current_user = get_current_user()
                if current_user:
                    user_info = {
                        'email': current_user.get('email', 'Unknown'),
                        'name': current_user.get('name', 'Unknown'),
                        'roles': current_user.get('roles', [])
                    }
                else:
                    user_info = {'email': 'Anonymous', 'name': 'Anonymous', 'roles': []}
            
            # Create log entry
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'user_email': user_info.get('email', 'Unknown'),
                'user_name': user_info.get('name', 'Unknown'),
                'user_roles': user_info.get('roles', []),
                'ip_address': self._get_client_ip(),
                'session_id': st.session_state.get('session_id', 'unknown'),
                'details': details or {},
                'user_agent': self._get_user_agent()
            }
            
            # Load existing logs
            logs = self._load_logs()
            
            # Add new entry
            logs.append(log_entry)
            
            # Keep only last 1000 entries to prevent file from growing too large
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            # Save logs
            self._save_logs(logs)
            
        except Exception as e:
            # Fail silently to not break the app
            print(f"Logging error: {str(e)}")
    
    def _get_client_ip(self):
        """Get client IP address"""
        try:
            # Try to get from Streamlit headers
            if hasattr(st, 'session_state') and hasattr(st.session_state, 'client_ip'):
                return st.session_state.client_ip
            return "Unknown"
        except:
            return "Unknown"
    
    def _get_user_agent(self):
        """Get user agent string"""
        try:
            # This would need to be set from browser if available
            return st.session_state.get('user_agent', 'Unknown')
        except:
            return "Unknown"
    
    def _load_logs(self):
        """Load existing logs from file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading logs: {str(e)}")
            return []
    
    def _save_logs(self, logs):
        """Save logs to file"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving logs: {str(e)}")
    
    def get_logs(self, limit=100, event_type=None, user_email=None, start_date=None, end_date=None):
        """Retrieve logs with optional filtering"""
        try:
            logs = self._load_logs()
            
            # Apply filters
            filtered_logs = []
            for log in logs:
                # Event type filter
                if event_type and log.get('event_type') != event_type:
                    continue
                
                # User filter
                if user_email and log.get('user_email') != user_email:
                    continue
                
                # Date filters
                log_date = datetime.fromisoformat(log['timestamp'])
                if start_date and log_date.date() < start_date:
                    continue
                if end_date and log_date.date() > end_date:
                    continue
                
                filtered_logs.append(log)
            
            # Sort by timestamp (newest first) and limit
            filtered_logs.sort(key=lambda x: x['timestamp'], reverse=True)
            return filtered_logs[:limit]
            
        except Exception as e:
            print(f"Error retrieving logs: {str(e)}")
            return []
    
    def get_logs_dataframe(self, limit=100, **filters):
        """Get logs as pandas DataFrame for display"""
        logs = self.get_logs(limit=limit, **filters)
        
        if not logs:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df_data = []
        for log in logs:
            df_data.append({
                'Timestamp': datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                'Event': log['event_type'],
                'User': log['user_name'],
                'Email': log['user_email'],
                'Roles': ', '.join(log.get('user_roles', [])),
                'IP Address': log.get('ip_address', 'Unknown'),
                'Details': str(log.get('details', {}))
            })
        
        return pd.DataFrame(df_data)
    
    def get_summary_stats(self):
        """Get summary statistics for dashboard"""
        try:
            logs = self._load_logs()
            
            if not logs:
                return {
                    'total_events': 0,
                    'unique_users': 0,
                    'login_events': 0,
                    'recent_activity': 0
                }
            
            # Calculate stats
            total_events = len(logs)
            unique_users = len(set(log['user_email'] for log in logs if log['user_email'] != 'Anonymous'))
            login_events = len([log for log in logs if log['event_type'] == 'login'])
            
            # Recent activity (last 24 hours)
            yesterday = datetime.now() - timedelta(days=1)
            recent_activity = len([
                log for log in logs 
                if datetime.fromisoformat(log['timestamp']) > yesterday
            ])
            
            return {
                'total_events': total_events,
                'unique_users': unique_users,
                'login_events': login_events,
                'recent_activity': recent_activity
            }
            
        except Exception as e:
            print(f"Error getting summary stats: {str(e)}")
            return {
                'total_events': 0,
                'unique_users': 0,
                'login_events': 0,
                'recent_activity': 0
            }

# Global logger instance
access_logger = AccessLogger()

# Convenience functions
def log_login(user_info=None):
    """Log a user login event"""
    access_logger.log_event('login', user_info)

def log_logout(user_info=None):
    """Log a user logout event"""
    access_logger.log_event('logout', user_info)

def log_query(query_text, user_info=None):
    """Log a database query event"""
    details = {'query': query_text[:200]}  # Truncate long queries
    access_logger.log_event('query', user_info, details)

def log_export(export_type, user_info=None):
    """Log a data export event"""
    details = {'export_type': export_type}
    access_logger.log_event('export', user_info, details)

def log_page_access(page_name, user_info=None):
    """Log page access event"""
    details = {'page': page_name}
    access_logger.log_event('page_access', user_info, details)

def log_admin_action(action, target=None, user_info=None):
    """Log administrative actions"""
    details = {'action': action, 'target': target}
    access_logger.log_event('admin_action', user_info, details)

# Error logging removed - focus only on access logs

def log_security_event(event_description, user_info=None):
    """Log security-related events"""
    details = {'security_event': event_description}
    access_logger.log_event('security', user_info, details)