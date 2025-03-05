# Part of Dream Auto Daily
Part of Dream - DreamerQuest auto daily check-in and spin
## Tools and components required
1. [Part of Dream](https://dreamerquests.partofdream.io/login?referralCodeForPOD=2e6835e8) Account, Register here: [https://dreamerquests.partofdream.io](https://dreamerquests.partofdream.io/login?referralCodeForPOD=2e6835e8)
2. Don't forget to connect socials and complete tasks!
3. Account UserID and Cookies
4. Python3 Latest
5. VPS or RDP (OPTIONAL), Get free $200 credit [DigitalOcean](https://m.do.co/c/3f132e0f7e13) for 60 days here: [Register](https://m.do.co/c/3f132e0f7e13)
## Installation
- Install Python For Windows: [Python](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)
- For Unix:
```bash
apt install python3 python3-pip git -y
```
- For Termux:
```bash
pkg install python python-pip git -y
```
- Download script [Manually](https://github.com/im-hanzou/partofdream-autodaily/archive/refs/heads/main.zip) or use git:
```bash
git clone https://github.com/im-hanzou/partofdream-autodaily
```
### How to get account id and cookies
- First, login into your [Part of Dream](https://dreamerquests.partofdream.io/login?referralCodeForPOD=2e6835e8) Account
- Open your Browser console `CTRL + SHIFT  + I` or `F12`
- Go to `Network` tab and refresh
- Search for `https://server.partofdream.io/user/session`
- Find your user id, select one and go to `Response`. Copy your `user id`
![image](https://github.com/user-attachments/assets/09ab31fd-a7cb-421f-96a4-935c9c2a0293)
- Find your cookie, select one and copy `cookies` from `Request Headers`
![image](https://github.com/user-attachments/assets/a5bec071-dc60-43e6-bcc7-30f7a53013c7)
### Requirements installation
- Make sure you already in bot folder:
```bash
cd partofdream-autodaily
```
#### Windows and Termux:
```bash
pip install -r requirements.txt
```
#### Unix:
```bash
pip3 install -r requirements.txt
```
## Run the Bot
- Windows and Termux:
```bash
python main.py
```
- Unix:
```bash
python3 main.py
```
- Then insert your `user id` and `cookies`
# Notes
- Run this bot, use my referral code if you don't have one.
- You can just run this bot at your own risk, I'm not responsible for any loss or damage caused by this bot.
- This bot is for educational purposes only.
