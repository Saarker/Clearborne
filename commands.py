from psnawp_api import PSNAWP, core
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
        titles_with_stats = user.title_stats()
        sorted_titles = sorted(titles_with_stats, key=lambda x: x.last_played_date_time, reverse=True)
        print(sorted_titles)
        for i in range(5):
            payload += f" \n"
            payload += f"**Game:** {sorted_titles[i].name} \n"
            payload += f"**Play Count:** {sorted_titles[i].play_count} \n"
            payload += f"**Play Duration:** {sorted_titles[i].play_duration} \n"
        sorted_titles.clear()
        return payload
    except IndexError:
        for title in sorted_titles:
            payload += f" \n"
            payload += f"**Game:** {title.name} \n"
            payload += f"**Play Count:** {title.play_count} \n"
            payload += f"**Play Duration:** {title.play_duration} \n"
            sorted_titles.clear()
        return payload
    except core.PSNAWPNotFound:
        return "User not found. Please try looking up an existing user."
    except core.PSNAWPForbidden:
        return "User is private. If this is your profile, please set your privacy to Public."
    except Exception as e:
        print(e)
        return "Something went wrong. Please try again."
    
def get_response(user_input: str) -> str:
    user_input = user_input[1:]
    
    if user_input[:4] == "help":
        return help(user_input[5:])
    elif user_input[:6] == "lookup":
        return lookup(user_input[7:])
    else:
        return "Something went wrong. Please try again."