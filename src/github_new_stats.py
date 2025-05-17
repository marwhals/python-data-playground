import requests
import matplotlib.pyplot as plt

# Set your GitHub username and token here
USERNAME = "marwhals"
TOKEN = "ghp_fake_token"  # 🔐 Replace this with your actual token

# Add Authorization header
headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}


def get_all_repos(username):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code} - {response.text}")
            break
        page_data = response.json()
        if not isinstance(page_data, list):
            print("Unexpected response format:", page_data)
            break
        if not page_data:
            break
        repos.extend(page_data)
        page += 1
    return repos


def get_language_stats(repos):
    language_totals = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        langs_url = repo.get("languages_url")
        if not langs_url:
            continue
        langs = requests.get(langs_url, headers=headers).json()
        for lang, size in langs.items():
            try:
                size = int(size)
                language_totals[lang] = language_totals.get(lang, 0) + size
            except (ValueError, TypeError):
                print(f"Skipping language {lang} with invalid size: {size}")
    return language_totals


def plot_language_usage(language_totals):
    total = sum(language_totals.values())
    if total == 0:
        print("No language data to plot.")
        return

    languages = list(language_totals.keys())
    sizes = [size / total for size in language_totals.values()]

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=languages, autopct='%1.1f%%', startangle=140)
    plt.title(f"GitHub Language Usage for {USERNAME}")
    plt.axis('equal')

    output_file = "language_stats.png"
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"✅ Language usage chart saved as '{output_file}'")


# --- Run the script ---
repos = get_all_repos(USERNAME)
if repos:
    totals = get_language_stats(repos)
    plot_language_usage(totals)
else:
    print("No repositories found or error occurred.")
