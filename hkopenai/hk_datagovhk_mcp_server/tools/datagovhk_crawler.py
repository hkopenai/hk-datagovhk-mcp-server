import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

def crawl_datasets(category: str, page: int = 1) -> Dict[str, Any]:
    """
    Crawl datasets from data.gov.hk based on category and page number.

    Args:
        category: The category of datasets to crawl (e.g., 'finance', 'education').
        page: The page number to crawl (default: 1).

    Returns:
        Dict containing a list of datasets with their titles and links.
    """
    base_url = "https://data.gov.hk/en-datasets"
    params = {
        "page": page,
        "category": category
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        datasets = []
        # Find all dataset entries. Adjust selector based on actual website structure.
        # This is a placeholder and might need to be updated based on the actual HTML.
        for item in soup.select(".dataset-item"): # Assuming a class 'dataset-item' for each entry
            title_tag = item.select_one(".dataset-title a") # Assuming title is in an <a> tag within .dataset-title
            link_tag = item.select_one(".dataset-link") # Assuming link is in a tag with class 'dataset-link'

            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = link_tag['href'] if 'href' in link_tag.attrs else ''
                datasets.append({"title": title, "link": link})
            elif title_tag: # If only title is found, still add it
                title = title_tag.get_text(strip=True)
                datasets.append({"title": title, "link": ""})

        return {"category": category, "page": page, "datasets": datasets}

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data from data.gov.hk: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
