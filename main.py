# IMPORTS
import discord
from discord_secrets import secrets
import os
import random

# VARIABLES
# Token, Admin Id, and Client
TOKEN = secrets.get("TOKEN")
ADMIN_ID = secrets.get("ADMIN_ID")
bot_intents = discord.Intents.default()
bot_intents.message_content = True
client = discord.Client(intents = bot_intents)
DIRECTORY_USER_DATA = "User Data"
DIRECTORY_BOT_DATA = "Bot Data\\"
DIRECTORY_UPDATE_LOGS = "Update Logs\\"
DIRECTORY_DELETION_REQUESTS = "Deletion Requests\\"
DIRECTORY_PERSONAL_MESSAGES = "Personal Messages\\"
# Other
hello_list = ["Hello ", "Hi ", "How's it goin' ",
              "'Sup ", "Wsp ", "Ello ", "Hiiii "]

# FUNCTIONS
def format_num(num):
    return f"{num:,}".replace(",", " ")

# MAIN FUNCTION
def main():
    @client.event
    async def on_ready():
        print(client.user.name + " is online.")

    @client.event
    async def on_message(message):

        if(message.content.startswith("/lime ") and
        message.author != client.user):
            
            command = message.content.replace("/lime ", "")

            # Gathering and/or creating data about the user
            author_id = str(message.author.id)
            user_file_name = DIRECTORY_USER_DATA + "\\id" + author_id + ".txt"
            if not os.path.isfile(user_file_name):
                with open(user_file_name, "w") as file:
                    file.write(
                        "(Use \"/lime name\" to change your name)" +
                        "\n0\nno\ngreen"
                    )
            with open(user_file_name, "r") as file:
                user_prefname = file.readline().strip()
                user_cmd_count = int(file.readline().strip())
                user_read_announcement = file.readline().strip()
                match file.readline():
                    case "red":
                        user_color = 0xff0000
                    case "orange":
                        user_color = 0xff8000
                    case "yellow":
                        user_color = 0xffff00
                    case "green":
                        user_color = 0x00ff00
                    case "blue":
                        user_color = 0x0000ff
                    case "purple":
                        user_color = 0x800080
                    case "white":
                        user_color = 0xffffff
                    case _:
                        user_color = 0x000000
            user_cmd_count += 1

            # Checking if the user should be warned of unread announcement
            if user_read_announcement == "no" and command != "announcement":
                embed = discord.Embed(
                    title = "Unread Announcement!!",
                    description = (
                        "You have an unread annoucement." + 
                        "\nUse \"/lime announcement\" to read it"
                    ),
                    color = user_color
                )
                await message.channel.send(embed = embed)

            # Checking if the user has a personal message
            entry_name = (
                DIRECTORY_PERSONAL_MESSAGES + "id" + author_id + ".txt"
            )
            if os.path.isfile(entry_name):
                with open(entry_name) as file:
                    content = file.read()
                os.remove(entry_name)
                embed = discord.Embed(
                    title = "Personal Message From the Admin",
                    description = content, color = user_color
                )
                await message.author.send(embed = embed)

            # COMMANDS
            # MY INFO
            if command == "my info" or command == "me":
                # Get place in Commands Ran leaderboard
                num_list = []
                for entry in os.listdir(DIRECTORY_USER_DATA):
                    entry_name = os.path.join(DIRECTORY_USER_DATA, entry)
                    if os.path.isfile(entry_name):
                        with open(entry_name, "r") as file:
                            file.readline()
                            num_list.append(int(file.readline().strip()))
                num_list.sort()
                num_list.reverse()
                user_cmd_place = len(num_list)
                for num in num_list:
                    if num == user_cmd_count - 1:
                        user_cmd_place = num_list.index(num) + 1
                        break
                # Get current color
                match user_color:
                    case 0xff0000:
                        user_color_name = "red"
                    case 0xff8000:
                        user_color_name = "orange"
                    case 0xffff00:
                        user_color_name = "yellow"
                    case 0x00ff00:
                        user_color_name = "green"
                    case 0x0000ff:
                        user_color_name = "blue"
                    case 0x800080:
                        user_color_name = "purple"
                    case 0xffffff:
                        user_color_name = "white"
                    case 0x000000:
                        user_color_name = "black"
                    case _:
                        user_color_name = (
                            "There was a problem getting your color."
                        )
                # Formatting and sending info
                content = (
                    "Your Discord Name: " + message.author.name +
                    "\nYour Discord Nickname: " +
                    message.author.display_name +
                    "\nYour Name for LimeBot: " + user_prefname +
                    "\nCommands Ran: " + format_num(user_cmd_count) +
                    " (#" + format_num(user_cmd_place) + ")" +
                    "\nColor: " + user_color_name
                )
                embed = discord.Embed(
                    title = user_prefname + "'s Info",
                    description = content, color = user_color
                )
                embed.set_thumbnail(url = message.author.avatar)
                await message.channel.send(embed = embed)

            # NAME
            elif command.startswith("name "):
                passed_name = command.replace("name ", "").strip()
                name = ""
                # Checking if name is acceptable for writing to text file
                for char in passed_name:
                    try:
                        if ord(char) > 127:
                            name = ""
                            break
                        else:
                            name += char
                    except:
                        name = ""
                if name == "":
                    name = "Invalid Name"
                # Preventing multi-line names
                name = name.replace("\n", " ")
                user_prefname = name
                # Formating and sending result
                if name == "Invalid Name":
                    title_content = "Invalid Character(s) Used."
                else:
                    title_content = "Your Name Has Been Changed."
                embed = discord.Embed(
                    title = title_content,
                    description = "Name is now: " + user_prefname,
                    color = user_color
                )
                await message.channel.send(embed = embed)

            # COLOR
            elif command.startswith("color "):
                passed_color = command.replace("color ", "").strip()
                # Converting to machine-readable color
                failed = False
                new_color = passed_color.capitalize()
                match passed_color:
                    case "red":
                        user_color = 0xff0000
                    case "orange":
                        user_color = 0xff8000
                    case "yellow":
                        user_color = 0xffff00
                    case "green":
                        user_color = 0x00ff00
                    case "blue":
                        user_color = 0x0000ff
                    case "purple":
                        user_color = 0x800080
                    case "white":
                        user_color = 0xffffff
                    case "black":
                        user_color = 0x000000
                    case _:
                        failed = True
                # Formatting and sending result
                if not failed:
                    title_content = (
                        user_prefname + " Changed Their Color."
                    )
                    content = "New color: " + new_color
                else:
                    title_content = "That Is Not an Available Color."
                    content = "No new color for you. :cry:"
                embed = discord.Embed(
                    title = title_content,
                    description = content,
                    color = user_color
                )
                await message.channel.send(embed = embed)

            # YOUR INFO
            elif command == "your info":
                # Getting user and commands ran counts
                user_count = 0
                cmd_count = 0
                for entry in os.listdir(DIRECTORY_USER_DATA):
                    entry_name = os.path.join(DIRECTORY_USER_DATA, entry)
                    if os.path.isfile(entry_name):
                        user_count += 1
                        with open(entry_name, "r") as file:
                            file.readline()
                            this_count = int(file.readline().strip())
                            cmd_count += this_count
                # Getting stored LimeBot data
                with open(DIRECTORY_BOT_DATA + "bot data.txt", "r") as file:
                    version = file.readline().strip()
                    status = file.readline().strip()
                    loc = file.readline().strip()
                    cmds_count = file.readline().strip()
                # Formatting and sending data
                try:
                    loc_text = format_num(int(loc))
                except ValueError:
                    loc_text = loc
                content = (
                    version + " - " + status +
                    "\nUsers: " + format_num(user_count) +
                    "\nCommands Ran: " + format_num(cmd_count + 1) +
                    "\nLines of Code: " + loc_text +
                    "\nCommands: " + cmds_count
                )
                embed = discord.Embed(
                    title = "LimeBot's Info",
                    description = content, color = user_color
                )
                embed.set_thumbnail(url = client.user.avatar)
                await message.channel.send(embed = embed)

            # HELLO
            elif command.startswith("hello") or command.startswith("hi"):
                # Generating message
                random_num = random.randint(0, len(hello_list) - 1)
                hello_message = hello_list[random_num] + user_prefname
                if 2 <= random_num <= 4:
                    hello_message += "?"
                else:
                    hello_message += "!"
                # Formatting and sending message
                embed = discord.Embed(
                    title = hello_message, color = user_color
                )
                await message.channel.send(embed = embed)

            # RATE
            elif command.startswith("rate "):
                # Getting thing to rate
                rated_user = command.replace("rate ", "").strip()
                if rated_user.startswith("<"):
                    id_to_find = (
                        rated_user.replace("<@", "").replace(">", "")
                    )
                    file_to_find = (
                        DIRECTORY_USER_DATA + "\\id" + id_to_find + ".txt"
                    )
                    if id_to_find == "987105587127025756":
                        rated_user = "LimeBot"
                    else:
                        try:
                            with open(file_to_find, "r") as file:
                                rated_user = file.readline().strip()
                        except OSError:
                            rated_user = "Unknown User"
                elif rated_user == "me":
                    rated_user = user_prefname
                # Rating thing
                if rated_user.lower() == "limebot":
                    random_num = "11"
                    rated_user = "LimeBot"
                else:
                    random_num = str(random.randint(1, 10))
                # Formatting and sending result
                if random_num == "8" or random_num == "11":
                    piece = " an "
                else:
                    piece = " a "
                embed = discord.Embed(
                    title = rated_user + " is" + piece + random_num + ".",
                    color = user_color
                )
                await message.channel.send(embed = embed)

            # ANNOUNCEMENT
            elif command == "announcement":
                # Getting latest annoucement
                with(open(DIRECTORY_BOT_DATA + "announcement.txt", "r")
                as file):
                    content = file.read()
                # Formatting and sending announcement
                embed = discord.Embed(
                    title = "Announcement:", description = content,
                    color = user_color
                )
                if user_read_announcement == "yes":
                    embed.set_footer(
                        text = "You have already read this annoucement."
                    )
                else:
                    embed.set_footer(
                        text = "Announcement marked as read."
                    )
                user_read_announcement = "yes"
                await message.channel.send(embed = embed)

            # LEADERBOARD
            elif command == "leaderboard" or command == "lb":
                # Getting data
                name_list = []
                cmd_list = []
                for entry in os.listdir(DIRECTORY_USER_DATA):
                    entry_name = os.path.join(DIRECTORY_USER_DATA, entry)
                    if os.path.isfile(entry_name):
                        with open(entry_name, "r") as file:
                            name_list.append(file.readline().strip())
                            cmd_list.append(
                                int(file.readline().strip())
                            )
                # Formatting data
                content = "by Total Commands Ran"
                for i in range(1, 6):
                    if cmd_list != []:
                        pos = cmd_list.index(max(cmd_list))
                        name_to_add = name_list[pos]
                        cmd_to_add = format_num(cmd_list[pos])
                        name_list.pop(pos)
                        cmd_list.pop(pos)
                        content += (
                            "\n" + str(i) + ". " + name_to_add +
                            " - " + cmd_to_add
                        )
                # Sending data
                embed = discord.Embed(
                    title = "LimeBot Leaderboard", description = content,
                    color = user_color
                )
                await message.channel.send(embed = embed)

            # VIEW UPDATE LOGS
            elif command.startswith("view update"):
                # Looping through update logs
                for entry in os.listdir(DIRECTORY_UPDATE_LOGS):
                    entry_name = os.path.join(DIRECTORY_UPDATE_LOGS, entry)
                    if os.path.isfile(entry_name):
                        # Getting info
                        with open(entry_name, "r") as file:
                            content = file.read()
                        # Sending info
                        embed = discord.Embed(
                            title = entry.replace(".txt", ""),
                            description = content, color = user_color
                        )
                        await message.channel.send(embed = embed)

            # VIEW STORED DATA
            elif command == "view stored data":
                # Making and formatting content
                embed = discord.Embed(
                    title = "Stored Data", color = user_color
                )
                embed.add_field(
                    name = "• Your Discord account's id",
                    value = "This is the id used to identify your account." +
                    " This id can easily be found by any person" +
                    " with developer tools on or any bot.", inline = False
                )
                embed.add_field(
                    name = "• Your LimeBot account's name",
                    value = "Found in \"/lime my info\".", inline = False
                )
                embed.add_field(
                    name = "• Your LimeBot account's color",
                    value = "Found on the side of this message." +
                    " Used to control what color" +
                    " messages to you will appear as.", inline = False
                )
                embed.add_field(
                    name = "• Your LimeBot account's command count",
                    value = "Found in \"/lime my info\".", inline = False
                )
                embed.add_field(
                    name = "• Whether you've read the latest announcement.",
                    value = "Found in \"/lime announcement\"." +
                    " If the announcement says" +
                    " \"You have already read this annoucement.\"" +
                    " then it will be \"yes\".", inline = False
                )
                embed.add_field(
                    name = "• Aditional data for deletion requests",
                    value = "Id and reason for request.", inline = False
                )
                # Sending content
                await message.channel.send(embed = embed)

            # REQUEST ACCOUNT DELETION
            elif command.startswith("request account deletion"):
                reason_given = (
                    command.replace("request account deletion", "").strip()
                )
                if reason_given == "":
                    reason_given = "No reason given."
                # Submitting request
                with(open(DIRECTORY_DELETION_REQUESTS +
                "request_id" + author_id + ".txt", "w") as file):
                    file.write(reason_given)
                # Sending result
                embed = discord.Embed(
                    title = "Request Submitted",
                    description = (
                        "Requests are not granted automatically " + 
                        "so you may need to wait awhile."
                    ), color = user_color
                )
                await message.channel.send(embed = embed)

            # HELP
            elif command == "help":
                # Making and formatting content
                embed = discord.Embed(
                    title = "LimeBot Command List", color = user_color
                )
                embed.add_field(
                    name = "my info",
                    value = "• displays info about you" +
                    "\n• accepts \"/lime me\" as well", inline = False
                )
                embed.add_field(
                    name = "name <name>", value = "• change your name",
                    inline = False
                )
                embed.add_field(
                    name = "color <color>",
                    value = "• change your message's color" +
                    "\n• red, orange, yellow, green, " +
                    "blue, purple, white, or black", inline = False
                )
                embed.add_field(
                    name = "your info",
                    value = "• displays info about LimeBot",
                    inline = False
                )
                embed.add_field(
                    name = "hello",
                    value = "• say hello to LimeBot" +
                    "\n• accepts \"/lime hi\" as well",
                    inline = False
                )
                embed.add_field(
                    name = "rate <user>",
                    value = "• LimeBot will rate you" +
                    "\n• <user> can be a name or @ mention" +
                    "\n• NOT meant to be taken seriously", inline = False
                )
                embed.add_field(
                    name = "announcement",
                    value = "• read the latest announcement",
                    inline = False
                )
                embed.add_field(
                    name = "leaderboard",
                    value = "• see the current Commands Ran leaderboard" +
                    "\n• accepts \"/lime lb\" as well", inline = False
                )
                embed.add_field(
                    name = "view update logs",
                    value = "• view logs of all LimeBot updates" +
                    "\n• accepts \"/lime view updates\" as well",
                    inline = False
                )
                embed.add_field(
                    name = "view stored data",
                    value = "• view what data LimeBot stores about you",
                    inline = False
                )
                embed.add_field(
                    name = "request account deletion <reason>",
                    value = "• requestion for your account to be deleted" +
                    "\n• <reason> is your reason for this request",
                    inline = False
                )
                embed.add_field(
                    name = "help", value = "• super helpful",
                    inline = False
                )
                embed.set_footer(
                    text = "All commands start with \"/lime\". " +
                    "Ex. \"/lime help\"."
                )
                # Sending content
                await message.channel.send(embed = embed)

            # ADMIN COMMANDS - ME ONLY
            elif author_id == ADMIN_ID:

                # CLEAR DATA
                if command.startswith("clear data "):
                    id_to_remove = command.replace("clear data ", "").strip()
                    # Clearing all data
                    if id_to_remove == "all":
                        users_removed = 0
                        for entry in os.listdir(DIRECTORY_USER_DATA):
                            entry_name = os.path.join(
                                DIRECTORY_USER_DATA, entry
                            )
                            if os.path.isfile(entry_name):
                                os.remove(entry_name)
                                users_removed += 1
                        # Formatting and sending result
                        embed = discord.Embed(
                            title = "All User Data Cleared",
                            description = (
                                str(users_removed) + " users deleted."
                            ), color = user_color
                        )
                        await message.channel.send(embed = embed)
                    # Clearing one user's data
                    else:
                        entry_name = (
                            DIRECTORY_USER_DATA + "\\id" +
                            id_to_remove + ".txt"
                        )
                        if os.path.isfile(entry_name):
                            os.remove(entry_name)
                            # Formatting and sending result
                            embed = discord.Embed(
                                title ="One User's Data Cleared",
                                description = id_to_remove + " was deleted.",
                                color = user_color
                            )
                            await message.channel.send(embed = embed)

                # UPDATE
                elif command.startswith("update "):
                    # Getting current data
                    with(open(DIRECTORY_BOT_DATA + "bot data.txt", "r")
                    as file):
                        new_version = file.readline().strip()
                        new_status = file.readline().strip()
                        new_loc = file.readline().strip()
                        new_cmd_count = file.readline().strip()
                    to_update = (
                        command.replace("update ", "").strip().split(" ")
                    )
                    if len(to_update) > 1:
                        match(to_update[0]):
                            case "version":
                                new_version = to_update[1]
                            case "status":
                                new_status = to_update[1]
                            case "loc":
                                new_loc = to_update[1]
                            case "commands":
                                new_cmd_count = ""
                                for i in range(1, len(to_update)):
                                    new_cmd_count += to_update[i] + " "
                                new_cmd_count = new_cmd_count.strip()
                    # Returning updated data
                    with(open(DIRECTORY_BOT_DATA + "bot data.txt", "w")
                    as file):
                        file.write(
                            new_version + "\n" + new_status + "\n" +
                            new_loc + "\n" + new_cmd_count
                        )
                    # Formatting and sending current data
                    content = (
                        "Version: " + new_version +
                        "\nStatus: " + new_status + "\nLoC: " + new_loc +
                        "\nCommand Count: " + new_cmd_count
                    )
                    embed = discord.Embed(
                        title = "Updated Info",
                        description = content, color = user_color
                    )
                    await message.channel.send(embed = embed)

                # CHANGE NAME
                elif command.startswith("change name "):
                    # Getting id and name to change
                    passed_content = (
                        command.replace("change name ", "")
                        .strip().replace("\n", " ", 1).split(" ")
                    )
                    new_name = ""
                    if len(passed_content) > 1:
                        id_to_change = passed_content[0]
                        for i in range(1, len(passed_content)):
                            new_name += passed_content[i] + " "
                        new_name = new_name.strip()
                    else:
                        id_to_change = "No ID Given"
                    # Changing id's name
                    try:
                        file_to_find = (
                            DIRECTORY_USER_DATA + "\\id" +
                            id_to_change + ".txt"
                        )
                        with open(file_to_find, "r") as file:
                            file.readline()
                            cmd_count = file.readline().strip()
                            read_announcement = file.readline().strip()
                            color = file.readline().strip()
                        with open(file_to_find, "w") as file:
                            file.write(
                                new_name + "\n" + cmd_count + "\n" +
                                read_announcement + "\n" + color
                            )
                        embed = discord.Embed(
                            title = "Name Changed",
                            description = "New Name: " + new_name,
                            color = user_color
                        )
                    # Catching error if id not in users
                    except OSError:
                        embed = discord.Embed(
                            title = "User Not Found",
                            description = id_to_change + " does not exist.",
                            color = user_color
                        )
                    # Sending result
                    await message.channel.send(embed = embed)

                # NEW ANNOUNCEMENT
                elif command.startswith("new announcement"):
                    # Getting new announcement
                    content = command.replace("new announcement", "").strip()
                    if content != "":
                        # Updating announcement file
                        with(open(DIRECTORY_BOT_DATA + "announcement.txt",
                        "w") as file):
                            file.write(content)
                        # Resetting users
                        for entry in os.listdir(DIRECTORY_USER_DATA):
                            entry_name = (
                                os.path.join(DIRECTORY_USER_DATA, entry)
                            )
                            if(os.path.isfile(entry)):
                                with open(entry_name, "r") as file:
                                    file_content = ""
                                    file_content += (
                                        file.readline() + file.readline()
                                    )
                                    file.readline()
                                    file_content2 = file.readline()
                                with open(entry_name, "w") as file:
                                    file.write(
                                        file_content + "no\n" + file_content2
                                    )
                        # Formatting and sending result
                        embed = discord.Embed(
                            title = "New Announcement", description = content,
                            color = user_color
                        )
                        user_read_announcement = "yes"
                        await message.channel.send(embed = embed)

                # PERSONAL MESSAGE
                elif command.startswith("personal message "):
                    # Getting data
                    passed_content = (
                        command.replace("personal message ", "")
                        .strip().replace("\n", " ", 1).split(" ")
                    )
                    id_to_message = ""
                    message_to_send = ""
                    if len(passed_content) > 1:
                        id_to_message = passed_content[0]
                        for i in range(1, len(passed_content)):
                            message_to_send += passed_content[i]
                            if not passed_content[i].startswith("\n"):
                                message_to_send = (
                                    message_to_send.strip() + " "
                                )
                    if id_to_message != "":
                        # Storing data
                        with(open(DIRECTORY_PERSONAL_MESSAGES + "id" +
                        id_to_message + ".txt", "w") as file):
                            file.write(message_to_send)
                        # Formatting result
                        embed = discord.Embed(
                            title = "Personal Message to " + id_to_message,
                            description = message_to_send, color = user_color
                        )
                    else:
                        embed = discord.Embed(
                            title = "No ID Given to Message",
                            color = user_color
                        )
                    # Sending result
                    await message.channel.send(embed = embed)

                # GET NAMES
                elif command == "get users" or command == "list users":
                    # Getting data and formatting message content
                    content = ""
                    for entry in os.listdir(DIRECTORY_USER_DATA):
                        entry_name = os.path.join(DIRECTORY_USER_DATA, entry)
                        if os.path.isfile(entry_name):
                            id_of_user = (
                                entry.replace("id", "")
                                .replace(".txt", "")
                            )
                            with open(entry_name, "r") as file:
                                name_of_user = file.readline()
                            content += (
                                "\n" + id_of_user + " - " + name_of_user
                            )
                    # Completing and sending message
                    embed = discord.Embed(
                        title = "List of LimeBot Users",
                        description = content, color = user_color
                    )
                    await message.channel.send(embed = embed)

                # NEW UPDATE LOG
                elif command.startswith("new update log "):
                    # Getting update log info
                    passed_content = (
                        command.replace("new update log ", "")
                        .strip().replace("\n", " ", 1).split(" ")
                    )
                    update_title = "Remove This Update"
                    update_description = ""
                    if len(passed_content) > 1:
                        update_title = passed_content[0]
                        for i in range(1, len(passed_content)):
                            update_description += passed_content[i]
                            if not passed_content[i].startswith("\n"):
                                update_description = (
                                    update_description.strip() + " "
                                )
                    update_description = update_description.strip()
                    # Creating update log
                    with(open(DIRECTORY_UPDATE_LOGS +
                    update_title + ".txt", "w") as file):
                        file.write(update_description)
                    # Formatting and sending info
                    embed = discord.Embed(
                        title = "New Update Log Created: " + update_title,
                        description = update_description, color = user_color
                    )
                    await message.channel.send(embed = embed)

                # CLEAR UPDATE LOGS
                elif command == "clear update logs":
                    # Deleting update logs
                    logs_cleared = 0
                    for entry in os.listdir(DIRECTORY_UPDATE_LOGS):
                        entry_name = os.path.join(
                            DIRECTORY_UPDATE_LOGS, entry
                        )
                        if os.path.isfile(entry_name):
                            os.remove(entry_name)
                            logs_cleared += 1
                    # Formatting and sending result
                    embed = discord.Embed(
                        title = "All Update Logs Deleted",
                        description = (
                            str(logs_cleared) + " update logs deleted."
                        ), color = user_color
                    )
                    await message.channel.send(embed = embed)

                # VIEW DELETION REQUESTS
                elif command == "view deletion requests":
                    embed = discord.Embed(
                        title = "Deletion Requests",
                        color = user_color
                    )
                    total_requests = 0
                    for entry in os.listdir(DIRECTORY_DELETION_REQUESTS):
                        entry_name = os.path.join(
                            DIRECTORY_DELETION_REQUESTS, entry
                        )
                        if os.path.isfile(entry_name):
                            with open(entry_name, "r") as file:
                                reason_given = file.readline().strip()
                            embed.add_field(
                                name = entry.replace(".txt", ""),
                                value = reason_given, inline = False
                            )
                            total_requests += 1
                    embed.add_field(
                        name = "Total: " + str(total_requests),
                        value = "Grant or Deny requests to remove them.",
                        inline = False
                    )
                    await message.channel.send(embed = embed)
                    

                # GRANT DELETION REQUEST
                elif command.startswith("grant deletion request "):
                    id_to_grant = (
                        command.replace("grant deletion requst ", "").strip()
                    )
                    content = ""
                    if id_to_grant == "all":
                        for entry in os.listdir(DIRECTORY_DELETION_REQUESTS):
                            entry_name = os.path.join(
                                DIRECTORY_DELETION_REQUESTS, entry
                            )
                            if os.path.isfile(entry_name):
                                id_found = entry.replace("request_", "")
                                os.remove(entry_name)
                                entry_name2 = (
                                    DIRECTORY_USER_DATA + "\\" + id_found
                                )
                                if os.path.isfile(entry_name2):
                                    os.remove(entry_name2)
                                    content += (
                                        "• " + id_found.replace("id", "")
                                        .replace(".txt", "") + "\n"
                                    )
                    else:
                        entry_name = (
                            DIRECTORY_DELETION_REQUESTS + "request_id"
                            + id_to_grant + ".txt"
                        )
                        if os.path.isfile(entry_name):
                            os.remove(entry_name)
                            entry_name2 = (
                                DIRECTORY_USER_DATA + "\\request_id" +
                                id_to_grant + ".txt"
                            )
                            if os.path.isfile(entry_name2):
                                os.remove(entry_name2)
                                content += "• " + id_to_grant + "\n"
                    content = content.strip()
                    if content == "":
                        content = "No requests granted."
                    embed = discord.Embed(
                        title = "Granted Deletion Requests:",
                        description = content, color = user_color
                    )
                    await message.channel.send(embed = embed)

                # DENY DELETION REQUEST
                elif command.startswith("deny deletion request "):
                    id_to_deny = (
                        command.replace("deny deletion request ", "").strip()
                    )
                    content = ""
                    if id_to_deny == "all":
                        for entry in os.listdir(DIRECTORY_DELETION_REQUESTS):
                            entry_name = os.path.join(
                                DIRECTORY_DELETION_REQUESTS, entry
                            )
                            if os.path.isfile(entry_name):
                                id_found = (
                                    entry.replace("request_id", "")
                                    .replace(".txt", "")
                                )
                                os.remove(entry_name)
                                content += "• " + id_found + "\n"
                    else:
                        entry_name = (
                            DIRECTORY_DELETION_REQUESTS + "request_id"
                            + id_to_deny + ".txt"
                        )
                        if os.path.isfile(entry_name):
                            os.remove(entry_name)
                            content += "• " + id_to_deny + "\n"
                    content = content.strip()
                    if content == "":
                        content = "No requests denied."
                    embed = discord.Embed(
                        title = "Denied Deletion Requests:",
                        description = content, color = user_color
                    )
                    await message.channel.send(embed = embed)

                # ADMIN HELP
                elif command == "admin help":
                    # Making and formatting content
                    embed = discord.Embed(
                        title = "LimeBot Admin Command List",
                        color = user_color
                    )
                    embed.add_field(
                        name = "clear data <id>",
                        value = "• <id> represents id to clear" +
                        "\n• \"all\" clears all user data",
                        inline = False
                    )
                    embed.add_field(
                        name = "update <field>",
                        value = "• <field> options below" +
                        "\n• version" +
                        "\n• status" +
                        "\n• loc" +
                        "\n• commands",
                        inline = False
                    )
                    embed.add_field(
                        name = "change name <id> <name>",
                        value = "• <name> represents the name to give <id>",
                        inline = False
                    )
                    embed.add_field(
                        name = "personal message <id> <message>",
                        value = "• sends <message> to <id> next time they " +
                        "are online\n• <message> can be on a serarate line",
                        inline = False
                    )
                    embed.add_field(
                        name = "new announcement <announcement>",
                        value = "• creates a new annoucement" +
                        "\n• <annoucement> can be on a serarate line",
                        inline = False
                    )
                    embed.add_field(
                        name = "get users/list users",
                        value = "• get a list of all user ids and names",
                        inline = False
                    )
                    embed.add_field(
                        name = "new update log <version> <text>",
                        value = "• creates an update log" +
                        "\n• can be used to change existing update logs" +
                        "\n• <text> can be on a separate line",
                        inline = False
                    )
                    embed.add_field(
                        name = "clear update logs",
                        value = "• clears all update logs",
                        inline = False
                    )
                    embed.add_field(
                        name = "view deletion requests",
                        value = "• show all deletion requests",
                        inline = False
                    )
                    embed.add_field(
                        name = "grant deletion request <id>",
                        value = "• <id> represents id of request" +
                        "\n• \"all\" grants all requests",
                        inline = False
                    )
                    embed.add_field(
                        name = "deny deletion request <id>",
                        value = "• <id> represents id of request" +
                        "\n• \"all\" denies all requests",
                        inline = False
                    )
                    embed.add_field(
                        name = "admin help",
                        value = "• help with admin commands",
                        inline = False
                    )
                    await message.channel.send(embed = embed)

                # IF COMMAND DOESN'T EXIST - ADMIN VERSION
                else:
                    user_cmd_count -= 1
                    embed = discord.Embed(
                        title = "That Command Does Not Exist",
                        description = (
                            "See \"/lime help\" " +
                            "for available commands."
                        ), color = user_color
                    )
                    await message.channel.send(embed = embed)

            # IF COMMAND DOESN'T EXIST
            else:
                user_cmd_count -= 1
                content = (
                    "Use \"lime help\" to see a list of commands. " +
                    "Please note that LimeBot is case-sensitive, " +
                    "meaning you must use /lime, " +
                    "not /LiMe, and such."
                )
                embed = discord.Embed(
                    title = "That Command Does Not Exist",
                    description = content,
                    color = user_color)
                await message.channel.send(embed = embed)

            # UPDATING USER DATA
            match user_color:
                case 0xff0000:
                    user_color = "red"
                case 0xff8000:
                    user_color = "orange"
                case 0xffff00:
                    user_color = "yellow"
                case 0x00ff00:
                    user_color = "green"
                case 0x0000ff:
                    user_color = "blue"
                case 0x800080:
                    user_color = "purple"
                case 0xffffff:
                    user_color = "white"
                case _:
                    user_color = "black"
            with open(user_file_name, "w") as file:
                file.write(
                    user_prefname + "\n" + str(user_cmd_count) +
                    "\n" + user_read_announcement + "\n" + user_color
                )

# RUN MAIN FUNCTION
main()
client.run(TOKEN)