from events.base_event      import BaseEvent
from utils                  import get_channel
import brawlstats
import database, configparser, math
from discord.utils import get

# Your friendly example event
# You can name this class as you like, but make sure to set BaseEvent
# as the parent class
class RegulateServer(BaseEvent):

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')
        self.interval_minutes = float(self.config.get('ConfigInfo', 'TIME_INTERVAL'))  # Set the interval for this event
        var = float(self.config.get('ConfigInfo', 'ALLOWED_TIME'))
        self.allowed_userWarning = math.ceil(var/self.interval_minutes)
        print(f"User Warning {self.allowed_userWarning}")
        super().__init__(self.interval_minutes)

    # Override the run() method
    # It will be called once every {interval_minutes} minutes
    async def run(self, client):
        activeServers = list(client.servers)[0]
        list_members = activeServers.members
        brawl_database = database.SQL_Server()
        print("Start Task")

        warning_channel = get_channel(client, "warnings")
        brawl_database = database.SQL_Server()

        if "ClubTag" not in brawl_database.return_allUsers():
                msg = "@everyone Club Tag not added to the database"
                await client.send_message(warning_channel , msg)
        else:
            for member in list_members:

                member        =  (str(member))
                member_object = activeServers.get_member_named(member)
                role          = [get(member_object.server.roles, name="member")]

                if member_object.bot or get(member_object.roles, name="owner"):
                    pass

                elif brawl_database.return_userWarning(member) >= self.allowed_userWarning and get(member_object.roles, name="member"):
                    msg = " removed from server since they did not insert player information in database"
                    await client.send_message(warning_channel , member_object.mention + msg)
                    await client.remove_roles(member_object, *role)

                elif member not in brawl_database.return_allUsers():
                    brawl_database.insert_user_warning(member)
                    msg = " did not insert player information in database"
                    await client.send_message(warning_channel , member_object.mention + msg)

                elif not brawl_database.infomation_present(member):
                    brawl_database.append_user_warning(member)
                    msg = " did not insert player information in database"
                    await client.send_message(warning_channel , member_object.mention + msg)

                elif get(member_object.roles, name="member"):
                    brawl_client = brawlstats.Client("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijk5MzM5YTRlLWFmYzItNDJhYy04ZTg1LWE1Y2JlOWE4YjhkOSIsImlhdCI6MTU4NjY1ODc3NSwic3ViIjoiZGV2ZWxvcGVyL2Q0OGFlYWJmLWQ4Y2MtNTMxYi02OTAwLTk5NmI4MjQ2ZWMzMCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTk4LjE5OS42Ny45NCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.25aIHp26Or2tPG6xAcd_CYx5rRAePm7uVDWOjyO-pOgRy4ymkNhZqd7ikcZG5ma35J1pEi-UhzQXR4W6uiX20Q")
                    with open('tags.txt', 'r') as f:
                        brawl_tag = f.read().splitlines()
                    list_users = []
                    list_users.extend(brawl_client.get_club_members(brawl_database.view_information_user("ClubTag")))
                    for tag in brawl_tag:
                        list_users.extend(brawl_client.get_club_members(tag))
                    if member not in list_users:
                        msg = " removed from server since they are not part of the club"
                        await client.send_message(warning_channel , member_object.mention + msg)
                        await client.remove_roles(member_object, *role)

