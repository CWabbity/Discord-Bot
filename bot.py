import asyncio # for debugging
import config
import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

filter_words = ["shit", "fuck"]

# console log when bot is ready
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(msg):
    if msg.author != client.user: # to check that message wasn't from bot
        # ping the bot
        if msg.content.lower().startswith("!ping"):
            await msg.channel.send(f"Hi, I am awake {msg.author.display_name}")

        # word filter
        for text in filter_words:
            if "Moderator" not in str(msg.author.roles) and text in str(msg.content.lower()):
                await msg.delete()
                print("Deleted filtered word...")
                return
        
        # create note
        if msg.content.lower().startswith("!createnote"):
            if os.path.exists("note.txt") == False:
                f = open("note.txt","a")
                f.write(msg.content.split(" ", 1)[1]) # remove the command in my message
                f.close()
                await msg.channel.send(f"note.txt has been created and note has been saved {msg.author.display_name}")
            else:
                await msg.channel.send(f"there is already an existing note {msg.author.display_name}")

        # read note
        if msg.content.lower().startswith("!readnote"):
            if os.path.exists("note.txt") == True:
                f = open("note.txt", "r")
                await msg.channel.send(f"The note says :{f.read()}")
            else:
                await msg.channel.send("There is no note to read!")

        # delete note
        if msg.content.lower().startswith("!deletenote"):
            if os.path.exists("note.txt") == True:
                os.remove("note.txt")
                await msg.channel.send(f"deleted note.txt {msg.author.display_name}")
            else:
                await msg.channel.send("file does not exist, unable to delete note!")

        # bot online status react message (displays the message)
        if msg.content.lower().startswith("!botstatus"):
            embed_bot_status = discord.Embed(title="Bot Status", description="React to the message to switch bot online status", type="rich", color=0x00ff00)
            embed_bot_status.add_field(name="How to use", value="🟢 = Online\n🟡 = Idle\n🔴 = Do not disturb\n❌ = Close this prompt", inline=False)
            sent_message = await msg.channel.send(embed=embed_bot_status)
            await sent_message.add_reaction("🟢")
            await sent_message.add_reaction("🟡")
            await sent_message.add_reaction("🔴")
            await sent_message.add_reaction("❌")
            bot_message_id = sent_message.id # grab current message id from bot

            # React to user reactions
            @client.event
            async def on_raw_reaction_add(payload): 
                message_id = payload.message_id
                if message_id == bot_message_id:
                    if payload.emoji.name == "🟢":
                        await client.change_presence(status=discord.Status.online) # change bot status to online
                        await sent_message.remove_reaction("🟢", payload.member) # remove user reaction to make it look nice
                        await sent_message.delete(delay=60) # deletes message if user does not respond after awhile
                        await msg.delete(delay=60)
                    elif payload.emoji.name == "🟡":
                        await client.change_presence(status=discord.Status.idle)
                        await sent_message.remove_reaction("🟡", payload.member)
                        await sent_message.delete(delay=60)
                        await msg.delete(delay=60)
                    elif payload.emoji.name == "🔴":
                        await client.change_presence(status=discord.Status.dnd)
                        await sent_message.remove_reaction("🔴", payload.member)
                        await sent_message.delete(delay=60)
                        await msg.delete(delay=60)
                    elif payload.emoji.name == "❌":
                        await sent_message.delete()
                        await msg.delete()

            @client.event
            async def on_raw_reaction_remove(payload):
                pass
        
        # purge/deletes all chat in text channel
        if msg.content.lower().startswith("!purge"):
            async with msg.channel.typing():
                purged_messages = await msg.channel.purge(limit=50)
                await msg.channel.send(f"Deleted {len(purged_messages)} message(s)")

        # bot typing feature
        if msg.content.lower().startswith("!typing"):
            async with msg.channel.typing():
                await asyncio.sleep(20)
            
            await msg.channel.send("Done!")

        # List all commands available currently for the bot
        if msg.content.lower().startswith("!help"):
            embed_command_list = discord.Embed(title="Command List", description="Displays all the current commands coded into the bot", color=0x00ff00)
            file_image = discord.File("image.jpg", filename="image.jpg")
            embed_command_list.set_image(url="attachment://image.jpg")
            embed_command_list.add_field(name="!help", value="Displays this message", inline=False)
            embed_command_list.add_field(name="!ping", value="Pings the bot", inline=False)
            embed_command_list.add_field(name="!createnote", value="Creates a note with your content", inline=False)
            embed_command_list.add_field(name="!readnote", value="Reads the current note if available", inline=False)
            embed_command_list.add_field(name="!deletenote", value="Deletes the note", inline=False)
            embed_command_list.add_field(name="!botstatus", value="Change bot online status", inline=False)
            embed_command_list.add_field(name="!purge", value="Deletes 50 messages in text channel", inline=False)
            embed_command_list.add_field(name="!typing", value="Debugging command", inline=False)
            await msg.channel.send(embed=embed_command_list, file=file_image)
            
        # optimize note taking feature using mongodb?
        # add music function

client.run(config.token)