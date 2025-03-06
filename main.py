import requests
import time
import json
from datetime import datetime, timedelta
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def print_banner():
    banner = f"""{Fore.YELLOW}
╔═══════════════════════════════════════════════╗
║   partofdream.io - DreamerQuest Auto Daily    ║
║     Github: https://github.com/kelliark       ║
╚═══════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

class GameAutomation:
    def __init__(self, user_config, proxies_list=None):
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'priority': 'u=1, i',
            'referer': 'https://dreamerquests.partofdream.io/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        self.cookies = {}
        if "cookies" in user_config:
            for cookie in user_config["cookies"].split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    self.cookies[name.strip()] = value.strip()
        self.payload = {
            "userId": user_config.get('userId', ''),
            "timezoneOffset": -420
        }
        self.displayName = user_config.get("userId", "Unknown")
        self.proxy_str = user_config.get("proxy", None)
        self.proxy = self.init_proxy(self.proxy_str)
        self.proxies_list = proxies_list if proxies_list and len(proxies_list) > 0 else None

    def init_proxy(self, proxy):
        if proxy:
            return {"http": proxy, "https": proxy}
        return None

    def perform_request(self, url, payload=None):
        try:
            if payload is None:
                payload = self.payload
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                cookies=self.cookies,
                proxies=self.proxy
            )
            return response
        except Exception as e:
            print(f"{Fore.RED}Error during request to {url}: {str(e)}{Style.RESET_ALL}")
            return None

    def perform_checkin(self):
        url = 'https://server.partofdream.io/checkin/checkin'
        response = self.perform_request(url)
        next_run = datetime.now() + timedelta(hours=1)
        if response:
            try:
                data = response.json()
                msg = data.get("message", "").lower()
                if "already" in msg:
                    print(f"{Fore.GREEN}Daily Check in is already done! Next check in at {next_run.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}Daily Check in successfully! Next check in at {next_run.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                return True
            except Exception:
                print(f"{Fore.GREEN}Daily Check in completed. Next check in at {next_run.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                return True
        else:
            print(f"{Fore.RED}Daily Check in encountered an error.{Style.RESET_ALL}")
            return False

    def perform_spin(self):
        url = 'https://server.partofdream.io/spin/spin'
        response = self.perform_request(url)
        next_run = datetime.now() + timedelta(hours=1)
        if response is None:
            print(f"{Fore.CYAN}Daily Spin encountered an error.{Style.RESET_ALL}")
            return False
        try:
            data = response.json()
        except Exception as e:
            print(f"{Fore.CYAN}Daily Spin encountered an error parsing JSON: {str(e)}{Style.RESET_ALL}")
            return False
        msg = data.get("message", "").lower()
        if "already" in msg:
            print(f"{Fore.CYAN}Daily Spin is already done! Next spin at {next_run.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            return True
        elif response.status_code != 200:
            print(f"{Fore.CYAN}Daily Spin encountered an error (Status Code {response.status_code}).{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.CYAN}Daily Spin successfully! Next spin at {next_run.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            return True

    def get_account_info(self):
        try:
            response = requests.post(
                "https://server.partofdream.io/user/session",
                headers=self.headers,
                cookies=self.cookies,
                proxies=self.proxy,
                json={}
            )
            if response.status_code != 200 or not response.text.strip():
                return self.displayName, "Unknown"
            data = response.json()
            if "user" in data:
                self.displayName = data["user"].get("displayName", self.displayName)
                points = data["user"].get("points", "Unknown")
                return self.displayName, points
            else:
                return self.displayName, "Unknown"
        except Exception:
            return self.displayName, "Unknown"

    def get_proxy_ip(self):
        try:
            response = requests.get("http://ip-api.com/json", proxies=self.proxy, timeout=10)
            if response.status_code != 200 or not response.text.strip():
                return "Unknown"
            data = response.json()
            return data.get("query", "Unknown")
        except Exception:
            return "Unknown"

    def update_status(self):
        displayName, points = self.get_account_info()
        ip_used = self.get_proxy_ip()
        print(f"{Fore.GREEN}Account: {Fore.RESET}{displayName}")
        print(f"{Fore.CYAN}Points: {Fore.RESET}{points}")
        print(f"{Fore.YELLOW}Ip used: {Fore.RESET}{ip_used}\n")

    def run_tasks(self):
        max_attempts = 3
        attempts = 0
        while attempts < max_attempts:
            self.update_status()
            success_checkin = self.perform_checkin()
            success_spin = self.perform_spin()
            if success_checkin and success_spin:
                break  # both tasks succeeded
            else:
                attempts += 1
                if self.proxies_list:
                    try:
                        current_index = self.proxies_list.index(self.proxy_str)
                    except ValueError:
                        current_index = 0
                    new_index = (current_index + 1) % len(self.proxies_list)
                    new_proxy = self.proxies_list[new_index]
                    print(f"{Fore.RED}Switching proxy for account {self.displayName} to {new_proxy}{Style.RESET_ALL}")
                    self.proxy_str = new_proxy
                    self.proxy = self.init_proxy(new_proxy)
                print(f"{Fore.RED}Error encountered. Retrying quest for account {self.displayName} (Attempt {attempts}/{max_attempts})...{Style.RESET_ALL}")
                time.sleep(30)

def read_accounts():
    """
    Reads accounts from accounts.txt.
    Expected format per line:
      userid:cookie
    Example:
      123456:name1=value1; name2=value2
    """
    accounts = []
    try:
        with open("accounts.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ':' in line:
                    user_id, cookies = line.split(":", 1)
                    accounts.append({
                        "userId": user_id.strip(),
                        "cookies": cookies.strip()
                    })
    except Exception as e:
        print(f"{Fore.RED}Error reading accounts.txt: {str(e)}{Style.RESET_ALL}")
    return accounts

def read_proxies():
    proxies = []
    try:
        with open("proxies.txt", "r") as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    except Exception as e:
        print(f"{Fore.RED}Error reading proxies.txt: {str(e)}{Style.RESET_ALL}")
    return proxies

def main():
    print_banner()
    accounts = read_accounts()
    proxies = read_proxies()
    
    if not accounts:
        print(f"{Fore.RED}No accounts found in accounts.txt{Style.RESET_ALL}")
        return

    if not proxies:
        print(f"{Fore.RED}No proxies found in proxies.txt... proceeding without any proxy.{Style.RESET_ALL}")
        proxies = None

    game_instances = []
    for i, account in enumerate(accounts):
        if proxies:
            if i < len(proxies):
                account["proxy"] = proxies[i]
            else:
                account["proxy"] = proxies[i % len(proxies)]
        else:
            account["proxy"] = None
        game = GameAutomation(account, proxies_list=proxies)
        game_instances.append(game)

    while True:
        for game in game_instances:
            game.run_tasks()
            print("====================\n")
        print("All accounts finished, waiting 1 hour to do the task again!..\n")
        time.sleep(3600)  # Wait 1 hour

if __name__ == "__main__":
    main()
