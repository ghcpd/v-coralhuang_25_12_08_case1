import os
import tempfile
import shutil

from src import app as edapp


def test_directories_and_samples_created(tmp_path):
    # Run ensure_directories and create sample modules inside a temp dir
    root = tmp_path / 'workspace'
    os.makedirs(root, exist_ok=True)

    # monkeypatch ROOT_DIR for test
    edapp.ROOT_DIR = str(root)
    edapp.DATA_DIR = os.path.join(edapp.ROOT_DIR, 'data')
    edapp.MODULES_DIR = os.path.join(edapp.ROOT_DIR, 'modules')
    edapp.ACCOUNTS_FILE = os.path.join(edapp.DATA_DIR, 'accounts.json')

    edapp.ensure_directories()
    assert os.path.isdir(edapp.DATA_DIR)
    assert os.path.isdir(edapp.MODULES_DIR)

    # sample modules
    edapp.create_sample_modules()
    for m in edapp.SAMPLE_MODULES:
        assert os.path.exists(os.path.join(edapp.MODULES_DIR, m['file']))


def test_create_and_authenticate_user(tmp_path):
    root = tmp_path / 'workspace2'
    os.makedirs(root, exist_ok=True)

    edapp.ROOT_DIR = str(root)
    edapp.DATA_DIR = os.path.join(edapp.ROOT_DIR, 'data')
    edapp.MODULES_DIR = os.path.join(edapp.ROOT_DIR, 'modules')
    edapp.ACCOUNTS_FILE = os.path.join(edapp.DATA_DIR, 'accounts.json')

    edapp.ensure_directories()

    ok, text = edapp.create_account('tester', 'password123')
    assert ok is True
    assert edapp.authenticate_user('tester', 'password123') is True
    assert edapp.authenticate_user('tester', 'wrong') is False
