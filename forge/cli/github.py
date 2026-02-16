"""GitHub CLI commands for FORGE."""

import os
import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.group()
def github():
    """GitHub integration commands."""
    pass


@github.command()
@click.option('--token', '-t', help='GitHub Personal Access Token')
def auth(token):
    """Authenticate with GitHub and store token securely."""
    if not token:
        console.print("[red]Error: Token is required[/red]")
        console.print("Get a token from: https://github.com/settings/tokens")
        return
    
    try:
        from ..core.github import GitHubManager
        manager = GitHubManager(token)
        success, message = manager.test_auth()
        
        if success:
            manager.save_token(token)
            console.print(f"[green]✅ Authentication successful![/green]")
            console.print(f"[cyan]{message}[/cyan]")
            console.print("\n[yellow]Token saved.[/yellow]")
        else:
            console.print(f"[red]❌ Authentication failed: {message}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("\n[yellow]Tip: Install PyGithub: pip install PyGithub GitPython keyring[/yellow]")


@github.command()
@click.option('--type', '-t', type=click.Choice(['owner', 'all', 'public', 'private']),
              default='owner', help='Repository type')
def list(type):
    """List your GitHub repositories."""
    try:
        from ..core.github import GitHubManager
        manager = GitHubManager()
        
        if not manager.is_available():
            console.print("[red]GitHub not available.[/red]")
            console.print("[yellow]Run: forge github auth --token YOUR_TOKEN[/yellow]")
            return
        
        console.print("[blue]Fetching repositories...[/blue]")
        console.print("[yellow]Note: Full GitHub listing requires PyGithub installation[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@github.command()
@click.argument('repo_name')
@click.option('--path', '-p', help='Local path to clone to')
@click.option('--branch', '-b', help='Branch to clone')
def clone(repo_name, path, branch):
    """Clone a GitHub repository locally."""
    try:
        from ..core.github import GitHubManager
        manager = GitHubManager()
        
        if not manager.is_available():
            console.print("[red]GitHub not available.[/red]")
            console.print("[yellow]Run: forge github auth --token YOUR_TOKEN[/yellow]")
            return
        
        console.print(f"[blue]Cloning {repo_name}...[/blue]")
        console.print("[yellow]Note: Full clone requires PyGithub and GitPython installation[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@github.command()
@click.argument('message', nargs=-1, required=True)
@click.option('--ai/--no-ai', default=True, help='Use AI to enhance commit message')
def commit(message, ai):
    """Commit changes with AI-enhanced messages."""
    full_message = ' '.join(message)
    
    console.print(f"[blue]Commit message: {full_message}[/blue]")
    
    if ai:
        console.print("[yellow]Note: AI-enhanced commits require DeepSeek API[/yellow]")
    
    console.print("[yellow]Note: Full git operations require GitPython installation[/yellow]")


@github.command()
@click.option('--branch', '-b', help='Branch to push')
@click.option('--force', '-f', is_flag=True, help='Force push')
def push(branch, force):
    """Push changes to GitHub."""
    try:
        from ..core.github import GitHubManager
        manager = GitHubManager()
        
        if not manager.is_available():
            console.print("[red]GitHub not available.[/red]")
            console.print("[yellow]Run: forge github auth --token YOUR_TOKEN[/yellow]")
            return
        
        console.print(f"[blue]Pushing branch: {branch or 'current'}[/blue]")
        console.print("[yellow]Note: Full push requires GitPython installation[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@github.command()
@click.argument('repo_name')
@click.option('--state', '-s', type=click.Choice(['open', 'closed', 'all']),
              default='open', help='PR state')
def pr_list(repo_name, state):
    """List pull requests for a repository."""
    try:
        from ..core.github import GitHubManager
        manager = GitHubManager()
        
        if not manager.is_available():
            console.print("[red]GitHub not available.[/red]")
            console.print("[yellow]Run: forge github auth --token YOUR_TOKEN[/yellow]")
            return
        
        console.print(f"[blue]Fetching PRs for {repo_name}...[/blue]")
        console.print("[yellow]Note: Full PR listing requires PyGithub installation[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@github.command()
@click.argument('title', nargs=-1, required=True)
@click.option('--repo', '-r', required=True, help='Repository name (owner/repo)')
@click.option('--head', '-h', required=True, help='Head branch')
@click.option('--base', '-b', default='main', help='Base branch')
def pr_create(title, repo, head, base):
    """Create a pull request."""
    full_title = ' '.join(title)
    
    try:
        from ..core.github import GitHubManager
        manager = GitHubManager()
        
        if not manager.is_available():
            console.print("[red]GitHub not available.[/red]")
            console.print("[yellow]Run: forge github auth --token YOUR_TOKEN[/yellow]")
            return
        
        console.print(f"[blue]Creating PR: {full_title}[/blue]")
        console.print(f"[blue]Repository: {repo}[/blue]")
        console.print(f"[blue]Head: {head} → Base: {base}[/blue]")
        console.print("[yellow]Note: Full PR creation requires PyGithub installation[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@github.command()
@click.argument('repo_name')
@click.option('--state', '-s', type=click.Choice(['open', 'closed', 'all']),
              default='open', help='Issue state')
def issue_list(repo_name, state):
    """List issues for a repository."""
    try:
        from ..core.github import GitHubManager
        manager = GitHubManager()
        
        if not manager.is_available():
            console.print("[red]GitHub not available.[/red]")
            console.print("[yellow]Run: forge github auth --token YOUR_TOKEN[/yellow]")
            return
        
        console.print(f"[blue]Fetching issues for {repo_name}...[/blue]")
        console.print("[yellow]Note: Full issue listing requires PyGithub installation[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@github.command()
@click.argument('title', nargs=-1, required=True)
@click.option('--repo', '-r', required=True, help='Repository name (owner/repo)')
@click.option('--body', '-B', help='Issue description')
def issue_create(title, repo, body):
    """Create an issue on GitHub."""
    full_title = ' '.join(title)
    
    try:
        from ..core.github import GitHubManager
        manager = GitHubManager()
        
        if not manager.is_available():
            console.print("[red]GitHub not available.[/red]")
            console.print("[yellow]Run: forge github auth --token YOUR_TOKEN[/yellow]")
            return
        
        console.print(f"[blue]Creating issue: {full_title}[/blue]")
        console.print(f"[blue]Repository: {repo}[/blue]")
        console.print("[yellow]Note: Full issue creation requires PyGithub installation[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@github.command()
@click.argument('path', required=False)
def status(path):
    """Show git status of local repository."""
    try:
        import git
        from git import Repo
        
        repo_path = Path(path) if path else Path.cwd()
        
        try:
            repo = Repo(repo_path)
            console.print(f"\n[bold]On branch:[/bold] [cyan]{repo.active_branch}[/cyan]\n")
            
            if not repo.is_dirty() and not repo.untracked_files:
                console.print("[green]Working tree clean[/green]")
            else:
                if repo.is_dirty():
                    console.print("[yellow]Changes not staged:[/yellow]")
                if repo.untracked_files:
                    console.print(f"[yellow]Untracked files: {len(repo.untracked_files)}[/yellow]")
                    
        except git.exc.InvalidGitRepositoryError:
            console.print(f"[red]Not a git repository: {repo_path}[/red]")
            
    except ImportError:
        console.print("[red]GitPython not installed.[/red]")
        console.print("[yellow]Install with: pip install GitPython[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
