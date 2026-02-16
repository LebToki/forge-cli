"""Test the FORGE CLI."""

import pytest
from click.testing import CliRunner
from forge.cli.main import cli


def test_version():
    """Test version flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert 'FORGE version' in result.output


def test_ask_no_key():
    """Test ask command without API key."""
    runner = CliRunner()
    result = runner.invoke(cli, ['ask', 'Hello'])
    assert result.exit_code == 1
    assert 'DEEPSEEK_API_KEY' in result.output


def test_config_list():
    """Test config list command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['config', 'list'])
    assert result.exit_code == 0
    assert 'Configuration' in result.output
