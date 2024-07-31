from psnawp_api import PSNAWP, core
from dotenv import load_dotenv
from disnake import Embed, Color
from datetime import datetime
import os

load_dotenv()
NPSSO = os.getenv('NPSSO')
psnawp = PSNAWP(npsso_cookie=NPSSO)

def lookup(input: str) -> dict:
    embed = Embed()
    try:
        user = psnawp.user(online_id=input)
        profileutil = user.profile()
        embed = Embed(title=f"{psnawp.user(online_id=input).online_id}",
                      description=f"Account ID: {psnawp.user(online_id=input).account_id}\nAbout Me: {profileutil["aboutMe"]}",
                      type="rich",
                      url=f"https://psnprofiles.com/{psnawp.user(online_id=input).online_id}",
                      color=Color(0x13357e))
        
        if profileutil["isPlus"] == True:
            embed.title += " <:psplus:1268226188225151057>"
        
        profileDict = profileutil["avatars"]
        thumbnailDict = profileDict[1]["url"]   
        embed.set_thumbnail(url=thumbnailDict)
        
        titles = user.title_stats(limit=5)
        sorted_titles = sorted(titles, key=lambda x: x.last_played_date_time, reverse=True)
        if len(sorted_titles) == 0:
            return embed
        embed.description += "\n\n**Recently Played Games:**"
        for title in sorted_titles:
            embed.add_field(name=title.name,
                            value=f"Last Played {str(datetime.now().astimezone() - title.last_played_date_time)} ago\nTotal Playtime: {title.play_duration}",
                            inline=False) 
        sorted_titles.clear()
        return embed
    
    except core.PSNAWPNotFound:
        embed = Embed()
        embed.description = "User not found. Please try looking up an existing user."
        return embed

    except core.PSNAWPForbidden:
        embed = Embed()
        embed.description = "User is private. If this is your profile, please set your privacy to Public."
        return embed

    except Exception as e:
        print(e)
        embed = Embed()
        embed.description = "Something went wrong. Please try again."
        return embed

