# DiscordDMSecurity
A Discord.py bot that requires new users to disable Direct Messages in the server's privacy settings for their safety.

# Purpose
This is a Discord Verification Bot that requires the joining user to disable "Direct Messages" in the Privacy Settings of the server to verify and gain access to the entirety of the server

For communities and environments susceptible to various kinds of unwanted content, whether inappropriate or malicious, a solution like this is hardcore and ensures that YOU are taking a step in making their experience more secure.

This is perfect for web3 communities or younger communities where it's best to keep messages off. Whether the user decides to turn it back on afterward is in their hands, however, the blame can no longer fall on you (as if it should've anyway)

![option](https://github.com/bitbrink/DiscordDMSecurity/assets/74519953/c636e78e-e16b-4e1b-aee1-cdcdfbb7bafa)


# Use / Setup
Both hosting the bot and setting the server up are fairly simple

## Discord Server Setup
Have a channel named #verify for example that is only visible to users with **no roles**
Have the permissions set so no one can send messages in it
Have permissions set to the #verify channel so the "Verified" role **cannot** see or send messages in it. This removes the unnecessary channels after they are verified
Add permissions the "Verified" role to any of the actual channels you want users to be able to see

![image](https://github.com/bitbrink/DiscordDMSecurity/assets/74519953/fda8ec86-3cfe-4081-8a71-1f2ab227c82f)


## Hosting
This uses discord.py 2.3.2
Ensure you have Python installed

Download the files and store them wherever you plan to run the software. 
Configure the config.json to fit your server specifics
Run main.py
Use !send_embed in your #verify channel
Enjoy

![image](https://github.com/bitbrink/DiscordDMSecurity/assets/74519953/1a456a74-a104-42f3-b8bb-a4829540b190)

# Other
Feel free to change this however you'd like to fit your needs, or feel free to create issues/pull requests for fixes or features you would like added.
