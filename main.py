import discord
from discord.ext import commands
from discord.ui import View, Button
import json
from datetime import datetime

# Configuration file for messages and IDs
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Privileged Gateway Intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.messages = True
intents.guilds = True
intents.message_content = True

# Bot Prefix
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    log_message(f" Login Success: {bot.user.name}")

# Function for nicely formatted logging messages to console
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}][LOG]{message}")

# Function to prevent any normal user from sending the embed
def permissioned():
    async def predicate(ctx):
        permission_role = config["permission_role"]
        member = ctx.author
        guild = ctx.guild
        staff_role = discord.utils.get(guild.roles, id=int(permission_role))
        return staff_role in member.roles

    return commands.check(predicate)

# Function that is called to check if the user's DMs are closed or open
async def can_dm_user(user):
    try:
        # Attempt to send a test DM, return true if possible
        await user.send("If you received this message, it means you have not disabled Direct Messages in our server. Please disable them and try to verify again!")
        log_message(f" DM Enabled Message successfully sent to {user}")
        return True
    except discord.Forbidden:
        # If not possible, return false
        return False

# View class to handle button interactions
class VerificationView(View):
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        verified_role_id = int(config["verified_role_id"]) # Converting role ID to an int because discord api requires that
        user_name = f"{interaction.user.name}"
        log_message(f" {button.custom_id} clicked by user {user_name}")

        try:
            # Next 4 sections are used for debugging and error fixing
            member = interaction.user
            log_message(f"[DEBUG] User: {member}")

            await interaction.response.defer()
            log_message(f"[DEBUG] Interaction deferred")

            guild = bot.get_guild(interaction.guild_id)
            log_message(f"[DEBUG] Guild: {guild.name}, {guild.id}")

            log_message(f"[DEBUG] Listing Server Roles:")
            for role in guild.roles:
                log_message(f"[DEBUG] {role.name}, {role.id}")

            # If statement that responds depending on whether the user has the DMs Open or Closed, responds appropriately
            if await can_dm_user(member):
                log_message(f" DM Enabled - User {user_name} has DMs enabled. Verification failed.")
            else:
                log_message(f" DM Disabled - Attempting to verify user {user_name}.")
                guild = bot.get_guild(interaction.guild_id)
                if guild:
                    log_message(f"[DEBUG] Guild found: {guild}")
                    verified_role = guild.get_role(verified_role_id)
                    if verified_role:
                        log_message(f"[DEBUG] Verified role found: {verified_role}")
                        await member.add_roles(verified_role)
                        log_message(f" Verification role ({verified_role}) added to user {user_name}")
                        await interaction.followup.send("You've been verified!", ephemeral=True)
                    else:
                        log_message("[ERROR] Verified role not found")
                else:
                    log_message("[ERROR] Guild not found")

        except Exception as e:
            print(f"[LOG][ERROR] An error occurred in verify_button_callback: {e}")
            await interaction.followup.send("An error occurred.", ephemeral=True)

# Function that sends the embed message with the Verify button
@bot.command()
@permissioned() # needs permission to use
async def send_embed(ctx):
    await ctx.message.delete() # deletes the !send_embed message
    user_name = f"{ctx.author.name}"
    # Creating the embed
    embed_color = config["embed_color"]
    embed = discord.Embed(
        title=config["embed_title"],
        description=config["embed_message"],
        color=discord.Color(embed_color),
    )
    embed.set_image(url="https://i.imgur.com/Ls6D7Sm.png") # Keep or replace image

    # Send the embed with the custom View
    view = VerificationView()
    await ctx.send(embed=embed, view=view)
    log_message(f" Embed Message successfully sent by {user_name}")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    user_name = f"{ctx.author.name}"
    if isinstance(error, commands.CheckFailure):
        log_message(f"[ALERT] User {user_name} tried to use a command lacking permission")
    else:
        await ctx.send(f"An error occurred: {error}")
        log_message(f"[ERROR] An error occurred with {user_name}: {error}")

# Run the bot
bot.run(config["token"])

