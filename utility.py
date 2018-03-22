from discord import Message, Member


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
                    string = string.replace('{{' + str(a) + '}}', str(fallback))
                    break
        else:
            if b is not None:
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
