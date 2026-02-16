#!/usr/bin/env python
"""FORGE CLI - Your DeepSeek-powered development forge."""

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich import print as rprint

from forge.core.llm import DeepSeekClient
from forge import __version__
from forge.cli.fs import fs
from forge.cli.run import run
from forge.cli.github import github
from forge.cli.test import test

console = Console()


def show_banner():
    """Display the FORGE banner on startup."""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   ███████╗ ██████╗ ██████╗  ██████╗ ███████╗            ║
    ║   ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝            ║
    ║   █████╗  ██║   ██║██████╔╝██║  ███╗█████╗              ║
    ║   ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝              ║
    ║   ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗            ║
    ║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝            ║
    ║                                                          ║
    ║              🔥 Shape Code • Ship Faster 🔥             ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold orange1")


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help='Show version and exit')
@click.pass_context
def cli(ctx, version):
    """🔥 FORGE - Your DeepSeek-powered development forge."""
    if version:
        console.print(f"FORGE version [bold orange1]{__version__}[/bold orange1]")
        sys.exit(0)
    
    if ctx.invoked_subcommand is None:
        # No command provided, show banner and help
        show_banner()
        console.print("\n[yellow]Usage:[/yellow] forge [OPTIONS] COMMAND [ARGS]...\n")
        console.print("Commands:")
        console.print("  [bold]ask[/bold]     Ask DeepSeek a question")
        console.print("  [bold]config[/bold]  Configure FORGE settings")
        console.print("\nRun [cyan]forge COMMAND --help[/cyan] for more info.\n")


@cli.command()
@click.argument('prompt', nargs=-1, required=True)
@click.option('--file', '-f', multiple=True, help='Include file contents in context')
@click.option('--model', default='deepseek-chat', help='DeepSeek model to use')
def ask(prompt, file, model):
    """Ask DeepSeek a question about code or development."""
    full_prompt = ' '.join(prompt)
    
    # Check for API key
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        console.print("[red]Error:[/red] DEEPSEEK_API_KEY environment variable not set.")
        console.print("Set it with: [cyan]export DEEPSEEK_API_KEY='your-key'[/cyan]")
        sys.exit(1)
    
    # Show what we're doing
    console.print(f"\n[bold orange1]🔨 Forging answer...[/bold orange1]")
    
    # Handle file includes
    file_contents = []
    if file:
        console.print("\n📁 Including files:")
        for f in file:
            path = Path(f)
            if path.exists():
                try:
                    content = path.read_text()
                    file_contents.append(f"File: {f}\n```\n{content}\n```\n")
                    console.print(f"  [green]✓[/green] {f}")
                except Exception as e:
                    console.print(f"  [red]✗[/red] {f} (error reading: {e})")
            else:
                console.print(f"  [red]✗[/red] {f} (not found)")
    
    # Build the prompt with file context
    if file_contents:
        full_prompt = "Here are the files I'm working with:\n\n" + "\n".join(file_contents) + f"\n\nMy question: {full_prompt}"
    
    try:
        client = DeepSeekClient(api_key=api_key)
        messages = [{"role": "user", "content": full_prompt}]
        
        console.print("\n[dim]DeepSeek is thinking...[/dim]\n")
        
        # Stream the response
        stream = client.stream_chat(messages, model=model)
        
        collected = []
        with Live(console=console, refresh_per_second=10, vertical_overflow="visible") as live:
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    collected.append(token)
                    text = Text("".join(collected), style="bold green")
                    live.update(text)
        
        console.print()  # Newline after streaming
        
    except Exception as e:
        console.print(f"\n[red]Error calling DeepSeek API:[/red] {e}")


@cli.group()
def config():
    """Configure FORGE settings."""
    pass


@config.command('set')
@click.argument('key')
@click.argument('value')
def set_config(key, value):
    """Set a configuration value (e.g., deepseek.api_key YOUR_KEY)."""
    # For now, just show what would happen
    console.print(f"[yellow]Note:[/yellow] Config storage coming soon!")
    console.print(f"Would set: [cyan]{key} = {value}[/cyan]")
    
    # In the future, this will write to ~/.forge/config.toml
    config_dir = Path.home() / ".forge"
    config_dir.mkdir(exist_ok=True)
    console.print(f"Future config location: [dim]{config_dir / 'config.toml'}[/dim]")


@config.command('list')
def list_config():
    """List all configuration values."""
    console.print("[bold]Current Configuration:[/bold]\n")
    console.print("  [yellow]deepseek.api_key[/yellow] = ", end="")
    if os.getenv('DEEPSEEK_API_KEY'):
        console.print("[green]✓ set via environment[/green]")
    else:
        console.print("[red]not set[/red] (use DEEPSEEK_API_KEY env var)")
    
    console.print("\n[bold]Environment:[/bold]")
    has_key = os.getenv('DEEPSEEK_API_KEY')
    status = "[green]present[/green]" if has_key else "[red]missing[/red]"
    console.print(f"  DEEPSEEK_API_KEY: {status}")


@cli.command()
@click.argument('description', nargs=-1, required=True)
def task(description):
    """Execute a development task (coming soon: file edits, commands, GitHub PRs)."""
    full_description = ' '.join(description)
    
    console.print("\n[bold orange1]🔨 Starting forge task...[/bold orange1]")
    console.print(Panel(full_description, title="Task Description", border_style="orange1"))
    console.print("\n[yellow]Task execution coming soon! This will:[/yellow]")
    console.print("  • Read/write files")
    console.print("  • Run commands")
    console.print("  • Create commits")
    console.print("  • Open pull requests")
    console.print("\n[cyan]Stay tuned for Phase 2![/cyan]")


# Register subcommands
cli.add_command(fs)
cli.add_command(run)
cli.add_command(github)
cli.add_command(test)


if __name__ == '__main__':
    cli()
