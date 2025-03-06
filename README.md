# Partofdream AutoDaily

A Python automation script to perform daily check-in and spin tasks on **Dreamer Quests** for multiple accounts. The script supports assigning individual proxies per account and automatically retries tasks (with proxy switching) if an error occurs.

## Register
 - [Dreamer Quests](https://dreamerquests.partofdream.io/login?referralCodeForPOD=65da3b06)
 - Use my code: 65da3b06

## Features

- **Multi-Account Support:** Use a single script to automate tasks for multiple accounts.
- **Proxy Support:** Assign a unique proxy per account via a `proxies.txt` file.
- **Automatic Retrying:** If a task fails, the script retries up to three times and switches proxies if available.
- **Status Reporting:** Displays account details (display name, points, IP used) and task outcomes with friendly messages.
- **Scheduled Execution:** Repeats the entire process every hour until stopped.

## Prerequisites
- **Python Latest**  
- Required Python packages:
  - `requests`
  - `colorama`
  - `schedule`

## Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/kelliark/DreamerQuests-AutoBot
   cd DreamerQuests-AutoBot
   ```
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Accounts:**
   Open `accounts.txt` file in the project directory. Each line should follow this format:
   ```
   userid:cookie
   ```
3. **Configure Proxies (Optional):**
   Open `proxies.txt` file in the project directory. Each line should be a proxy in the following format:
   ```
   protocol://username:password@ip:port
   ```
   *Note:* If you do not supply a `proxies.txt` file or if it's empty, the script will run without any proxies.

## Usage

Run the script with:

```bash
python main.py
```

The script will:
- Display a banner and account status (display name, points, and current IP used).
- Perform daily check-in and spin tasks for each account.
- Print friendly messages indicating whether the tasks were successful or already completed, along with a countdown for the next attempt.
- Retry tasks up to three times in case of errors (switching proxies if available).
- Wait one hour before repeating the process.

## Troubleshooting
- **Proxy Errors:**  
  If a proxy error occurs, the script will automatically switch to a different proxy from your `proxies.txt` file (if available) and retry the task.
- **Task Failures:**  
  If tasks continue to fail, ensure that your account cookies are up-to-date and that your proxies (if used) are working properly.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request with improvements or bug fixes.

## License
This project is licensed under the MIT License. 


## Notes
Use at your own risk, all risk are borne with the user.
