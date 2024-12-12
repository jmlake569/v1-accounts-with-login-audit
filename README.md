
# Vision One IAM Accounts and Audit Logs Retrieval Scripts

This repository contains a Python script designed to retrieve **IAM accounts** and their corresponding **audit logs** from Trend Micro Vision One.

---

## Description  
The script combines IAM account information with their associated audit logs. Each user account includes actions performed on their behalf, fetched from the Audit Logs API. The script outputs data in JSON or CSV format, depending on user preference.

---

## Usage  

### 1. Prerequisites  
- **Python**: Ensure Python 3.x is installed.
- **Bearer Token**: Obtain a valid API token with permissions to access the IAM Accounts and Audit Logs APIs from Trend Micro Vision One.

### 2. Installation  
- Clone this repository to your local environment:  
  ```bash
  git clone <repository-url>
  cd <repository-folder>
  ```
- Install required dependencies:  
  ```bash
  pip install requests
  ```

### 3. Running the Script  
- Syntax:  
  ```bash
  python script.py -t <YOUR_BEARER_TOKEN> [-j | -c]
  ```
- **Arguments**:  
  - `-t`, `--token`: Bearer token for API authentication (**required**).
  - `-j`, `--json`: Save the output as JSON (optional).
  - `-c`, `--csv`: Save the output as CSV (optional).

- **Example Command**:  
  ```bash
  python script.py -t abc123456789 --json
  ```

### 4. Output  
The script saves results in the **current directory**:  
- `accounts_with_audit_logs.json` (if `--json` is used).  
- `accounts_with_audit_logs.csv` (if `--csv` is used).  

---

## Dependencies  
The script requires the following:  
- **Python 3.x**  
- **requests library**: Install using:  
  ```bash
  pip install requests
  ```

---

## Features  
- **IAM Account Retrieval**: Fetches all IAM accounts using the Vision One IAM API.  
- **Audit Logs Integration**: Retrieves audit logs specific to each IAM user.  
- **Output Options**: Allows saving data as JSON or CSV for analysis.

---

## Example Output  
**JSON Format**:  
```json
[
  {
    "email": "user@example.com",
    "id": "12345",
    "audit_logs": [
      {
        "eventTime": "2024-06-10T12:00:00Z",
        "action": "LOGIN",
        "description": "User logged into the console"
      }
    ]
  }
]
```

---

## License  
This script is open-source and can be freely modified and shared under the appropriate license.
