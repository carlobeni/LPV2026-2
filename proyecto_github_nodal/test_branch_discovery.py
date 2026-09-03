"""
test_branch_discovery.py
Prueba de extracción de ramas y asignación dinámica de ramas en commits.
"""

import asyncio
import httpx
from bs4 import BeautifulSoup
import re


async def test():
    url = "https://github.com/carlobeni/LPV2026-2"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        # 1. Intentar descubrir ramas en /branches o /branches/all
        res = await client.get(f"{url}/branches/all", headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        branch_links = soup.select("a[href*='/tree/'], a[class*='branch'], span[class*='branch'], a[href*='/branches']")
        discovered_branches = set()
        
        for link in branch_links:
            text = link.get_text(strip=True)
            if text and not text.startswith("http") and len(text) < 40:
                discovered_branches.add(text)
                
        print(f"Ramas descubiertas en HTML: {discovered_branches}")

if __name__ == "__main__":
    asyncio.run(test())
