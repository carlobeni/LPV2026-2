"""
test_scrape_live.py
Script de prueba para verificar el funcionamiento del motor de Web Scraping
sobre un repositorio real de GitHub (https://github.com/fastapi/fastapi).
"""

import asyncio
from scraper import GitHubWebScraper


async def main():
    print("=== INICIANDO PRUEBA DE WEB SCRAPING EN VIVO ===")
    repo_target = "https://github.com/fastapi/fastapi"
    scraper = GitHubWebScraper()
    
    owner, repo_name = scraper.extract_repo_owner_name(repo_target)
    full_repo = f"{owner}/{repo_name}"
    print(f"Target Repo: {full_repo}")
    
    html = await scraper.fetch_commits_html(repo_target)
    commits = scraper.parse_commits_html(html, full_repo, limit=5)
    
    print(f"\nCommits Extraídos y Validados con Pydantic v2: {len(commits)}\n")
    for i, c in enumerate(commits, 1):
        padre_str = c.parent_hash[:7] if c.parent_hash else "Nodo Raíz"
        print(f"{i}. Hash: [{c.short_hash}] | Autor: @{c.author_username}")
        print(f"   Mensaje: {c.message[:60]}")
        print(f"   Padre Nodal: {padre_str} | Lineas: +{c.additions} / -{c.deletions}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
