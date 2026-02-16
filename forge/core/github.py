"""GitHub integration for FORGE."""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import base64
import time


class GitHubManager:
    """Manage GitHub operations with authentication and repo handling."""
    
    SERVICE_NAME = "forge-cli"
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub manager with token."""
        self.token = token or self._get_token()
        if not self.token:
            raise ValueError("GitHub token required. Use 'forge github auth' to set up.")
        
        # Try to import optional dependencies
        try:
            from github import Github, Auth
            self.github = Github(auth=Auth.Token(self.token))
            self.user = self.github.get_user()
            self._has_github = True
        except ImportError:
            self._has_github = False
            self.github = None
            self.user = None
        
        # Local git repos cache
        self.repos = {}
    
    def _get_token(self) -> Optional[str]:
        """Get GitHub token from keyring or environment."""
        # Check environment first
        token = os.getenv('GITHUB_TOKEN')
        if token:
            return token
        
        # Check keyring
        try:
            import keyring
            return keyring.get_password(self.SERVICE_NAME, "github_token")
        except:
            return None
    
    def save_token(self, token: str) -> bool:
        """Save GitHub token to keyring."""
        try:
            import keyring
            keyring.set_password(self.SERVICE_NAME, "github_token", token)
            return True
        except Exception as e:
            print(f"Error saving token: {e}")
            return False
    
    def test_auth(self) -> Tuple[bool, str]:
        """Test authentication and return user info."""
        if not self._has_github:
            return False, "PyGithub not installed. Run: pip install PyGithub"
        
        try:
            user = self.user.login
            name = self.user.name or user
            return True, f"Authenticated as {name} ({user})"
        except Exception as e:
            return False, str(e)
    
    def is_available(self) -> bool:
        """Check if GitHub integration is available."""
        return self._has_github and self.token is not None
