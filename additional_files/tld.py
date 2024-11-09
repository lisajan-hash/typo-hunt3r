import requests
import re


def get_tlds():
    # Make a request to the IANA page
    url = "http://www.iana.org/domains/root/db"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []

    # Use regular expressions to find TLDs in the HTML content
    tld_pattern = r'<a href="/domains/root/db/[^"]+">(\.[a-z]{2,})</a>'
    tlds = re.findall(tld_pattern, response.text)

    # Remove duplicates and sort the list
    tld_list = sorted(set(tlds))

    return tld_list