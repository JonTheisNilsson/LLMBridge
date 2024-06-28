import re
import tempfile
import os
from git import Repo
from urllib.parse import urlparse

class GitHubUtils:
    @staticmethod
    def is_github_url(url):
        github_pattern = r'^https?://github\.com/[\w-]+/[\w.-]+/?$'
        return re.match(github_pattern, url) is not None

    @staticmethod
    def clone_repository(url):
        if not GitHubUtils.is_github_url(url):
            raise ValueError("Invalid GitHub URL")

        repo_name = os.path.basename(urlparse(url).path)
        temp_dir = tempfile.mkdtemp(prefix=f"llmbridge_{repo_name}_")
        
        try:
            Repo.clone_from(url, temp_dir)
            return temp_dir
        except Exception as e:
            raise Exception(f"Failed to clone repository: {str(e)}")