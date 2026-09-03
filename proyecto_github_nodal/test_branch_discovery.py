"""
test_branch_discovery.py
Prueba de extracción de ramas y asignación dinámica de ramas en commits.
"""

import asyncio
import httpx
from bs4 import BeautifulSoup
import re


async def test():
    url = "https://github.com/fastapi/fastapi"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        res = await client.get(f"{url}/branches/all", headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        branch_links = soup.select("a[href*='/tree/'], a[href*='/branches/'], span[class*='branch'], a[class*='branch'], a[href*='/commit/']")
        discovered_branches = set()
        
        for link in branch_links:
            href = link.get("href", "")
            if "/tree/" in href:
                b_name = href.split("/tree/")[-1].split("/")[0]
                if b_name and b_name not in ["all", "active", "stale", "overview"]:
                    discovered_branches.add(b_name)
            text = link.get_text(strip=True)
            if text and not text.startswith("http") and len(text) < 40 and text not in ["Stale", "Active", "Overview", "All", "View all branches"]:
                discovered_branches.add(text)
                
        print(f"Ramas descubiertas en HTML de FastAPI: {discovered_branches}")

if __name__ == "__main__":
    asyncio.run(test())
