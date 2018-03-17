# Kevin Rudd
A Discord moderation bot that you probably won't find useful. You're better off using another.

## How to run

### Windows:
1. [Download Python](https://www.python.org/downloads/)
2. Clone (or just download and extract) this repository.
3. Open `constants.example.py` and set all the variables as instructed. Then, rename the file to `constants.py` (you'll be prompted if you forget).
4. Run `setup.bat`. This will download all dependencies. The bot should automatically be launched once complete.
In subsequent runs, you only need to use `run.bat` (will not re-download everything).

## Feature Documentation (WIP)
> Default prefix is `/`. Commands are documented in a tree structure, with a bit of info on how to use them at the top of each section.
> The bot provides in-client help with the help command. It only lists the commands you can use.
>
> Example:  
> `/help server set`

* **help** *\[command\]* - Posts the default help message (for *command*, if present)

### Text Formatting
Anything that lets you set text supports some basic formatting.

| Placeholder     | Will be replaced with      | Example            |
|-----------------|----------------------------|--------------------|
| {{username}}    | User's name                | Frizbunny          |
| {{usertag}}     | User's tag (discriminator) | 1234               |
| {{userid}}      | User's ID                  | 140427255531831296 |
| {{usernick}}    | User's server nickname     | Rob                |
| {{servername}}  | Server's name              | Friz's Lab 2.0     |
| {{channelname}} | Current channel's name     | general            |
| {{channelid}}   | Current channel's ID       | 382849552018833411 |


### Core
> Only the bot owner can use these commands. Intended for debugging. Cannot be unloaded.
>
> Examples:  
> `/core get ip`  
> `/core reload commands`

* **core**
  * **restart** - Logs out the bot, waits 10 seconds, then restarts.
  * **kill** - Logs out the bot and stops the host batch script.
  * **get**
    * **extensions/cogs** - Posts a list of loaded extensions in chat.
    * **invite** - DMs you the bot's invite.
    * **ip** - DMs you the current host's public IP
  * **load** *\<cog\>* - Loads an extension (file name in `cogs/`)
  * **unload** *\<cog\>* - Removes an extension.
  * **reload** *\<cog\>* - Reloads an extension. If *cog* is `*` then all loaded extensions will be reloaded.
### Moderation
> Server owners are expected to be setting up the bot.  
> The owner must use `/server set role admin|mod|trusted <role name>` to grant a role permissions within the bot.
> 
> Examples:  
> `/server set role admin Guardian` would set *Guardian* as the admin role.  
> `/server set message leave Bye bye, {{user}}!` sets the leave message.

* **purge** \<amount\> - Deletes *amount* of messages from the channel. Max 200.
* **mute** *\<user\>* - Applies the server's mute role to the user. 
Does nothing if not set (see **server set role mute**)
* **kick** *\<user\>*
* **ban** *\<user\>*
* **server**
  * **set**
    * **channel**
      * **leave** *\<channel\>* - Posts user leave messages in the channel. (see `/server set message leave`)
      * **logs** *\<channel\>* - Sets a channel as the bot's log channel. 
      All commands used will be logged to this channel.
    * **message**
      * **leave** *\<content\>* - Sets the content of the leave message.
    * **role**
      * **admin** *\<role name\>* - Sets role for admin permissions
      * **mod** *\<role name\>* - Sets role for moderator permissions
      * **trusted** *\<role name\>* - Sets role for trusted user permissions
      * **mute** *\<role name\>* - 
    * **ghosting** *<true/false>* - Sets whether the bot will automatically delete messages sent by
    invisible members.

### Roles
> Adds some manual role management for users.
>
> A role must be added using `/addrole <rolename>` before a user can add it to themselves.
> If the role name has a space in it, it must be in quotes (eg. `/addrole "Rainbow 6"`).
> Users can now add this role with `/role Rainbow 6`
>
> A role can also have an alias to make it easier to assign. Just add the alias after the role name.
> `/addrole "Rainbow 6" r6` would allow users to get the role with `/role r6`

* **role** *\<role name\>* - Adds or removes a role from yourself.
* **addrole** *\<rolename\>* *\[alias\]* - Adds an assignable role.
* **roles** - DMs you a list of the server's roles.

### Fun
* **echo** *\<message\>* - Repeats any message sent in chat. *message* must be under 300 characters.
### Commands
> "Trusted" and above can create commands, anyone can use them.
>
> Examples:  
> `/commands add ping Pong!` would activate whenever a user types `/ping` and would reply with `Pong!`  
> `/commands add "friz github" https://github.com/Frizbunny/` would activate whenever `/friz github` is used.
* **commands** - Lists all server commands (if a child command isn't used)
  * **add** *\<command_name\> \<reply_message\>* - Adds a command to the server. *command_name* can be multiple words,
  but if so, must be in quotes. All text formatting is applied for the author of the message, ie. `{{username}}`
  becomes the command caller's username.
  * **delete** *\<command_name\>* - Deletes a server command.
### Minecraft
***WIP cog. No documentation available yet! Soon, hopefully. Maybe. One day<sup>tm</sup>.***