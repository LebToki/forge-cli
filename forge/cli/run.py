"""Command execution CLI for FORGE."""

import os
import sys
import shlex
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich import print as rprint
import time

from forge.core.executor import CommandExecutor, CodeRunner
from forge.core.llm import DeepSeekClient
from forge.ui.styling import console

console = Console()


@click.group()
def run():
    """Run commands and execute code."""
    pass


@run.command()
@click.argument('command', nargs=-1, required=True)
@click.option('--cwd', '-C', help='Working directory')
@click.option('--timeout', '-t', default=60, help='Timeout in seconds')
@click.option('--analyze/--no-analyze', default=True, help='Analyze output with AI')
@click.option('--env', '-e', multiple=True, help='Environment variables (KEY=VALUE)')
def cmd(command, cwd, timeout, analyze, env):
    """Run a shell command with live output."""
    full_command = ' '.join(command)
    
    # Parse environment variables
    env_vars = {}
    for e in env:
        if '=' in e:
            key, value = e.split('=', 1)
            env_vars[key] = value
    
    # Set working directory
    workspace = Path(cwd) if cwd else Path.cwd()
    
    console.print(f"\n[bold blue]⚡ Running:[/bold blue] [yellow]{full_command}[/yellow]")
    console.print(f"[dim]Directory: {workspace}[/dim]\n")
    
    executor = CommandExecutor(workspace=workspace, timeout=timeout)
    
    stdout_lines = []
    stderr_lines = []
    
    try:
        # Stream output
        with Live(console=console, refresh_per_second=10, vertical_overflow="visible") as live:
            output_text = ""
            for chunk in executor.run(full_command, stream=True, env=env_vars):
                if isinstance(chunk, dict):
                    if chunk["type"] == "stdout":
                        line = chunk["line"]
                        stdout_lines.append(line)
                        output_text += f"[green]{line}[/green]\n"
                    else:
                        line = chunk["line"]
                        stderr_lines.append(line)
                        output_text += f"[red]{line}[/red]\n"
                    
                    live.update(Panel(
                        output_text,
                        title="Output",
                        border_style="blue"
                    ))
        
        # Get final result
        result = {
            "command": full_command,
            "stdout": stdout_lines,
            "stderr": stderr_lines,
            "returncode": executor.process.returncode if executor.process else -1,
            "success": executor.process.returncode == 0 if executor.process else False
        }
        
        # Show summary
        console.print("\n")
        if result["success"]:
            console.print(f"[green]✅ Command completed successfully[/green]")
        else:
            console.print(f"[red]❌ Command failed with code {result['returncode']}[/red]")
        
        # Analyze with AI if requested
        if analyze and (stderr_lines or not result["success"]):
            console.print("\n[yellow]🔍 Analyzing output with DeepSeek...[/yellow]")
            
            client = DeepSeekClient()
            
            # Prepare context
            context = f"""
Command: {full_command}
Return code: {result['returncode']}

STDOUT:
{chr(10).join(stdout_lines[-20:])}

STDERR:
{chr(10).join(stderr_lines[-20:])}
"""
            
            messages = [
                {"role": "system", "content": "You are a debugging assistant. Analyze command output and explain what went wrong."},
                {"role": "user", "content": context}
            ]
            
            analysis = client.chat(messages)
            console.print(Panel(analysis, title="DeepSeek Analysis", border_style="yellow"))
        
    except TimeoutError as e:
        console.print(f"[red]⏰ Timeout: {e}[/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Command interrupted by user[/yellow]")
        executor.kill_process()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@run.command()
@click.argument('code', required=False)
@click.option('--lang', '-l', help='Programming language')
@click.option('--file', '-f', help='Read code from file')
@click.option('--args', '-a', help='Arguments to pass to the program')
@click.option('--analyze/--no-analyze', default=True, help='Analyze output with AI')
def code(code, lang, file, args, analyze):
    """Execute code in various languages."""
    runner = CodeRunner()
    
    # Get code from file or argument
    if file:
        path = Path(file)
        if not path.exists():
            console.print(f"[red]File not found: {file}[/red]")
            return
        code_content = path.read_text()
        filename = file
    elif code:
        code_content = code
        filename = None
    else:
        console.print("[red]Error: No code provided. Use --file or provide code as argument.[/red]")
        return
    
    # Parse arguments
    cmd_args = shlex.split(args) if args else []
    
    # Detect language and check dependencies
    detected_lang, config = runner.detect_language(code_content, filename, lang)
    console.print(f"[blue]📋 Language:[/blue] [bold]{detected_lang}[/bold]")
    
    # Check dependencies
    has_deps, version = runner.check_dependencies(detected_lang)
    if not has_deps:
        console.print(f"[red]❌ {version}[/red]")
        console.print(f"\n[yellow]Tip: Install {detected_lang} to run this code[/yellow]")
        return
    else:
        console.print(f"[green]✅ {detected_lang} {version}[/green]\n")
    
    # Show code preview
    preview_lines = code_content.splitlines()[:10]
    preview = '\n'.join(preview_lines)
    if len(code_content.splitlines()) > 10:
        preview += f"\n[dim]... and {len(code_content.splitlines()) - 10} more lines[/dim]"
    
    console.print(Panel(
        Syntax(preview, detected_lang, theme="monokai"),
        title="Code Preview",
        border_style="blue"
    ))
    
    console.print(f"\n[bold blue]⚡ Executing...[/bold blue]\n")
    
    stdout_lines = []
    stderr_lines = []
    
    try:
        # Run code
        with Live(console=console, refresh_per_second=10, vertical_overflow="visible") as live:
            output_text = ""
            for chunk in runner.run_code(code_content, detected_lang, filename, cmd_args, stream=True):
                if isinstance(chunk, dict):
                    if chunk["type"] == "stdout":
                        line = chunk["line"]
                        stdout_lines.append(line)
                        output_text += f"[green]{line}[/green]\n"
                    else:
                        line = chunk["line"]
                        stderr_lines.append(line)
                        output_text += f"[red]{line}[/red]\n"
                    
                    live.update(Panel(
                        output_text,
                        title="Output",
                        border_style="blue"
                    ))
        
        # Show summary
        console.print("\n")
        if not stderr_lines:
            console.print("[green]✅ Code executed successfully[/green]")
        else:
            console.print("[yellow]⚠️ Code executed with warnings/errors[/yellow]")
        
        # Analyze with AI if requested
        if analyze and stderr_lines:
            console.print("\n[yellow]🔍 Analyzing output with DeepSeek...[/yellow]")
            
            client = DeepSeekClient()
            
            context = f"""
Language: {detected_lang}
Code:
```{detected_lang}
{code_content}
```
Output:
STDOUT:
{chr(10).join(stdout_lines[-20:])}

STDERR:
{chr(10).join(stderr_lines[-20:])}
"""
            
            messages = [
                {"role": "system", "content": "You are a debugging assistant. Analyze code output and help fix issues."},
                {"role": "user", "content": context}
            ]
            
            analysis = client.chat(messages)
            console.print(Panel(analysis, title="DeepSeek Analysis", border_style="yellow"))
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@run.command()
@click.argument('path')
@click.option('--args', '-a', help='Arguments to pass')
@click.option('--analyze/--no-analyze', default=True, help='Analyze output with AI')
def file(path, args, analyze):
    """Execute a code file."""
    runner = CodeRunner()
    
    if not Path(path).exists():
        console.print(f"[red]File not found: {path}[/red]")
        return
    
    # Detect language from file
    ext = Path(path).suffix
    lang_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.sh': 'bash',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
    }
    
    lang = lang_map.get(ext)
    if not lang:
        console.print(f"[red]Unknown file type: {ext}[/red]")
        return
    
    # Parse arguments
    cmd_args = shlex.split(args) if args else []
    
    # Check dependencies
    has_deps, version = runner.check_dependencies(lang)
    if not has_deps:
        console.print(f"[red]❌ {version}[/red]")
        console.print(f"\n[yellow]Tip: Install {lang} to run this file[/yellow]")
        return
    
    console.print(f"[green]✅ {lang} {version}[/green]\n")
    
    # Read and show file
    content = Path(path).read_text()
    console.print(Panel(
        Syntax(content, lang, theme="monokai", line_numbers=True),
        title=f"File: {path}",
        border_style="blue"
    ))
    
    console.print(f"\n[bold blue]⚡ Executing {path}...[/bold blue]\n")
    
    try:
        result = runner.run_file(path, cmd_args, stream=False)
        
        if result.get("stdout"):
            console.print("\n[bold]Output:[/bold]")
            for line in result["stdout"]:
                console.print(f"  [green]{line}[/green]")
        
        if result.get("stderr"):
            console.print("\n[bold red]Errors:[/bold red]")
            for line in result["stderr"]:
                console.print(f"  [red]{line}[/red]")
        
        if result.get("success"):
            console.print(f"\n[green]✅ Command completed successfully[/green]")
        else:
            console.print(f"\n[red]❌ Command failed with code {result.get('returncode', -1)}[/red]")
        
        # Analyze with AI
        if analyze and result.get("stderr"):
            console.print("\n[yellow]🔍 Analyzing with DeepSeek...[/yellow]")
            
            client = DeepSeekClient()
            
            context = f"""
File: {path}
Language: {lang}

Code:
```{lang}
{content}
```

Output:
STDOUT:
{chr(10).join(result.get('stdout', [])[-20:])}

STDERR:
{chr(10).join(result.get('stderr', [])[-20:])}
"""
            
            messages = [
                {"role": "system", "content": "You are a debugging assistant. Analyze code output and help fix issues."},
                {"role": "user", "content": context}
            ]
            
            analysis = client.chat(messages)
            console.print(Panel(analysis, title="DeepSeek Analysis", border_style="yellow"))
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@run.command()
def list():
    """List available language runtimes."""
    runner = CodeRunner()
    
    table = Table(title="Available Languages", show_header=True, header_style="bold cyan")
    table.add_column("Language", style="cyan")
    table.add_column("Extension", style="yellow")
    table.add_column("Status", style="green")
    table.add_column("Version", style="blue")
    
    for lang, config in runner.LANGUAGE_CONFIGS.items():
        has_deps, version = runner.check_dependencies(lang)
        if has_deps:
            status = "✅ Installed"
            version_display = version.split('\n')[0][:50]
        else:
            status = "❌ Not found"
            version_display = ""
        
        table.add_row(
            lang.capitalize(),
            config["extension"],
            status,
            version_display
        )
    
    console.print(table)
