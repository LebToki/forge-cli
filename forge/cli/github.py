"""GitHub CLI commands for FORGE."""

import os
import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def check_github_available():
    """Check if GitHub is available and show error if not."""
    try:
        from forge.core.github import GitHubManager
        manager = GitHubManager()
        if not manager.is_available():
            console.print("[red]GitHub not configured.[/red]")
            console.print("[yellow]Run: forge config set github.token YOUR_TOKEN[/yellow]")
            return None
        return manager
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return None


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
        console.print("\n[dim]Required scopes: repo (full control)[/dim]")
        return
    
    try:
        from forge.core.github import GitHubManager
        manager = GitHubManager(token=token)
        success, message = manager.test_auth()
        
        if success:
            manager.save_token(token)
            console.print(f"[green]✅ Authentication successful![/green]")
            console.print(f"[cyan]{message}[/cyan]")
        else:
            console.print(f"[red]❌ Authentication failed:[/red] {message}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.option('--type', '-t', type=click.Choice(['owner', 'all', 'public', 'private']),
              default='owner', help='Repository type')
@click.option('--limit', '-l', type=int, default=30, help='Number of repos to show')
def list(type, limit):
    """List your GitHub repositories."""
    manager = check_github_available()
    if not manager:
        return
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Fetching repositories...", total=None)
            repos = manager.list_repos(repo_type=type, limit=limit)
        
        if not repos:
            console.print("[yellow]No repositories found[/yellow]")
            return
        
        # Display repositories in a table
        table = Table(title=f"Your {type.capitalize()} Repositories")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Stars", justify="right", style="yellow")
        table.add_column("Language", style="green")
        
        for repo in repos:
            table.add_row(
                repo['name'],
                repo['description'][:50] + ('...' if len(repo['description']) > 50 else ''),
                str(repo['stars']),
                repo['language']
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.argument('repo_name')
@click.option('--path', '-p', help='Local path to clone to')
@click.option('--branch', '-b', help='Branch to clone')
def clone(repo_name, path, branch):
    """Clone a GitHub repository locally."""
    manager = check_github_available()
    if not manager:
        return
    
    console.print(f"[blue]Cloning {repo_name}...[/blue]")
    
    success, message = manager.clone_repo(repo_name, path=path, branch=branch)
    
    if success:
        console.print(f"[green]✅ {message}[/green]")
    else:
        console.print(f"[red]❌ {message}[/red]")


@github.command()
@click.argument('message', nargs=-1, required=True)
@click.option('--ai/--no-ai', default=False, help='Use AI to enhance commit message')
@click.option('--path', '-p', default='.', help='Repository path')
def commit(message, ai, path):
    """Commit changes with optional AI-enhanced messages."""
    full_message = ' '.join(message)
    
    manager = check_github_available()
    
    # If AI is requested, generate a better commit message
    if ai and manager:
        console.print("[blue]Enhancing commit message with AI...[/blue]")
        # This would call DeepSeek to enhance the message
        # For now, just use the provided message
        console.print("[yellow]AI enhancement coming soon![/yellow]")
    
    try:
        from forge.core.github import GitHubManager
        gh_manager = manager or GitHubManager()
        success, msg = gh_manager.create_commit(path, full_message)
        
        if success:
            console.print(f"[green]✅ {msg}[/green]")
        else:
            console.print(f"[red]❌ {msg}[/red]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.option('--branch', '-b', help='Branch to push (default: current)')
@click.option('--force', '-f', is_flag=True, help='Force push')
@click.option('--path', '-p', default='.', help='Repository path')
def push(branch, force, path):
    """Push changes to GitHub."""
    try:
        from forge.core.github import GitHubManager
        manager = check_github_available()
        if not manager:
            return
        
        success, message = manager.push(path, branch=branch, force=force)
        
        if success:
            console.print(f"[green]✅ {message}[/green]")
        else:
            console.print(f"[red]❌ {message}[/red]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.option('--branch', '-b', help='Branch to pull (default: current)')
@click.option('--path', '-p', default='.', help='Repository path')
def pull(branch, path):
    """Pull changes from GitHub."""
    try:
        from forge.core.github import GitHubManager
        manager = check_github_available()
        if not manager:
            return
        
        success, message = manager.pull(path, branch=branch)
        
        if success:
            console.print(f"[green]✅ {message}[/green]")
        else:
            console.print(f"[red]❌ {message}[/red]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.argument('repo_name')
@click.option('--state', '-s', type=click.Choice(['open', 'closed', 'all']),
              default='open', help='PR state')
def pr_list(repo_name, state):
    """List pull requests for a repository."""
    manager = check_github_available()
    if not manager:
        return
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description=f"Fetching PRs for {repo_name}...", total=None)
            prs = manager.list_pull_requests(repo_name, state=state)
        
        if not prs:
            console.print(f"[yellow]No {state} pull requests found[/yellow]")
            return
        
        table = Table(title=f"Pull Requests for {repo_name}")
        table.add_column("#", justify="right", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Branch", style="green")
        table.add_column("Author", style="yellow")
        table.add_column("State", style="magenta")
        
        for pr in prs:
            table.add_row(
                str(pr['number']),
                pr['title'][:40] + ('...' if len(pr['title']) > 40 else ''),
                f"{pr['head_branch']} → {pr['base_branch']}",
                pr['user'],
                pr['state']
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.argument('title', nargs=-1, required=True)
@click.option('--repo', '-r', required=True, help='Repository name (owner/repo)')
@click.option('--head', '-h', required=True, help='Head branch')
@click.option('--base', '-b', default='main', help='Base branch')
@click.option('--body', '-B', default='', help='PR description')
def pr_create(title, repo, head, base, body):
    """Create a pull request."""
    full_title = ' '.join(title)
    manager = check_github_available()
    if not manager:
        return
    
    success, message = manager.create_pull_request(repo, full_title, head, base, body)
    
    if success:
        console.print(f"[green]✅ {message}[/green]")
    else:
        console.print(f"[red]❌ {message}[/red]")


@github.command()
@click.argument('repo_name')
@click.option('--state', '-s', type=click.Choice(['open', 'closed', 'all']),
              default='open', help='Issue state')
def issue_list(repo_name, state):
    """List issues for a repository."""
    manager = check_github_available()
    if not manager:
        return
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description=f"Fetching issues for {repo_name}...", total=None)
            issues = manager.list_issues(repo_name, state=state)
        
        if not issues:
            console.print(f"[yellow]No {state} issues found[/yellow]")
            return
        
        table = Table(title=f"Issues for {repo_name}")
        table.add_column("#", justify="right", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Labels", style="yellow")
        table.add_column("Author", style="green")
        table.add_column("State", style="magenta")
        
        for issue in issues:
            labels = ', '.join(issue['labels'][:3])
            table.add_row(
                str(issue['number']),
                issue['title'][:40] + ('...' if len(issue['title']) > 40 else ''),
                labels[:20],
                issue['user'],
                issue['state']
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.argument('title', nargs=-1, required=True)
@click.option('--repo', '-r', required=True, help='Repository name (owner/repo)')
@click.option('--body', '-B', default='', help='Issue description')
@click.option('--labels', '-l', multiple=True, help='Labels to add')
def issue_create(title, repo, body, labels):
    """Create an issue on GitHub."""
    full_title = ' '.join(title)
    manager = check_github_available()
    if not manager:
        return
    
    success, message = manager.create_issue(repo, full_title, body, list(labels) if labels else None)
    
    if success:
        console.print(f"[green]✅ {message}[/green]")
    else:
        console.print(f"[red]❌ {message}[/red]")


@github.command()
@click.argument('branch_name')
@click.option('--path', '-p', default='.', help='Repository path')
def branch_create(branch_name, path):
    """Create a new branch."""
    try:
        from forge.core.github import GitHubManager
        manager = check_github_available()
        if not manager:
            return
        
        success, message = manager.create_branch(path, branch_name)
        
        if success:
            console.print(f"[green]✅ {message}[/green]")
        else:
            console.print(f"[red]❌ {message}[/red]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.argument('branch_name')
@click.option('--path', '-p', default='.', help='Repository path')
def branch_switch(branch_name, path):
    """Switch to a branch."""
    try:
        from forge.core.github import GitHubManager
        manager = check_github_available()
        if not manager:
            return
        
        success, message = manager.switch_branch(path, branch_name)
        
        if success:
            console.print(f"[green]✅ {message}[/green]")
        else:
            console.print(f"[red]❌ {message}[/red]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.argument('path', required=False)
def status(path):
    """Show git status of local repository."""
    try:
        from forge.core.github import GitHubManager
        manager = GitHubManager()
        status_data = manager.get_local_status(path)
        
        if not status_data:
            console.print("[red]Not a git repository[/red]")
            return
        
        console.print(f"\n[bold]On branch:[/bold] [cyan]{status_data['branch']}[/cyan]\n")
        
        if not status_data['is_dirty'] and not status_data['untracked']:
            console.print("[green]Working tree clean[/green]")
        else:
            if status_data['untracked']:
                console.print(f"[yellow]Untracked files ({len(status_data['untracked'])}):[/yellow]")
                for f in status_data['untracked'][:10]:
                    console.print(f"  ? {f}")
                if len(status_data['untracked']) > 10:
                    console.print(f"  ... and {len(status_data['untracked']) - 10} more")
            
            if status_data['modified']:
                console.print(f"\n[yellow]Modified files ({len(status_data['modified'])}):[/yellow]")
                for f in status_data['modified'][:10]:
                    console.print(f"  M {f}")
                if len(status_data['modified']) > 10:
                    console.print(f"  ... and {len(status_data['modified']) - 10} more")
            
            if status_data['staged']:
                console.print(f"\n[green]Staged files ({len(status_data['staged'])}):[/green]")
                for f in status_data['staged'][:10]:
                    console.print(f"  A {f}")
                if len(status_data['staged']) > 10:
                    console.print(f"  ... and {len(status_data['staged']) - 10} more")
        
        console.print()
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@github.command()
@click.option('--path', '-p', default='.', help='Repository path')
@click.option('--limit', '-l', type=int, default=10, help='Number of commits')
def log(path, limit):
    """Show commit history."""
    try:
        from forge.core.github import GitHubManager
        manager = GitHubManager()
        commits = manager.get_commit_history(path, limit=limit)
        
        if not commits:
            console.print("[yellow]No commit history found[/yellow]")
            return
        
        table = Table(title="Recent Commits")
        table.add_column("SHA", style="cyan", width=8)
        table.add_column("Message", style="white")
        table.add_column("Author", style="yellow")
        table.add_column("Date", style="green")
        
        for commit in commits:
            table.add_row(
                commit['sha'],
                commit['message'][:50] + ('...' if len(commit['message']) > 50 else ''),
                commit['author_email'].split('@')[0],
                commit['date'][:10]
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
