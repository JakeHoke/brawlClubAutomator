from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import os, sys
import database

class RegisterUser(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Adds a User to Club's Database"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["player_tag"]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command 
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object

        try:
            player_tag = str(params[0])
            
        except Exception:
            await client.send_message(message.channel,
                                      "Please, provide valid player tag")
            return
        
        brawl_database = database.SQL_Server()
        user_name = str(message.author)
        if user_name in brawl_database.return_allUsers():
            await client.send_message(message.channel,
                        "The User has already been linked to an account")
            return
        
        if player_tag in brawl_database.return_allPlayers():
            await client.send_message(message.channel,
                            "The Tag has already been linked to other user")
            return

        brawl_database.insert_user(user_name, player_tag)
        brawl_database.save_database()
        msg = get_emoji(":ok_hand:") + f" The User {player_tag} has been linked to {user_name} in the database!"

        await client.send_message(message.channel, msg)
