from disnake import Embed

def help() -> dict:
    embed = Embed(description="/help: List of commands\n/lookup [online_id]: Lookup a PSN user\n")
    return embed 