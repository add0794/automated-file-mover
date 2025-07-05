"""
test_manager.py - Unit tests for FileManager class.

Purpose: Unit testing individual methods in FileManager.

What it checks:
• If methods like create_file, move, delete, etc. work in isolation
• Handles direct calls to Python functions
• Focuses on logic and expected outputs
• Tests edge cases and error handling at the method level

Example usage:
    python -m pytest tests/test_manager.py
"""

import sys
from pathlib import Path
import shutil
import pytest

# Add the project root directory to sys.path (for local testing only)
sys.path.append(str(Path(__file__).resolve().parent.parent))

from manager import FileManager

@pytest.fixture
def file_manager():
    """
    Provides a FileManager instance using the user's home directory.
    """
    return FileManager()

def test_create_file(file_manager):
    """
    Test that a new file is created with the correct content.
    """
    file_path = file_manager.create_file("testfile.txt", content="Hello, world!")
    assert file_path.exists()
    assert file_path.read_text() == "Hello, world!"
    file_path.unlink()

def test_create_file_with_removed_chars(file_manager):
    """
    Test that specified characters are removed from the content before saving.
    """
    file_path = file_manager.create_file("cleaned.txt", content="Hello, world!", remove_chars="lo")
    assert file_path.read_text() == "He, wrd!"
    file_path.unlink()

def test_create_folder(file_manager):
    """
    Test that a new folder is created successfully.
    """
    folder_path = file_manager.create_folder("testfolder")
    assert folder_path.exists() and folder_path.is_dir()
    shutil.rmtree(folder_path)

def test_move(file_manager):
    """
    Test moving a file from one location to another.
    """
    src = file_manager.create_file("move_me.txt", content="Move this file.")
    dest_dir = file_manager.create_folder("dest_folder")
    dest_path = dest_dir / src.name
    file_manager.move(str(src), str(dest_dir))
    assert dest_path.exists()
    shutil.rmtree(dest_dir)

def test_rename(file_manager):
    """
    Test renaming a file.
    """
    original = file_manager.create_file("oldname.txt", content="Rename me.")
    new_path = file_manager.rename("oldname.txt", "newname.txt")
    assert new_path.exists() and new_path.name == "newname.txt"
    new_path.unlink()

def test_delete_file(file_manager):
    """
    Test that a file can be deleted.
    """
    file_path = file_manager.create_file("delete_me.txt", content="Delete me.")
    file_manager.delete("delete_me.txt")
    assert not file_path.exists()

def test_delete_folder(file_manager):
    """
    Test that a folder can be deleted.
    """
    folder_path = file_manager.create_folder("delete_folder")
    file_manager.delete("delete_folder")
    assert not folder_path.exists()

def test_view_file(file_manager):
    """
    Test reading the contents of a file.
    """
    file_path = file_manager.create_file("view_me.txt", content="Read me.")
    content = file_manager.view("view_me.txt")
    assert content == "Read me."
    file_path.unlink()

def test_view_folder(file_manager):
    """
    Test listing the contents of a folder.
    """
    folder_name = "view_folder"
    folder_path = file_manager.base_dir / folder_name

    if folder_path.exists():
        shutil.rmtree(folder_path)

    file_manager.create_folder(folder_name)
    file_manager.create_file(f"{folder_name}/test.txt", content="hello")

    view_result = file_manager.view(folder_name)

    assert "test.txt" in view_result
    shutil.rmtree(folder_path)

def test_zip_folder(file_manager):
    """
    Test that a folder is zipped and the archive is created.
    """
    folder_path = file_manager.create_folder("zip_me")
    zip_path = file_manager.zip_folder("zip_me")
    assert zip_path.exists() and zip_path.suffix == ".zip"
    zip_path.unlink()
    shutil.rmtree(folder_path)
