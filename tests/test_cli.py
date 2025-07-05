import subprocess
from pathlib import Path

def test_cli_create_folder(tmp_path):
    """
    Test the CLI's create-folder command.

    Ensures the command creates the specified folder successfully and returns a success message.
    """
    test_folder = tmp_path / "test_cli_folder"
    result = subprocess.run(
        ["python3", "cli.py", "create-folder", str(test_folder)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert test_folder.exists()
    assert "Created folder" in result.stdout


def test_cli_create_file(tmp_path):
    """
    Test the CLI's create-file command with text content.

    Verifies that the file is created with the correct contents and that output confirms success.
    """
    test_file = tmp_path / "test_cli_file.txt"
    result = subprocess.run(
        ["python3", "cli.py", "create-file", str(test_file), "--text", "hello world"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert test_file.exists()
    assert test_file.read_text() == "hello world"
    assert "Created file" in result.stdout


def test_cli_move_file(tmp_path):
    """
    Test the CLI's move command.

    Ensures a file is successfully moved from source to destination and retains its content.
    """
    source = tmp_path / "source.txt"
    destination_dir = tmp_path / "destination"
    destination_dir.mkdir()
    destination = destination_dir / "source.txt"
    source.write_text("test content")

    result = subprocess.run(
        ["python3", "cli.py", "move", str(source), str(destination)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert destination.exists()
    assert destination.read_text() == "test content"
    assert "Moved to" in result.stdout


def test_cli_view_file(tmp_path):
    """
    Test the CLI's view command.

    Verifies that file contents are correctly displayed in the output.
    """
    test_file = tmp_path / "test_view.txt"
    test_file.write_text("view this")

    result = subprocess.run(
        ["python3", "cli.py", "view", str(test_file)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "view this" in result.stdout


def test_cli_help():
    """
    Test the CLI's help command.

    Ensures the help message lists all available commands and usage instructions.
    """
    result = subprocess.run(
        ["python3", "cli.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
    assert "create-file" in result.stdout
    assert "create-folder" in result.stdout