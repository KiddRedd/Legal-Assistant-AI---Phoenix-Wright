import requests
import re
from datetime import datetime
import os

def get_date_from_text(text):
    match = re.search(r'Current to (\d{4}-\d{2}-\d{2})', text)
    if match:
        return datetime.fromisoformat(match.group(1))
    else:
        print("Warning: Unable to find 'Current to' date in PDF.")
        return None

def main(urls):
    for url in urls:
        try:
            # Extract filename from URL
            filename = url.split('/')[-1]
            
            # Check if the file exists locally
            if not os.path.exists(filename):
                print(f"File '{filename}' does not exist. Downloading...")
                response = requests.get(url)
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print("Download completed.")
                else:
                    print(f"Failed to download file. Status code: {response.status_code}")
            else:
                # Download the new PDF content
                response = requests.get(url)
                if response.status_code == 200:
                    new_text = response.text
                    new_date = get_date_from_text(new_text)
                    if new_date is not None:
                        # Read local file's content and extract date
                        with open(filename, 'rb') as f:
                            local_content = f.read()
                        local_text = local_content.decode('utf-8', errors='ignore')
                        local_date = get_date_from_text(local_text)
                        
                        if local_date is None or new_date > local_date:
                            print(f"New date '{new_date}' is newer than existing date '{local_date}'. Updating...")
                            with open(filename, 'wb') as f:
                                f.write(response.content)
                            print("Update completed.")
                        else:
                            print(f"New date '{new_date}' is not newer. No update needed.")
                    else:
                        print("Unable to determine new file's update date. Skipping download.")
                else:
                    print(f"Failed to download file. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while processing '{url}': {str(e)}")

if __name__ == "__main__":
    # List of URLs to process
    urls = [
        # Criminal Code
        'https://laws.justice.gc.ca/PDF/C-46.pdf',
        # Youth Criminal Justice Act
        'https://laws-lois.justice.gc.ca/PDF/Y-1.5.pdf',
        # Privacy Act
        'https://laws-lois.justice.gc.ca/PDF/P-21.pdf',
        # Access to information Act
        'https://laws-lois.justice.gc.ca/PDF/A-1.pdf',
        # Copyright Act
        'https://laws-lois.justice.gc.ca/PDF/C-42.pdf',
        # Income Tax Act
        'https://laws-lois.justice.gc.ca/PDF/I-3.3.pdf',
        # Interpretation Act
        'https://laws-lois.justice.gc.ca/PDF/I-21.pdf',
        # Oath of Allegiance Act
        'https://laws.justice.gc.ca/PDF/O-1.pdf',
        # Constitutions Act
        'https://laws.justice.gc.ca/PDF/Const_RPT.pdf'
        # Add more URLs as needed
    ]
    
    main(urls)