import requests
from bs4 import BeautifulSoup
import pprint

def scrape_karriere():
    # Send a request to the job listing page
    res = requests.get('https://www.karriere.at/jobs/python-junior/wien')
    soup = BeautifulSoup(res.text, 'html.parser')

    # Extract job details
    links = soup.select('.m-jobsListItem__titleLink')
    companies = soup.select('.m-jobsListItem__companyName')

    def create_custom_postings(links):
        # Create empty list
        karriere_links = []
        for idx, item in enumerate(links):
            # Get title
            title = item.getText()
            # Get link
            href = item.get('href', None)
            # Get company name
            company_name = companies[idx].getText().strip() if idx < len(companies) else "Unknown"
            # Create full title
            full_title = f"{title} at {company_name}"
            # Discard senior positions
            if "Senior".lower() not in title.lower():
                karriere_links.append({'title': full_title, 'link': href,})
        # return populated list
        return karriere_links
        
    return create_custom_postings(links)