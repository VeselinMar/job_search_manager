import requests
from bs4 import BeautifulSoup
from datetime import datetime
from ..models import Application
from zoneinfo import ZoneInfo
import re

# store postings in memory
_cache = {
    "postings": [],
    "last_refreshed": None,
}

def normalize(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text

def scrape_karriere():
    res = requests.get("https://www.karriere.at/jobs/python/wien")
    soup = BeautifulSoup(res.text, "html.parser")

    links = soup.select(".m-jobsListItem__titleLink")
    companies = soup.select(".m-jobsListItem__companyName")

    karriere_links = []
    current_applications = {
        (normalize(a.position.lower()), normalize(a.firm.lower())) for a in Application.query.all()
    }

    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get("href", None)
        company_name = (
            companies[idx].getText().strip() if idx < len(companies) else "Unknown"
        )

        norm_title = normalize(title)
        norm_company = normalize(company_name)

        full_title = f"{title} at {company_name}"

        if "senior" not in norm_title and (
            norm_title,
            norm_company,
        ) not in current_applications:
            karriere_links.append({"title": full_title, "link": href})

    # update cache
    _cache["postings"] = karriere_links
    _cache["last_refreshed"] = datetime.now(ZoneInfo("Europe/Vienna"))

    return _cache


def get_cached_postings():
    if not _cache["postings"]:
        return scrape_karriere()
    return _cache
