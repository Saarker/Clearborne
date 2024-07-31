from psnawp_api import PSNAWP, core
from dotenv import load_dotenv
from discord import Embed
from datetime import datetime
import os

load_dotenv()
NPSSO = os.getenv('NPSSO')
psnawp = PSNAWP(npsso_cookie=NPSSO)

def lookup(input: str) -> dict:
    try:
        embedDict = {}
        user = psnawp.user(online_id=input)
        profileutil = user.profile()
        embedDict = {"title": f"{psnawp.user(online_id=input).online_id}",
                     "description": f"Account ID: {psnawp.user(online_id=input).account_id}\n",
                     "type": "rich"}
        if profileutil["isPlus"] == True:
            embedDict["title"] += " <:psplus:1268226188225151057>"
        
        embedDict["description"] += f"About Me: {profileutil["aboutMe"]}"
        profileDict = profileutil["avatars"]
        thumbnailDict = profileDict[1]["url"]   
        embedDict["thumbnail"] = {"url":thumbnailDict}
        embedDict["url"] = f"https://psnprofiles.com/{psnawp.user(online_id=input).online_id}"
        embedDict["color"] = 1258878
        
        gameDict = {}
        gameDictArray = []
        titles = user.title_stats()
        sorted_titles = sorted(titles, key=lambda x: x.last_played_date_time, reverse=True)
        if len(sorted_titles) >= 5:
            embedDict["description"] += "\n\n**Recently Played Games:**"
        else:
            raise IndexError
        for i in range(5):
            gameDict["name"] = sorted_titles[i].name
            gameDict["value"] = f"Last Played {str(datetime.now().astimezone() - sorted_titles[i].last_played_date_time)} ago\nTotal Playtime: {sorted_titles[i].play_duration}"
            gameDictArray.append(gameDict.copy())
            gameDict.clear()
        embedDict["fields"] = gameDictArray
        sorted_titles.clear()
        embed = Embed.from_dict(embedDict)
        return embed
    
    except IndexError:
        if sorted_titles:
            embedDict["description"] += "\n\n**Recently Played Games:**"
        for title in sorted_titles:
            gameDict["name"] = title.name
            gameDict["value"] = f"Last Played {str(datetime.now().astimezone() - title.last_played_date_time)} ago\nTotal Playtime: {title.play_duration}"
            gameDictArray.append(gameDict.copy())
            gameDict.clear()
        embedDict["fields"] = gameDictArray
        sorted_titles.clear()
        embed = Embed.from_dict(embedDict)
        return embed

    except core.PSNAWPNotFound:
        embedDict.clear()
        embedDict["description"] = "User not found. Please try looking up an existing user."
        embed = Embed.from_dict(embedDict)
        return embed

    except core.PSNAWPForbidden:
        embedDict.clear()
        embedDict["description"] = "User is private. If this is your profile, please set your privacy to Public."
        embed = Embed.from_dict(embedDict)
        return embed

    except Exception as e:
        print(e)
        embedDict.clear()
        embedDict["description"] = "Something went wrong. Please try again."
        embed = Embed.from_dict(embedDict)
        return embed
