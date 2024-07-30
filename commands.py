from psnawp_api import PSNAWP
from dotenv import load_dotenv
import os

load_dotenv()
NPSSO = os.getenv('NPSSO')
psnawp = PSNAWP(npsso_cookie=NPSSO)

def help(filtered_user_input: str) -> str:
    payload = "^help: List of commands\n"
    payload += "^lookup [online_id]: Lookup a PSN user\n"
    return payload 

def lookup(filtered_user_input: str) -> str:
    try:
        user = psnawp.user(online_id=filtered_user_input)
        payload = f"Online ID: {user.online_id}\n"
        payload += f"Account ID: {user.account_id}\n"
        return payload
    except Exception as e:
        return "User not found. Please try again."

def get_response(user_input: str) -> str:
    user_input = user_input[1:]
    
    if user_input[:4] == "help":
        return help(user_input[5:])
    elif user_input[:6] == "lookup":
        return lookup(user_input[7:])
    else:
        return "Something went wrong. Please try again."