import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_files_from_directory(url, download_path):
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
    
    for link in links:
        href = link.get('href')
        if href and not href.startswith('?') and not href.startswith('/') and not href.startswith('../'):
            file_url = urljoin(url, href)
            file_name = os.path.join(download_path, href)
            
            # Download the file
            print(f"Downloading {file_url}...")
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                with open(file_name, 'wb') as file:
                    file.write(file_response.content)
                print(f"Downloaded {file_name}")
            else:
                print(f"Failed to download {file_url}")

if __name__ == "__main__":
    # URL of the directory containing the files
    directory_url = "https://the-eye.eu/public/Radio/Coast%20to%20Coast%20AM/The%20Ultimate%20Art%20Bell%20Collection/Shows/"
    # Path to the directory where files will be downloaded
    download_directory = "/home/nmb/Music"
    
    download_files_from_directory(directory_url, download_directory)

