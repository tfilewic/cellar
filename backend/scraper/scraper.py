"""
Wine rating scraper.

Extracts rating score from Cellar Tracker
Cellar Tracker's TOS do not prohibit scraping
"""

import requests
from bs4 import BeautifulSoup


def scrape_rating(name: str, vintage: str, producer: str) -> str:
    """
    Fetch rating score from Cellar Tracker for given wine details.

    Args:
        name (str): Wine name.
        vintage (str): Vintage year or 'nv'.
        producer (str): Producer name.

    Returns:
        int or None: Aggregate score (1-100) if found, else None.
    """
    #generate search url from args
    try:
        url = build_url(name, vintage, producer)
    except ValueError:
        return None

    #send HTTP get request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    #parse response and locate first score
    soup = BeautifulSoup(response.text, "html.parser")
    el_scr = soup.find("span", class_="el scr")
    if el_scr:
        score_action = el_scr.find("a", class_="action")
        if score_action:
            score_text = score_action.text.strip().split()[0]
            score = int(float(score_text))
            return score

    return None


def build_url(name: str, vintage: str, producer: str) -> str:
    """
    Construct a Cellar Tracker search URL from wine details.

    Args:
        name (str): The wine's name.  
        vintage (str): The wine's vintage year or designation.  
        producer (str): The wine producer's name.

    Raises:
        ValueError: If any of the arguments are missing or empty.

    Returns:
        str: A Wine-Searcher search URL string for the args.
    """

    if not name or not vintage or not producer:
        raise ValueError("Missing required field")
    
    return f"https://www.cellartracker.com/list.asp?fInStock=0&Table=List&iUserOverride=0&szSearch={vintage.replace(' ', '+')}+{producer.replace(' ', '+')}+{name.replace(' ', '+')}"