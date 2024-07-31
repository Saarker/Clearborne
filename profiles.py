from psnawp_api import PSNAWP, core
from dotenv import load_dotenv
from discord import Embed
import os

load_dotenv()
NPSSO = os.getenv('NPSSO')
psnawp = PSNAWP(npsso_cookie=NPSSO)

def lookup(input: str) -> dict:
    try:
        embedDict = {}
        user = psnawp.user(online_id=input)
        profileutil = user.profile()
        embedDict = {"title": "User Profile",
                     "description": f"Online ID: {psnawp.user(online_id=input).online_id}\n Account ID: {psnawp.user(online_id=input).account_id}\n About Me: {profileutil["aboutMe"]}",
                     "type": "rich"}
        profileDict = profileutil["avatars"]
        thumbnailDict = profileDict[1]["url"]   
        embedDict["thumbnail"] = {"url":thumbnailDict}
        embedDict["url"] = f"https://psnprofiles.com/{psnawp.user(online_id=input).online_id}"
        embedDict["color"] = 1258878
        print(embedDict)
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
            gameDict["value"] = f"Play Count: {sorted_titles[i].play_count}\nPlay Duration: {sorted_titles[i].play_duration}"
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
            gameDict["value"] = f"Play Count: {title.play_count}\nPlay Duration: {title.play_duration}"
            gameDictArray.append(gameDict.copy())
            gameDict.clear()
        embedDict["fields"] = gameDictArray
        sorted_titles.clear()
        embed = Embed.from_dict(embedDict)
        return embed
    except core.PSNAWPNotFound:
        embedDict["description"] = "User not found. Please try looking up an existing user."
        embed = Embed.from_dict(embedDict)
        return embed
    except core.PSNAWPForbidden:
        embedDict["description"] = "User is private. If this is your profile, please set your privacy to Public."
        embed = Embed.from_dict(embedDict)
        return embed
    except Exception as e:
        print(e)
        embedDict["description"] = "Something went wrong. Please try again."
        embed = Embed.from_dict(embedDict)
        return embed
