import os
import asyncio
import aiohttp
import feedparser
import tarfile
from tqdm.asyncio import tqdm

# Constants for folder paths
BASE_DIR = "arXiv_output"
PDF_DIR = os.path.join(BASE_DIR, "downloads")
TAR_DIR = os.path.join(BASE_DIR, "tarballs")
TEX_DIR = os.path.join(BASE_DIR, "tex_sources")

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
                    'id': paper_id,
                    'title': entry.title,
                    'authors': [author.name for author in entry.authors],
                    'summary': entry.summary,
                    'published': entry.published,
                    'link': entry.link,
                    'pdf_link': f"https://arxiv.org/pdf/{paper_id}.pdf",
                    'source_link': f"https://arxiv.org/e-print/{paper_id}"
                }
                papers.append(paper)

            return papers

async def download_file(session, url, filename, folder, desc="Downloading"):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    try:
        async with session.get(url) as response:
            if response.status == 200:
                total_size = int(response.headers.get('Content-Length', 0))
                with open(file_path, 'wb') as f, tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=desc[:30],
                    leave=False
                ) as bar:
                    async for chunk in response.content.iter_chunked(1024):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
                print(f"Downloaded: {file_path}")
            else:
                print(f"Failed to download {url}: {response.status}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return file_path

def extract_tar_gz(file_path, extract_to):
    try:
        os.makedirs(extract_to, exist_ok=True)
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=extract_to)
        print(f"Extracted: {file_path} → {extract_to}")
    except Exception as e:
        print(f"Failed to extract {file_path}: {e}")

async def main():
    papers = await fetch_latest_papers()

    if not papers:
        print("No papers found.")
        return

    async with aiohttp.ClientSession() as session:
        tasks = []
        for paper in papers:
            safe_title = ''.join(c if c.isalnum() or c in (' ', '-') else '_' for c in paper['title'])
            base_filename = safe_title[:100]

            # PDF download task
            pdf_task = asyncio.create_task(
                download_file(session, paper['pdf_link'], f"{base_filename}.pdf", folder=PDF_DIR, desc=base_filename + " [PDF]")
            )

            # TeX source download and extraction task
            async def handle_tex(paper=paper, base_filename=base_filename):
                tar_path = await download_file(
                    session,
                    paper['source_link'],
                    f"{base_filename}.tar.gz",
                    folder=TAR_DIR,
                    desc=base_filename + " [TeX]"
                )
                extract_dir = os.path.join(TEX_DIR, base_filename)
                extract_tar_gz(tar_path, extract_dir)

            tex_task = asyncio.create_task(handle_tex())
            tasks.extend([pdf_task, tex_task])

        await asyncio.gather(*tasks)

    for idx, paper in enumerate(papers, start=1):
        print(f"\nPaper {idx}: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Published: {paper['published']}")
        print(f"Link: {paper['link']}")
        print(f"PDF Link: {paper['pdf_link']}")
        print(f"Source Link: {paper['source_link']}")
        print(f"Summary: {paper['summary'][:500]}...")

if __name__ == "__main__":
    asyncio.run(main())
