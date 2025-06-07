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
        # Charter of Ville de Montréal, metropolis of Québec
        'https://www.legisquebec.gouv.qc.ca/en/pdf/cs/C-11.4.pdf',
        # TAX ADMINISTRATION ACT
        'https://www.legisquebec.gouv.qc.ca/en/pdf/cs/A-6.002.pdf',
        # CHARTER OF HUMAN RIGHTS AND FREEDOMS
        'https://www.legisquebec.gouv.qc.ca/en/pdf/cs/C-12.pdf',
        # HIGHWAY SAFETY CODE
        'https://www.legisquebec.gouv.qc.ca/en/pdf/cs/C-24.2.pdf',
        # LABOUR CODE
        'https://www.legisquebec.gouv.qc.ca/en/pdf/cs/C-27.pdf',
        # Civil Code of Québec
        'https://www.legisquebec.gouv.qc.ca/en/pdf/cs/CCQ-1991.pdf',
        # CONSUMER PROTECTION ACT
        'https://www.legisquebec.gouv.qc.ca/en/pdf/cs/P-40.1.pdf',
        # Add more URLs as needed
    ]
    
    main(urls)