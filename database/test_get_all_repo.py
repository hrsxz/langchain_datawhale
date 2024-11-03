"""
This module
"""

import os
import base64
import requests
import loguru
from dotenv import load_dotenv

# Add
# 加载环境变量
load_dotenv()
# 从环境变量中获取TOKEN
TOKEN = os.getenv("TOKEN")


# 定义获取组织仓库的函数
def get_repos(organization_name, token, outpu_dir):
    """
    default description
    """
    headers = {
        "Authorization": f"token {token}",
    }
    url = f"https://api.github.com/orgs/{organization_name}/repos"
    response = requests.get(
        url, headers=headers, params={"per_page": 200, "page": 0}, timeout=10
    )
    if response.status_code == 200:
        repository = response.json()
        loguru.logger.info(
            f"Fetched {len(repository)} repositories for {organization_name}."
        )
        # 使用 outpu_dir 确定保存仓库名的文件路径
        repositories_path = os.path.join(outpu_dir, "repositories.txt")
        with open(repositories_path, "w", encoding="utf-8") as file:
            for re in repository:
                file.write(re["name"] + "\n")
        return repository
    else:
        loguru.logger.error(f"Error fetching repositories: {response.status_code}")
        loguru.logger.error(response.text)
        return []


# 定义拉取仓库README文件的函数
def fetch_repo_readme(organization_name, repository_name, token, outpu_dir):
    """
    default description
    """
    headers = {
        "Authorization": f"token {token}",
    }
    url = f"https://api.github.com/repos/{organization_name}/{repository_name}/readme"
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        readme_content = response.json()["content"]
        # 解码base64内容
        readme_content = base64.b64decode(readme_content).decode("utf-8")
        # 使用 outpu_dir 确定保存 README 的文件路径
        repo_dir = os.path.join(outpu_dir, repository_name)
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)
        readme_path = os.path.join(repo_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as file:
            file.write(readme_content)
    else:
        loguru.logger.error(
            f"Error fetching README for {repository_name}: {response.status_code}"
        )
        loguru.logger.error(response.text)


# 主函数
if __name__ == "__main__":
    # 配置组织名称
    ORG_NAME = "datawhalechina"
    # 配置 export_dir
    EXPORT_DIR = "database/readme_db"  # 请替换为实际的目录路径
    # 获取仓库列表
    repos = get_repos(ORG_NAME, TOKEN, EXPORT_DIR)
    # 打印仓库名称
    if repos:
        for repo in repos:
            repo_name = repo["name"]
            # 拉取每个仓库的README
            fetch_repo_readme(ORG_NAME, repo_name, TOKEN, EXPORT_DIR)
    # 清理临时文件夹
    # if os.path.exists('temp'):
    #     shutil.rmtree('temp')
