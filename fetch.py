import os
import requests
import sys
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from datetime import datetime


# def update_asset_paths(soup, tag, attribute, new_dir):
#     for asset in soup.find_all(tag):
#         src = asset.get(attribute)
#         if src:
#             filename = os.path.basename(urlparse(src).path)
#             new_path = os.path.join(new_dir, filename)
#             asset[attribute] = new_path
#     return soup


# def save_assets(url, content, base_dir):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
#     }
#     soup = BeautifulSoup(content, "html.parser")
#     domain = urlparse(url).netloc
#     assets_dir = f"{base_dir}/assets"
#     os.makedirs(assets_dir, exist_ok=True)

#     # function to download and save assets
#     def download_asset(asset_url, save_dir):
#         if not asset_url:
#             return
#         asset_url = urljoin(url, asset_url)  # Ensure the asset URL is absolute
#         filename = os.path.basename(urlparse(asset_url).path)
#         if not filename:
#             return  # Skip if URL doesn't include a filename
#         save_path = os.path.join(save_dir, filename)
#         try:
#             response = requests.get(asset_url, headers=headers)
#             response.raise_for_status()
#             with open(save_path, "wb") as file:
#                 file.write(response.content)
#             print(f"Saved asset: {asset_url} as {save_path}")
#             return save_path
#         except requests.RequestException as e:
#             print(f"Error fetching asset: {asset_url}: {e}")

#     # Download and update paths for images, CSS, and scripts
#     for tag, attribute, sub_dir in [
#         ("img", "src", "images"),
#         ("link", "href", "css"),
#         ("script", "src", "scripts"),
#     ]:
#         full_sub_dir = os.path.join(assets_dir, sub_dir)
#         os.makedirs(full_sub_dir, exist_ok=True)
#         for asset in soup.find_all(tag):
#             asset_url = asset.get(attribute)
#             if asset_url:
#                 saved_path = download_asset(asset_url, full_sub_dir)
#                 if saved_path:
#                     # Update the HTML to point to the downloaded asset
#                     asset[attribute] = os.path.relpath(saved_path, base_dir)

#     # Return the modified HTML content
#     return str(soup)


def fetch_metadata(url, content):
    soup = BeautifulSoup(content, "html.parser")
    domain = urlparse(url).netloc

    num_links = len(soup.find_all("a"))
    num_images = len(soup.find_all("img"))
    last_fetch = datetime.now().isoformat()

    return {
        "site": domain,
        "num_links": num_links,
        "images": num_images,
        "last_fetch": last_fetch,
    }


def fetch_and_save(urls, print_metadata=False):
    base_dir = "sites"

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            domain = urlparse(url).netloc
            site_dir = os.path.join(base_dir, domain)
            os.makedirs(site_dir, exist_ok=True)
            filename = os.path.join(site_dir, "index.html")

            # modified_html = save_assets(url, response.text, site_dir)

            with open(filename, "w") as file:
                # file.write(modified_html)
                file.write(response.text)

            if print_metadata:
                metadata = fetch_metadata(url, response.text)
                print(
                    f"site: {metadata['site']}\nnum_links: {metadata['num_links']}\nimages: {metadata['images']}\nlast_fetch: {metadata['last_fetch']}"
                )

            print(f"Saved {url} as {filename}")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch.py [--metadata] [URL]...")
    else:
        # Check if --metadata flag is present
        print_metadata_flag = "--metadata" in sys.argv
        # Filter out the --metadata flag from the URL list
        urls = [arg for arg in sys.argv[1:] if arg != "--metadata"]
        fetch_and_save(urls, print_metadata=print_metadata_flag)
