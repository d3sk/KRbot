from discord import Message, Member


# def format_string_with_message_data(string: str, message: Message) -> str:
#     return string\
#         .replace('{{username}}', message.author.name)\
#         .replace('{{userid}}', str(message.author.id))\
#         .replace('{{usertag}}', message.author.discriminator)\
#         .replace('{{usernick}}', message.author.nick)\
#         .replace('{{servername}}', message.guild.name)\
#         .replace('{{channelname}}', message.channel.name)\
#         .replace('{{channelid}}', str(message.channel.id))

def __replace(string, replacement_dictionary):
    """
    :param string: Input to be manipulated
    :param replacement_dictionary: Key is a string that will be wrapped in {{ and }}. Value will replace the key.
    If the value is a list, subsequent items will be treated as fallbacks if the first item is None.
    :return: String with values replaced
    """
    for a, b in replacement_dictionary.items():
        if isinstance(b, list):
            for fallback in b:
                if fallback is not None:
                    string = string.replace('{{' + str(a) + '}}', fallback)
                    break
        else:
            string = string.replace('{{' + str(a) + '}}', str(b))
    return string


def format_string_with_message_data(string: str, message: Message):
    return __replace(string, {
        'username': message.author.name,
        'userid': message.author.id,
        'usertag': message.author.discriminator,
        'usernick': [message.author.nick, message.author.name],
        'servername': message.guild.name,
        'channelname': message.channel.name,
        'channelid': message.channel.id,
    })


def format_string_with_member_data(string: str, member: Member) -> str:
    return __replace(string, {
        'username': member.name,
        'userid': member.id,
        'usertag': member.discriminator,
        'usernick': member.nick,
        'servername': member.guild.name,
    })
