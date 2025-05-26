import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

def download_files_from_directory(url, download_path, download_limit=10):
    # Create the download path directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # Get the page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve URL: {url}")
        return

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')

    downloads_done = 0

    for i, link in enumerate(links):
        href = link.get('href')
        if href and not href.startswith('?') and not href.startswith('/') and not href.startswith('../'):
            file_url = urljoin(url, href)
            decoded_filename = unquote(href)  # Convert %20 etc. to normal characters
            file_path = os.path.join(download_path, decoded_filename)

            # Check if decoded file already exists
            if os.path.exists(file_path):
                print(f"File already exists, skipping: {file_path}")
                continue
            
            # Download the file
            print(f"Downloading {file_url}...")
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(file_response.content)
                print(f"Downloaded {file_path}")
                downloads_done += 1
            else:
                print(f"Failed to download {file_url}")

            # Stop if we've downloaded enough files
            if downloads_done >= download_limit:
                print(f"Download limit of {download_limit} reached.")
                break

if __name__ == "__main__":
    directory_url = "https://the-eye.eu/public/Radio/Coast%20to%20Coast%20AM/The%20Ultimate%20Art%20Bell%20Collection/Shows/"
    download_directory = "/home/nmb/Music"
    
    download_files_from_directory(
        directory_url,
        download_directory,
        download_limit=10
    )

