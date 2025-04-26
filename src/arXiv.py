import os
import asyncio
import aiohttp
import feedparser
from tqdm.asyncio import tqdm

async def fetch_latest_papers(search_query="computational finance", max_results=10):
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=all:{search_query}&sortBy=submittedDate&sortOrder=descending&start=0&max_results={max_results}"

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + query) as response:
            if response.status != 200:
                print(f"Failed to fetch data: {response.status}")
                return []

            text = await response.text()
            feed = feedparser.parse(text)
            papers = []

            for entry in feed.entries:
                paper_id = entry.id.split('/abs/')[-1]
                paper = {
                    'title': entry.title,
                    'authors': [author.name for author in entry.authors],
                    'summary': entry.summary,
                    'published': entry.published,
                    'link': entry.link,
                    'pdf_link': f"https://arxiv.org/pdf/{paper_id}.pdf"
                }
                papers.append(paper)

            return papers

async def download_paper(session, pdf_url, filename, folder="downloads"):
    os.makedirs(folder, exist_ok=True)
    try:
        async with session.get(pdf_url) as response:
            if response.status == 200:
                total_size = int(response.headers.get('Content-Length', 0))
                file_path = os.path.join(folder, filename)

                with open(file_path, 'wb') as f, tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=filename[:30],
                    leave=False
                ) as bar:
                    async for chunk in response.content.iter_chunked(1024):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
                print(f"Downloaded: {file_path}")
            else:
                print(f"Failed to download {pdf_url}: {response.status}")
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")

async def main():
    papers = await fetch_latest_papers()

    if not papers:
        print("No papers found.")
        return

    async with aiohttp.ClientSession() as session:
        tasks = []
        for paper in papers:
            safe_title = ''.join(c if c.isalnum() or c in (' ', '-') else '_' for c in paper['title'])
            filename = f"{safe_title[:100]}.pdf"  # limit filename length
            task = asyncio.create_task(download_paper(session, paper['pdf_link'], filename))
            tasks.append(task)
        await asyncio.gather(*tasks)

    for idx, paper in enumerate(papers, start=1):
        print(f"\nPaper {idx}: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Published: {paper['published']}")
        print(f"Link: {paper['link']}")
        print(f"PDF Link: {paper['pdf_link']}")
        print(f"Summary: {paper['summary'][:500]}...")

if __name__ == "__main__":
    asyncio.run(main())
