"""GitHub integration for FORGE."""

import os
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import base64
import time
import git
from github import Github, Auth
from github.Repository import Repository
from github.PullRequest import PullRequest
from github.Issue import Issue


class GitHubManager:
    """Manage GitHub operations with authentication and repo handling."""
    
    SERVICE_NAME = "forge-cli"
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub manager with token."""
        self.token = token or self._get_token()
        self.github: Optional[Github] = None
        self.user = None
        self._has_github = False
        
        if self.token:
            self._init_github()
    
    def _init_github(self) -> None:
        """Initialize PyGithub client."""
        try:
            self.github = Github(auth=Auth.Token(self.token))
            self.user = self.github.get_user()
            self._has_github = True
        except ImportError:
            self._has_github = False
            self.github = None
            self.user = None
        except Exception:
            self._has_github = False
    
    def _get_token(self) -> Optional[str]:
        """Get GitHub token from config, keyring, or environment."""
        # Check config first
        from forge.config import get_config
        cfg = get_config()
        token = cfg.get_github_token()
        if token:
            return token
        
        # Check environment
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
        """Save GitHub token to keyring and config."""
        # Save to keyring
        try:
            import keyring
            keyring.set_password(self.SERVICE_NAME, "github_token", token)
        except Exception:
            pass  # Keyring might not be available
        
        # Also save to config
        from forge.config import get_config
        cfg = get_config()
        cfg.set('github.token', token)
        
        # Reinitialize with new token
        self.token = token
        self._init_github()
        
        return True
    
    def test_auth(self) -> Tuple[bool, str]:
        """Test authentication and return user info."""
        if not self._has_github:
            return False, "PyGithub not installed. Run: pip install PyGithub"
        
        try:
            user = self.user.login
            name = self.user.name or user
            return True, f"Authenticated as {name} (@{user})"
        except Exception as e:
            return False, str(e)
    
    def is_available(self) -> bool:
        """Check if GitHub integration is available."""
        return self._has_github and self.token is not None
    
    # ============= Repository Operations =============
    
    def list_repos(self, repo_type: str = "owner", limit: int = 30) -> List[Dict[str, Any]]:
        """List repositories.
        
        Args:
            repo_type: Type of repos to list (owner, all, public, private)
            limit: Maximum number of repos to return
            
        Returns:
            List of repository info dictionaries
        """
        if not self.is_available():
            return []
        
        repos = []
        try:
            if repo_type == "owner":
                for repo in self.user.get_repos()[:limit]:
                    repos.append(self._repo_to_dict(repo))
            elif repo_type == "all":
                for repo in self.github.get_user().get_repos(type="all")[:limit]:
                    repos.append(self._repo_to_dict(repo))
            elif repo_type == "public":
                for repo in self.github.get_user().get_repos(type="public")[:limit]:
                    repos.append(self._repo_to_dict(repo))
            elif repo_type == "private":
                for repo in self.github.get_user().get_repos(type="private")[:limit]:
                    repos.append(self._repo_to_dict(repo))
        except Exception as e:
            print(f"Error listing repos: {e}")
        
        return repos
    
    def _repo_to_dict(self, repo: Repository) -> Dict[str, Any]:
        """Convert repository to dictionary."""
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description or "",
            "url": repo.html_url,
            "clone_url": repo.clone_url,
            "default_branch": repo.default_branch,
            "language": repo.language or "",
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "is_private": repo.private,
            "is_fork": repo.fork,
            "created_at": repo.created_at.isoformat() if repo.created_at else "",
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else "",
        }
    
    def get_repo(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific repository.
        
        Args:
            repo_name: Repository name (owner/repo or just name)
            
        Returns:
            Repository info dictionary or None
        """
        if not self.is_available():
            return None
        
        try:
            # Handle both "owner/repo" and just "repo" formats
            if "/" in repo_name:
                repo = self.github.get_repo(repo_name)
            else:
                repo = self.github.get_user().get_repo(repo_name)
            return self._repo_to_dict(repo)
        except Exception:
            return None
    
    def clone_repo(self, repo_name: str, path: Optional[str] = None, branch: Optional[str] = None) -> Tuple[bool, str]:
        """Clone a repository locally.
        
        Args:
            repo_name: Repository name
            path: Optional local path to clone to
            branch: Optional branch to clone
            
        Returns:
            Tuple of (success, message)
        """
        repo_info = self.get_repo(repo_name)
        if not repo_info:
            return False, f"Repository not found: {repo_name}"
        
        target_path = Path(path) if path else Path.cwd() / repo_info["name"]
        
        try:
            if target_path.exists():
                return False, f"Directory already exists: {target_path}"
            
            # Clone the repo
            git.Repo.clone_from(repo_info["clone_url"], str(target_path), branch=branch)
            return True, f"Cloned {repo_info['full_name']} to {target_path}"
        except Exception as e:
            return False, f"Clone failed: {str(e)}"
    
    # ============= Pull Request Operations =============
    
    def list_pull_requests(self, repo_name: str, state: str = "open", limit: int = 30) -> List[Dict[str, Any]]:
        """List pull requests for a repository.
        
        Args:
            repo_name: Repository name
            state: PR state (open, closed, all)
            limit: Maximum number of PRs to return
            
        Returns:
            List of PR info dictionaries
        """
        if not self.is_available():
            return []
        
        prs = []
        try:
            repo = self.github.get_repo(repo_name)
            for pr in repo.get_pulls(state=state)[:limit]:
                prs.append({
                    "number": pr.number,
                    "title": pr.title,
                    "body": pr.body or "",
                    "state": pr.state,
                    "html_url": pr.html_url,
                    "head_branch": pr.head.ref,
                    "base_branch": pr.base.ref,
                    "user": pr.user.login,
                    "created_at": pr.created_at.isoformat() if pr.created_at else "",
                    "updated_at": pr.updated_at.isoformat() if pr.updated_at else "",
                    "merged_at": pr.merged_at.isoformat() if pr.merged_at else "",
                })
        except Exception as e:
            print(f"Error listing PRs: {e}")
        
        return prs
    
    def create_pull_request(self, repo_name: str, title: str, head: str, base: str, body: str = "") -> Tuple[bool, str]:
        """Create a pull request.
        
        Args:
            repo_name: Repository name
            title: PR title
            head: Head branch name
            base: Base branch name
            body: PR description
            
        Returns:
            Tuple of (success, message)
        """
        if not self.is_available():
            return False, "GitHub not available. Run: forge github auth --token YOUR_TOKEN"
        
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.create_pull(title=title, body=body, head=head, base=base)
            return True, f"PR created: {pr.html_url}"
        except Exception as e:
            return False, f"Failed to create PR: {str(e)}"
    
    # ============= Issue Operations =============
    
    def list_issues(self, repo_name: str, state: str = "open", limit: int = 30) -> List[Dict[str, Any]]:
        """List issues for a repository.
        
        Args:
            repo_name: Repository name
            state: Issue state (open, closed, all)
            limit: Maximum number of issues to return
            
        Returns:
            List of issue info dictionaries
        """
        if not self.is_available():
            return []
        
        issues = []
        try:
            repo = self.github.get_repo(repo_name)
            for issue in repo.get_issues(state=state)[:limit]:
                # Skip pull requests (they're also issues in GitHub API)
                if issue.pull_request:
                    continue
                issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body or "",
                    "state": issue.state,
                    "html_url": issue.html_url,
                    "user": issue.user.login,
                    "labels": [label.name for label in issue.labels],
                    "created_at": issue.created_at.isoformat() if issue.created_at else "",
                    "updated_at": issue.updated_at.isoformat() if issue.updated_at else "",
                })
        except Exception as e:
            print(f"Error listing issues: {e}")
        
        return issues
    
    def create_issue(self, repo_name: str, title: str, body: str = "", labels: Optional[List[str]] = None) -> Tuple[bool, str]:
        """Create an issue.
        
        Args:
            repo_name: Repository name
            title: Issue title
            body: Issue description
            labels: Optional list of labels
            
        Returns:
            Tuple of (success, message)
        """
        if not self.is_available():
            return False, "GitHub not available. Run: forge github auth --token YOUR_TOKEN"
        
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body, labels=labels or [])
            return True, f"Issue created: {issue.html_url}"
        except Exception as e:
            return False, f"Failed to create issue: {str(e)}"
    
    # ============= Git Operations (using GitPython) =============
    
    def get_local_status(self, path: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get git status for a local repository.
        
        Args:
            path: Optional path to repository (defaults to cwd)
            
        Returns:
            Status dictionary or None
        """
        repo_path = Path(path) if path else Path.cwd()
        
        try:
            repo = git.Repo(repo_path)
            
            status = {
                "branch": repo.active_branch.name,
                "is_dirty": repo.is_dirty(),
                "untracked": repo.untracked_files,
                "staged": [item.a_path for item in repo.index.diff("HEAD")],
                "modified": [item.a_path for item in repo.index.diff(None)],
            }
            
            return status
        except git.exc.InvalidGitRepositoryError:
            return None
        except Exception as e:
            return None
    
    def create_commit(self, path: str, message: str) -> Tuple[bool, str]:
        """Create a git commit.
        
        Args:
            path: Path to the repository
            message: Commit message
            
        Returns:
            Tuple of (success, message)
        """
        try:
            repo = git.Repo(path)
            
            # Stage all changes
            repo.index.add("*")
            
            # Commit
            commit = repo.index.commit(message)
            return True, f"Committed: {commit.hexsha[:7]} - {message}"
        except Exception as e:
            return False, f"Commit failed: {str(e)}"
    
    def get_commit_history(self, path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get commit history for a repository.
        
        Args:
            path: Path to the repository
            limit: Number of commits to return
            
        Returns:
            List of commit info dictionaries
        """
        try:
            repo = git.Repo(path)
            commits = []
            
            for commit in repo.iter_commits(max_count=limit):
                commits.append({
                    "sha": commit.hexsha[:7],
                    "full_sha": commit.hexsha,
                    "message": commit.message.strip(),
                    "author": str(commit.author),
                    "author_email": commit.author.email,
                    "date": commit.committed_datetime.isoformat(),
                })
            
            return commits
        except Exception:
            return []
    
    def create_branch(self, path: str, branch_name: str) -> Tuple[bool, str]:
        """Create a new branch.
        
        Args:
            path: Path to the repository
            branch_name: Name of the new branch
            
        Returns:
            Tuple of (success, message)
        """
        try:
            repo = git.Repo(path)
            
            # Check if branch exists
            if branch_name in repo.branches:
                return False, f"Branch already exists: {branch_name}"
            
            # Create and checkout new branch
            new_branch = repo.create_head(branch_name)
            new_branch.checkout()
            
            return True, f"Created and checked out branch: {branch_name}"
        except Exception as e:
            return False, f"Failed to create branch: {str(e)}"
    
    def switch_branch(self, path: str, branch_name: str) -> Tuple[bool, str]:
        """Switch to a branch.
        
        Args:
            path: Path to the repository
            branch_name: Name of the branch to switch to
            
        Returns:
            Tuple of (success, message)
        """
        try:
            repo = git.Repo(path)
            branch = repo.branches[branch_name]
            branch.checkout()
            return True, f"Switched to branch: {branch_name}"
        except Exception as e:
            return False, f"Failed to switch branch: {str(e)}"
    
    def push(self, path: str, remote: str = "origin", branch: Optional[str] = None, force: bool = False) -> Tuple[bool, str]:
        """Push to a remote.
        
        Args:
            path: Path to the repository
            remote: Remote name (default: origin)
            branch: Branch to push (default: current branch)
            force: Force push
            
        Returns:
            Tuple of (success, message)
        """
        try:
            repo = git.Repo(path)
            
            if branch:
                refspec = branch
            else:
                refspec = repo.active_branch.name
            
            if force:
                result = repo.remotes[remote].push(refspec, force=True)
            else:
                result = repo.remotes[remote].push(refspec)
            
            pushed = [r.ref for r in result]
            if pushed:
                return True, f"Pushed to {remote}/{refspec}"
            return True, "Nothing to push"
        except Exception as e:
            return False, f"Push failed: {str(e)}"
    
    def pull(self, path: str, remote: str = "origin", branch: Optional[str] = None) -> Tuple[bool, str]:
        """Pull from a remote.
        
        Args:
            path: Path to the repository
            remote: Remote name (default: origin)
            branch: Branch to pull (default: current branch)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            repo = git.Repo(path)
            
            if branch:
                refspec = branch
            else:
                refspec = repo.active_branch.name
            
            result = repo.remotes[remote].pull(refspec)
            return True, f"Pulled from {remote}/{refspec}"
        except Exception as e:
            return False, f"Pull failed: {str(e)}"
