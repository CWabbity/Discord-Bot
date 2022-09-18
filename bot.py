import config
import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

filter_words = ["shit"]

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
                        print("Online Clicked") # debug code
                    elif payload.emoji.name == "🟡":
                        await client.change_presence(status=discord.Status.idle)
                        await sent_message.remove_reaction("🟡", payload.member)
                        print("Idle CLicked")
                    elif payload.emoji.name == "🔴":
                        await client.change_presence(status=discord.Status.dnd)
                        await sent_message.remove_reaction("🔴", payload.member)
                        print("DND Clicked")
                    elif payload.emoji.name == "❌":
                        await sent_message.delete()
                        await msg.delete()

            @client.event
            async def on_raw_reaction_remove(payload):
                pass

            # add feature to delete the prompt(like the bot status mesage) itself after 30 seconds
            # optimize note taking feature using mongodb?

client.run(config.token)