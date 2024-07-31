from discord import Embed

def help(input: str) -> dict:
    embedDict = {"description": "^help: List of commands\n^lookup [online_id]: Lookup a PSN user\n",
                 "type": "rich"}
    embed = Embed.from_dict(embedDict)
    return embed 