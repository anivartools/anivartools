import requests
import sys
import os

def get_file_content(file_path, repo_owner, repo_name):
    """
    Получает содержимое файла из репозитория GitHub.

    Args:
        file_path (str): Путь к файлу в репозитории (например, "docs/knowledge_base.md").
        repo_owner (str): Имя владельца репозитория (ваш логин на GitHub).
        repo_name (str): Название репозитория.


    Returns:
        str: Содержимое файла или сообщение об ошибке.
    """
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        return "Error: GITHUB_TOKEN environment variable not set."

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref=main"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3.raw"  # Получать содержимое файла в "сыром" виде
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки (статус коды 4xx или 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python get_file_content.py <file_path> <repo_owner> <repo_name>")
        sys.exit(1)

    file_path = sys.argv[1]
    repo_owner = sys.argv[2]
    repo_name = sys.argv[3]

    content = get_file_content(file_path, repo_owner, repo_name)
    print(content)