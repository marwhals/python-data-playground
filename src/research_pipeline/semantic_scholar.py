import requests

def fetch_paper_by_arxiv_id(arxiv_id):
    """
    Fetch metadata for a paper on Semantic Scholar using its arXiv ID.
    Does NOT require an API key.
    """
    base_url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}"
    fields = "title,authors,year,venue,citationCount,isOpenAccess,url"

    response = requests.get(f"{base_url}?fields={fields}")

    if response.status_code == 200:
        paper = response.json()
        return {
            "title": paper.get("title"),
            "authors": [author["name"] for author in paper.get("authors", [])],
            "year": paper.get("year"),
            "venue": paper.get("venue"),
            "citations": paper.get("citationCount"),
            "is_open_access": paper.get("isOpenAccess"),
            "url": paper.get("url")
        }
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


# Example usage with a well-known arXiv paper
if __name__ == "__main__":
    # 📘 Example: "Attention is All You Need"
    example_arxiv_id = "1706.03762" # TODO pipeline

    paper_info = fetch_paper_by_arxiv_id(example_arxiv_id)

    if paper_info:
        print("\n📄 Paper Metadata:")
        for k, v in paper_info.items():
            print(f"{k.capitalize().replace('_', ' ')}: {v}")
