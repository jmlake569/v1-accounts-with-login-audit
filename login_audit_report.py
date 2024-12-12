import argparse
import requests
import json
import csv
import os

# Setup argument parser
parser = argparse.ArgumentParser(description='Get IAM accounts and audit logs from Trend Micro API')
parser.add_argument('-t', '--token', required=True, help='Bearer token for authentication')
parser.add_argument('-j', '--json', action='store_true', help='Save output as JSON')
parser.add_argument('-c', '--csv', action='store_true', help='Save output as CSV')

# Parse arguments
args = parser.parse_args()

# Ensure that either -j or -c is provided
if not args.json and not args.csv:
    parser.error('You must specify either -j (JSON) or -c (CSV)')

# Color definitions using ANSI escape codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Base URLs
url_base = 'https://api.xdr.trendmicro.com'
iam_url_path = '/v3.0/iam/accounts'
audit_logs_url_path = '/v3.0/audit/logs'

# Headers for API requests
headers = {
    'Authorization': 'Bearer ' + args.token,
    'Content-Type': 'application/json'
}

# Function to retrieve IAM accounts
def get_iam_accounts():
    accounts = []
    next_url = f"{url_base}{iam_url_path}?top=50"

    while next_url:
        response = requests.get(next_url, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            accounts.extend(response_json.get('items', []))
            next_url = response_json.get('nextLink') or response_json.get('@odata.nextLink')
        else:
            print(f"Error fetching IAM accounts: {response.status_code} - {response.text}")
            exit(1)

    print(f"{YELLOW}Total IAM accounts retrieved: {len(accounts)}{RESET}")
    return accounts

# Function to retrieve audit logs for a user
def get_audit_logs(user_email):
    params = {
        'limit': 50,  # Adjust as needed
        'filter': f"user eq '{user_email}'"
    }
    audit_logs = []
    response = requests.get(f"{url_base}{audit_logs_url_path}", headers=headers, params=params)
    if response.status_code == 200:
        audit_logs = response.json().get('items', [])
    else:
        print(f"{YELLOW}No audit logs found for {user_email}. Error: {response.status_code}{RESET}")
    return audit_logs

# Main logic
print(f"{GREEN}Fetching IAM accounts...{RESET}")
iam_accounts = get_iam_accounts()

# Append audit logs to each account
print(f"{GREEN}Fetching audit logs for each account...{RESET}")
for account in iam_accounts:
    user_email = account.get('email')  # Adjust key if needed
    if user_email:
        audit_logs = get_audit_logs(user_email)
        account['audit_logs'] = audit_logs

# Save to JSON or CSV
output_file = ''
if args.json:
    output_file = os.path.join(os.getcwd(), 'accounts_with_audit_logs.json')
    with open(output_file, 'w') as f:
        json.dump(iam_accounts, f, indent=4)
elif args.csv:
    output_file = os.path.join(os.getcwd(), 'accounts_with_audit_logs.csv')
    with open(output_file, 'w', newline='') as f:
        fieldnames = list(iam_accounts[0].keys()) if iam_accounts else []
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for account in iam_accounts:
            writer.writerow(account)

print(f"{GREEN}Output saved to: {os.path.abspath(output_file)}{RESET}")
