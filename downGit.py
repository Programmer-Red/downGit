import os
import sys
import requests
from urllib.parse import urlparse

class DownGit:
    def __init__(self, repo_url):
        self.repo_url = repo_url.strip().rstrip("/")
        self.repo_owner, self.repo_name, self.paths= self._parse_repo_url()
        self.paths='/'.join(self.paths)
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{self.paths}"
        self.session = requests.Session()
        GITHUB_TOKEN = "填自己的"

        self.session.headers.update({
            "User-Agent": "DownGit-Script",
            "Authorization": f"token {GITHUB_TOKEN}"
        })

    def _parse_repo_url(self):
        try:
            path_parts = urlparse(self.repo_url).path.strip("/").split("/")
            real_path=path_parts[4:]
            if len(path_parts) < 2:
                raise ValueError("URL 格式错误，应该是 https://github.com/[owner]/[repo]")
            return path_parts[0], path_parts[1],real_path
        except Exception as e:
            print(f"[错误] URL 解析失败: {e}")
            sys.exit(1)

    def list_files(self, path=""):
        files = []
        print(path)
        url = f"{self.api_url}/{path}" if path else self.api_url
        try:
            resp = self.session.get(url)
            if resp.status_code != 200:
                raise Exception(f"HTTP {resp.status_code}: {resp.text}")
            data = resp.json()
            for item in data:
                if item["type"] == "file":
                    files.append(item["path"])
                elif item["type"] == "dir":
                    files.extend(self.list_files(item["path"]))
            return files
        except Exception as e:
            print(f"[错误] 遍历失败: {e}")
            sys.exit(1)

    def download_file(self, file_path, save_dir):
        raw_url = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/master/{file_path}"
        save_path = os.path.join(save_dir, file_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            r = self.session.get(raw_url)
            if r.status_code != 200:
                print(f"[警告] 下载失败: {file_path} (HTTP {r.status_code})")
                return
            with open(save_path, "wb") as f:
                f.write(r.content)
            print(f"[下载完成] {file_path}")
        except Exception as e:
            print(f"[错误] 下载 {file_path} 失败: {e}")

    def run(self):
        print(f"[信息] 正在遍历 {self.repo_url} ...")
        files = self.list_files()
        print(f"[信息] 共找到 {len(files)} 个文件")
        base_dir = self.repo_name
        os.makedirs(base_dir, exist_ok=True)
        sub_dir_name = input("请输入下载内容要保存的文件夹名或相对路径(如a/b/c,则会生成3层目录): ").strip()
        save_dir = os.path.join(base_dir, sub_dir_name)
        os.makedirs(save_dir, exist_ok=True)
        for file_path in files:
            self.download_file(file_path, save_dir)

        print("ok")


if __name__ == "__main__":
    repo_url = input("请输入 GitHub 仓库完整链接: ").strip()
    down_git = DownGit(repo_url)
    down_git.run()
