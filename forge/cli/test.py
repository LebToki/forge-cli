"""Testing and debugging CLI commands for FORGE."""

import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.testing import TestGenerator
from ..core.profiler import Profiler
from ..ui.styling import console

console = Console()


@click.group()
def test():
    """Testing and profiling commands."""
    pass


@test.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file for tests')
@click.option('--run/--no-run', default=False, help='Run tests after generation')
def generate(filepath, output, run):
    """Generate tests for a file using AI."""
    path = Path(filepath)
    
    if not path.exists():
        console.print(f"[red]File not found: {filepath}[/red]")
        return
    
    code = path.read_text()
    language = "python" if path.suffix == '.py' else "unknown"
    
    if language != "python":
        console.print("[yellow]Only Python files are supported[/yellow]")
        return
    
    console.print(f"\n[bold cyan]📋 Analyzing {path.name}...[/bold cyan]")
    
    try:
        generator = TestGenerator()
        
        # Analyze code
        analysis = generator.analyze_code(code, language)
        console.print(f"  Functions: {len(analysis['functions'])}")
        console.print(f"  Classes: {len(analysis['classes'])}")
        
        # Generate tests
        console.print("\n[bold cyan]🤖 Generating tests...[/bold cyan]")
        tests = generator.generate_tests(code, language)
        
        # Save tests
        test_file = generator.save_tests(tests, path, Path(output) if output else None)
        console.print(f"\n[green]✅ Tests saved to: {test_file}[/green]")
        
        # Show preview
        preview = tests[:500] + ("..." if len(tests) > 500 else "")
        syntax = Syntax(preview, "python", theme="monokai")
        console.print(Panel(syntax, title="Generated Tests Preview", border_style="green"))
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@test.command()
@click.argument('filepath', type=click.Path(exists=True))
def profile(filepath):
    """Profile a Python file."""
    path = Path(filepath)
    
    if not path.exists():
        console.print(f"[red]File not found: {filepath}[/red]")
        return
    
    if path.suffix != '.py':
        console.print("[yellow]Only Python files are supported[/yellow]")
        return
    
    console.print(f"\n[bold cyan]⏱️  Profiling {path.name}...[/bold cyan]")
    
    try:
        profiler = Profiler()
        
        # Create namespace and run
        namespace = {}
        profiler.start()
        
        exec(path.read_text(), namespace)
        
        results = profiler.stop()
        profiler.display_stats(results)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@test.command()
@click.argument('filepath', type=click.Path(exists=True))
def analyze(filepath):
    """Analyze code and suggest improvements."""
    path = Path(filepath)
    
    if not path.exists():
        console.print(f"[red]File not found: {filepath}[/red]")
        return
    
    code = path.read_text()
    language = "python" if path.suffix == '.py' else "unknown"
    
    console.print(f"\n[bold cyan]🔍 Analyzing {path.name}...[/bold cyan]")
    
    try:
        generator = TestGenerator()
        analysis = generator.analyze_code(code, language)
        
        # Display analysis
        table = Table(title="Code Analysis", show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Language", language)
        table.add_row("Functions", str(len(analysis['functions'])))
        table.add_row("Classes", str(len(analysis['classes'])))
        table.add_row("Complexity", analysis['complexity'])
        
        console.print(table)
        
        # Show functions
        if analysis['functions']:
            console.print("\n[bold]Functions found:[/bold]")
            for func in analysis['functions'][:10]:
                args = ', '.join(func['args']) if func['args'] else '()'
                console.print(f"  • {func['name']}({args})")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@test.command()
@click.argument('filepath', type=click.Path(exists=True))
def suggest(filepath):
    """Suggest test cases for a file."""
    path = Path(filepath)
    
    if not path.exists():
        console.print(f"[red]File not found: {filepath}[/red]")
        return
    
    code = path.read_text()
    
    console.print(f"\n[bold cyan]💡 Generating test suggestions...[/bold cyan]")
    console.print("[yellow]Note: Install pytest for full test generation[/yellow]")
    
    try:
        generator = TestGenerator()
        analysis = generator.analyze_code(code, "python")
        
        # Show suggestions
        console.print(f"\n[bold]Suggested test cases for {path.name}:[/bold]\n")
        
        for func in analysis['functions']:
            console.print(f"  • Test {func['name']} with normal inputs")
            if func['args']:
                console.print(f"  • Test {func['name']} with edge cases")
                console.print(f"  • Test {func['name']} with invalid inputs")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
