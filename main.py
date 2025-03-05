import requests
import schedule
import time
from datetime import datetime, timedelta
import colorama
from colorama import Fore, Back, Style
import traceback

colorama.init(autoreset=True)

def print_banner():
    banner = f"""{Fore.MAGENTA}
╔═══════════════════════════════════════════════╗
║   partofdream.io - DreamerQuest Auto Daily    ║
║     Github: https://github.com/im-hanzou      ║
╚═══════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

class GameAutomation:
    def __init__(self, user_config):
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://dreamerquests.partofdream.io',
            'priority': 'u=1, i',
            'referer': 'https://dreamerquests.partofdream.io/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
        }
        
        self.cookies = user_config.get('cookies', {})
        self.payload = {
            "userId": user_config.get('userId', ''),
            "timezoneOffset": -420
        }

    def log(self, message, color=Fore.WHITE):
        timestamp = f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}"
        print(f"{timestamp} {color}[LOG]{Style.RESET_ALL} {message}")

    def perform_request(self, url, action_name):
        try:
            self.log(f"Initiating {action_name} request...", Fore.CYAN)
            
            response = requests.post(
                url, 
                json=self.payload, 
                headers=self.headers, 
                cookies=self.cookies,
            )
            
            self.log(f"{action_name.capitalize()} Attempt Details:", Fore.GREEN)
            self.log(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Fore.GREEN)
            self.log(f"Status Code: {response.status_code}", 
                Fore.GREEN if response.status_code == 200 else Fore.RED
            )
            
            try:
                response_json = response.json()
                self.log(f"Response Content: {response_json}", Fore.MAGENTA)
            except ValueError:
                self.log(f"Response Content: {response.text}", Fore.YELLOW)
            
            next_run = datetime.now() + timedelta(hours=12)
            self.log(f"Done, next {action_name} will be in 12 hours at {next_run.strftime('%Y-%m-%d %H:%M:%S')}", Fore.GREEN)
            
            return response.status_code == 200
        
        except Exception as e:
            self.log(f"Error during {action_name}:", Fore.RED)
            self.log(f"{traceback.format_exc()}", Fore.RED)
            return False

    def perform_checkin(self):
        return self.perform_request(
            'https://server.partofdream.io/checkin/checkin', 
            'check-in'
        )

    def perform_spin(self):
        return self.perform_request(
            'https://server.partofdream.io/spin/spin', 
            'spin'
        )

def get_user_config():
    print_banner()
    
    user_id = input(f"{Fore.YELLOW}Enter your User ID: {Style.RESET_ALL}")
    print(f"{Fore.GREEN}Enter cookies (Format: name1=value1; name2=value2):{Style.RESET_ALL}")
    cookies_input = input(f"{Fore.YELLOW}Cookies: {Style.RESET_ALL}")
    print()
    cookies = {}
    if cookies_input.strip():
        for cookie in cookies_input.split(';'):
            if '=' in cookie:
                name, value = cookie.strip().split('=', 1)
                cookies[name.strip()] = value.strip()
    
    return {
        'userId': user_id,
        'cookies': cookies
    }
    
def main():
    user_config = get_user_config()

    game_auto = GameAutomation(user_config)
    
    schedule.every(12).hours.do(game_auto.perform_checkin)
    schedule.every(12).hours.do(game_auto.perform_spin)
    
    game_auto.perform_checkin()
    game_auto.perform_spin()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Script terminated by user.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
