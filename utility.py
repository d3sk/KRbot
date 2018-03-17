from discord import Message, Member


def format_string_with_message_data(string: str, message: Message) -> str:
    return string\
        .replace('{{username}}', message.author.name)\
        .replace('{{userid}}', str(message.author.id))\
        .replace('{{usertag}}', message.author.discriminator)\
        .replace('{{usernick}}', message.author.nick)\
        .replace('{{servername}}', message.guild.name)\
        .replace('{{channelname}}', message.channel.name)\
        .replace('{{channelid}}', str(message.channel.id))


def format_string_with_member_data(string: str, member: Member) -> str:
    return string\
        .replace('{{username}}', member.name)\
        .replace('{{userid}}', str(member.id))\
        .replace('{{usertag}}', member.discriminator)\
        .replace('{{usernick}}', member.nick)\
        .replace('{{servername}}', member.guild.name)\
