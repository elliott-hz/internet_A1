"""
Session Store for JWT Token Management
Stores active sessions in memory with automatic expiration
"""

from datetime import datetime, timedelta
from typing import Dict, Optional


class SessionStore:
    """In-memory session store for managing JWT tokens"""
    
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
    
    def create_session(self, username: str, token: str, expire_hours: int = 24):
        """
        Create a new session
        
        Args:
            username: User identifier
            token: JWT token string
            expire_hours: Session expiration time in hours (default: 24)
        """
        now = datetime.now()
        self.sessions[token] = {
            "username": username,
            "created_at": now,
            "expires_at": now + timedelta(hours=expire_hours)
        }
    
    def get_session(self, token: str) -> Optional[dict]:
        """
        Get session by token
        
        Args:
            token: JWT token string
            
        Returns:
            Session data if valid and not expired, None otherwise
        """
        session = self.sessions.get(token)
        if not session:
            return None
        
        # Check if expired
        if datetime.now() > session["expires_at"]:
            # Remove expired session
            del self.sessions[token]
            return None
        
        return session
    
    def delete_session(self, token: str):
        """
        Delete a session (used for logout)
        
        Args:
            token: JWT token to remove
        """
        if token in self.sessions:
            del self.sessions[token]
    
    def cleanup_expired(self):
        """Clean up all expired sessions"""
        now = datetime.now()
        expired = [
            token for token, session in self.sessions.items()
            if now > session["expires_at"]
        ]
        for token in expired:
            del self.sessions[token]


# Global singleton instance
session_store = SessionStore()
