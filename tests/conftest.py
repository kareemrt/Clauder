import pytest
from clauder.models import FileInfo, RepoData


@pytest.fixture
def sample_repo():
    return RepoData(
        owner="test",
        name="sample",
        description="A test repository",
        url="https://github.com/test/sample",
        default_branch="main",
        stars=42,
        language="Python",
        files=[
            FileInfo(
                path="main.py",
                content='import os\nSECRET = "hardcoded-api-key-12345"\ndef run(): pass',
                size=60,
                language="Python",
            ),
            FileInfo(
                path="README.md",
                content="# Sample\nA sample project.",
                size=25,
                language="Markdown",
            ),
        ],
        file_tree=["main.py", "README.md", "requirements.txt"],
        topics=["python", "example"],
    )
