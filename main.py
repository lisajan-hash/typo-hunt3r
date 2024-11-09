import logging
from additional_files.tld import get_tlds
from additional_files.permutatition import SimpleFuzzer
import dns.resolver
import requests

# Set up logging
logging.basicConfig(filename='logs.txt')

#add your domain name with tld ex. ["youirdomain.com"] or ["yourdomain.com", "otherdomain.com"]
domain_array_name_with_tld = ['yourdomain.com']


def remove_tld(domain):
    parts = domain.split('.')
    if len(parts) > 1:
        return '.'.join(parts[:-1])
    return domain


def query_dns(domain, record_type):
    try:
        records = dns.resolver.resolve(domain, record_type)
        return [str(record) for record in records]
    except dns.resolver.NoAnswer:
        logging.warning(f"No answer for {domain} with record type {record_type}.")
        return []
    except dns.resolver.NXDOMAIN:
        logging.warning(f"{domain} does not exist.")
        return []
    except Exception as e:
        logging.error(f"Error querying {domain} for {record_type}: {e}")
        return []

def check_domain(domain):
    result = {
        "exists": False,
        "mx_records": query_dns(domain, 'MX'),
        "ns_records": query_dns(domain, 'NS')
    }
    
    result["exists"] = len(query_dns(domain, 'A')) > 0
    return result


def start_checking():
    tlds = get_tlds()
    whois_url_list = []
    
    if len(tlds) == 0:
        logging.warning("Failed to retrieve TLDs, TLD list is empty, please check the tld.py file, exiting...")
        return whois_url_list  # Return early if no TLDs

    for domain in domain_array_name_with_tld:
        data = {"domain": domain, "permutations": [], "dns_info": {}}
        sanitized_domain = remove_tld(domain)
        permuted_domains = SimpleFuzzer(sanitized_domain).generate_permutations()

        for tld in tlds:
            for permuted_domain in permuted_domains:
                full_domain = permuted_domain + tld
                try:
                    success_request = requests.get(f"http://{full_domain}")
                    print(success_request.status_code)
                    if success_request.status_code == 200 or success_request.status_code == 301 or success_request.status_code == 302 or success_request.status_code == 404 or success_request.status_code == 404:
                        print(f"Domain {full_domain} exists")
                        dns_info = check_domain(full_domain)
                        if dns_info["exists"]:
                            data["permutations"].append(full_domain)
                            data["dns_info"][full_domain] = dns_info
                except Exception as e:
                    logging.error(f"Error checking domain {full_domain}: {e}")
        whois_url_list.append(data)
    
    # Write results to a text file
    with open('whois_results.txt', 'w') as f:
        for entry in whois_url_list:
            f.write(f"Domain: {entry['domain']}\n")
            f.write("Permutations:\n")
            for perm in entry['permutations']:
                f.write(f"  {perm}\n")
            f.write("DNS Info:\n")
            for domain, info in entry['dns_info'].items():
                f.write(f"  {domain}: {info}\n")
            f.write("\n")  # Add a newline between entries

    return whois_url_list

start_checking()