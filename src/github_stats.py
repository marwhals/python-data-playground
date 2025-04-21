import requests

def get_github_user_stats(username):
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=1"

    user_response = requests.get(user_url)
    repos_response = requests.get(repos_url)

    if user_response.status_code == 200:
        data = user_response.json()
        print(f"User: {data['login']}")
        print(f"Name: {data.get('name')}")
        print(f"Public Repos: {data['public_repos']}")
        print(f"Followers: {data['followers']}")
        print(f"Following: {data['following']}")
        print(f"Created at: {data['created_at']}")
    else:
        print(f"Failed to fetch user: {username}")
        return

    if repos_response.status_code == 200 and repos_response.json():
        repo = repos_response.json()[0]
        repo_name = repo['name']
        print(f"\nLatest Repo: {repo_name}")

        commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=10"
        commits_response = requests.get(commits_url)

        if commits_response.status_code == 200:
            print("\nLast 5 commits:")
            for commit in commits_response.json():
                message = commit['commit']['message']
                date = commit['commit']['committer']['date']
                print(f"- [{date}] {message}")
        else:
            print("Failed to fetch commits.")
    else:
        print("No repositories found.")

# Example usage
get_github_user_stats("marwhals") # stalking myself 😂
