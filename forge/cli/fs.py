"""File system commands for FORGE."""

import os
import sys
from pathlib import Path
from datetime import datetime
import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.syntax import Syntax
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from rich.live import Live
from rich.text import Text

from forge.core.filesystem import FileSystemTool
from forge.core.llm import DeepSeekClient
from forge.ui.styling import console

console = Console()


def format_size(size: int) -> str:
    """Format file size human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def format_time(timestamp: float) -> str:
    """Format timestamp."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


@click.group()
def fs():
    """File system operations."""
    pass


@fs.command()
@click.argument('path', default='.')
@click.option('--recursive', '-r', is_flag=True, help='Show recursively')
@click.option('--all', '-a', 'show_all', is_flag=True, help='Show all files (including hidden)')
def ls(path, recursive, show_all):
    """List directory contents with beautiful tree view."""
    try:
        fs_tool = FileSystemTool()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Scanning directory...", total=None)
            items = fs_tool.list_directory(path, recursive=recursive)
        
        if not items:
            console.print("[yellow]Directory is empty[/yellow]")
            return
        
        # Create tree
        tree = Tree(f"📁 [bold blue]{path}/[/bold blue]")
        node_map = {Path(path).resolve(): tree}
        
        # Sort items: directories first, then files
        items.sort(key=lambda p: (not p.is_dir(), p.name))
        
        for item in items:
            if not show_all and item.name.startswith('.'):
                continue
            
            parent = item.parent
            if parent not in node_map:
                # Create parent nodes if needed
                parents = []
                while parent not in node_map and parent != Path(path).resolve():
                    parents.append(parent)
                    parent = parent.parent
                
                for p in reversed(parents):
                    node = Tree(f"📁 [cyan]{p.name}/[/cyan]")
                    node_map[p] = node
                    node_map[p.parent].add(node)
            
            # Add item to tree
            if item.is_dir():
                node = Tree(f"📁 [cyan]{item.name}/[/cyan]")
                node_map[item] = node
                node_map[item.parent].add(node)
            else:
                size = format_size(item.stat().st_size)
                node_map[item.parent].add(f"📄 [green]{item.name}[/green] [dim]({size})[/dim]")
        
        console.print(tree)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('path')
@click.option('--lines', '-n', type=int, help='Show only first N lines')
@click.option('--language', '-l', help='Force syntax highlighting language')
def cat(path, lines, language):
    """Display file contents with syntax highlighting."""
    try:
        fs_tool = FileSystemTool()
        content, ext = fs_tool.read_file(path)
        
        # Truncate if lines specified
        if lines:
            content_lines = content.splitlines()
            if len(content_lines) > lines:
                content = '\n'.join(content_lines[:lines])
                content += f"\n\n[dim]... and {len(content_lines) - lines} more lines[/dim]"
        
        # Determine language for syntax highlighting
        lang = language or ext or 'text'
        
        # Create syntax highlighted output
        syntax = Syntax(content, lang, theme="monokai", line_numbers=True)
        
        # Show file info
        info = fs_tool.get_file_info(path)
        header = f"📄 [bold]{path}[/bold] - {format_size(info['size'])} - Modified: {format_time(info['modified'])}"
        
        console.print(Panel(syntax, title=header, border_style="green"))
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('path')
@click.argument('content', required=False)
@click.option('--edit', '-e', is_flag=True, help='Open in editor (coming soon)')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing file')
@click.option('--prompt', '-p', help='Use AI to generate content from prompt')
def write(path, content, edit, force, prompt):
    """Write content to a file."""
    try:
        fs_tool = FileSystemTool()
        
        # Handle AI-generated content
        if prompt:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="AI generating content...", total=None)
                
                client = DeepSeekClient()
                messages = [
                    {"role": "system", "content": "You are a helpful coding assistant. Generate the requested content."},
                    {"role": "user", "content": f"Generate content for a file. Request: {prompt}"}
                ]
                content = client.chat(messages)
        
        if not content and not edit:
            console.print("[red]Error:[/red] No content provided. Use --prompt, --edit, or provide content argument.")
            return
        
        # Write file
        fs_tool.write_file(path, content, force=force)
        console.print(f"[green]✓[/green] Written to [bold]{path}[/bold]")
        
        # Show preview
        preview_lines = content.splitlines()[:10]
        preview = '\n'.join(preview_lines)
        if len(content.splitlines()) > 10:
            preview += f"\n[dim]... and {len(content.splitlines()) - 10} more lines[/dim]"
        
        console.print(Panel(preview, title="Preview", border_style="blue"))
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('source')
@click.argument('destination', required=False)
@click.option('--recursive', '-r', is_flag=True, help='Copy directories recursively')
def cp(source, destination, recursive):
    """Copy files or directories."""
    try:
        fs_tool = FileSystemTool()
        
        if not destination:
            # Generate default destination
            src_path = Path(source)
            dest_path = src_path.parent / f"{src_path.stem}_copy{src_path.suffix}"
            destination = str(dest_path)
        
        fs_tool.copy_file(source, destination)
        console.print(f"[green]✓[/green] Copied [bold]{source}[/bold] → [bold]{destination}[/bold]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('source')
@click.argument('destination')
def mv(source, destination):
    """Move or rename files/directories."""
    try:
        fs_tool = FileSystemTool()
        fs_tool.move_file(source, destination)
        console.print(f"[green]✓[/green] Moved [bold]{source}[/bold] → [bold]{destination}[/bold]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('path')
@click.option('--force', '-f', is_flag=True, help='Force delete (use with caution)')
def rm(path, force):
    """Delete files or empty directories."""
    try:
        fs_tool = FileSystemTool()
        
        # Get info for confirmation
        info = fs_tool.get_file_info(path)
        
        # Confirm deletion
        if not force:
            type_str = "directory" if info['type'] == 'directory' else "file"
            console.print(f"[yellow]Warning:[/yellow] About to delete {type_str}: [bold]{path}[/bold]")
            if not click.confirm("Continue?"):
                console.print("[yellow]Cancelled[/yellow]")
                return
        
        fs_tool.delete_file(path, force=force)
        console.print(f"[green]✓[/green] Deleted [bold]{path}[/bold]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('pattern')
@click.option('--path', '-p', default='.', help='Search path')
@click.option('--content', '-c', is_flag=True, help='Search file contents (coming soon)')
def search(pattern, path, content):
    """Search for files matching pattern."""
    try:
        fs_tool = FileSystemTool()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Searching...", total=None)
            results = fs_tool.search_files(pattern, path)
        
        if not results:
            console.print(f"[yellow]No files found matching '{pattern}'[/yellow]")
            return
        
        # Display results
        console.print(f"[green]Found {len(results)} files:[/green]\n")
        for file_path in results[:20]:  # Limit to 20 results
            rel_path = file_path.relative_to(Path.cwd())
            size = format_size(file_path.stat().st_size)
            console.print(f"  📄 [cyan]{rel_path}[/cyan] [dim]({size})[/dim]")
        
        if len(results) > 20:
            console.print(f"\n[dim]... and {len(results) - 20} more files[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('file1')
@click.argument('file2')
def diff(file1, file2):
    """Show differences between two files."""
    try:
        fs_tool = FileSystemTool()
        diff_text = fs_tool.diff_files(file1, file2)
        
        if not diff_text:
            console.print("[green]Files are identical[/green]")
            return
        
        # Colorize diff
        syntax = Syntax(diff_text, "diff", theme="monokai")
        console.print(Panel(syntax, title=f"Diff: {file1} ↔ {file2}", border_style="yellow"))
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('path', default='.')
def info(path):
    """Show detailed information about a file or directory."""
    try:
        fs_tool = FileSystemTool()
        info_data = fs_tool.get_file_info(path)
        
        # Create info table
        table = Table(title=f"Info: {path}", show_header=False, box=None)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Type", info_data['type'])
        table.add_row("Size", format_size(info_data['size']))
        table.add_row("Created", format_time(info_data['created']))
        table.add_row("Modified", format_time(info_data['modified']))
        table.add_row("Permissions", info_data['permissions'])
        
        if 'extension' in info_data:
            table.add_row("Extension", info_data['extension'])
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@fs.command()
@click.argument('path')
@click.argument('question', nargs=-1, required=True)
def ask(path, question):
    """Ask DeepSeek about a file's contents."""
    full_question = ' '.join(question)
    
    try:
        fs_tool = FileSystemTool()
        content, ext = fs_tool.read_file(path)
        
        # Prepare context
        context = f"File: {path}\nExtension: {ext}\n\nContent:\n```\n{content}\n```\n\nQuestion: {full_question}"
        
        # Ask DeepSeek
        client = DeepSeekClient()
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant. Answer questions about the provided file."},
            {"role": "user", "content": context}
        ]
        
        console.print(f"\n[bold orange1]🔨 Analyzing {path}...[/bold orange1]\n")
        
        # Stream response
        stream = client.stream_chat(messages)
        
        collected = []
        with Live(console=console, refresh_per_second=10) as live:
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    collected.append(token)
                    text = Text("".join(collected), style="bold green")
                    live.update(text)
        
        console.print()  # Newline
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
