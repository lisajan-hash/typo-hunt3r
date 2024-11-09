# SQUATHUNTER

## Overview
SQUATHUNTER is a script designed to generate domain names using a permutation function. The script then checks the availability of these domains across various top-level domains (TLDs), performing additional checks for MX and NS records. Results are written to a `whois_result.txt` file.

## Performance
Please note that the script can take a significant amount of time to run. For instance, generating domains of length 11 can take about 18 hours to gather all the necessary information.

## Packagess

## Installation

To install SQUATHUNTER, follow these steps:

1. **Create a Virtual Environment and activate it**:
   ```bash
   python -m venv venv
   vevv/scripti/activate [ Widnows ] or source venv/lib/activate [ Unix/ Linux ]
2. **Install packages**:
    ```bash
   pip install -r requirements.txt

## Usage
Find "domain_array_name_with_tld" in main.py and add your domain example ex. ["youirdomain.com"] or ["yourdomain.com", "otherdomain.com"] . Save and run main.py

## Goal of the script
Sometimes attackers can mimic your domain, which can facilitate attacks against you. If an MX record exists for the mimicked domain, it likely means they can send emails from that domain name.