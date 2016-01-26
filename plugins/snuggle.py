from motobot import command, Action, match


@command('snuggle')
def snuggle_command(bot, database, nick, channel, message, args):
    """ Snuggle your favourite person. """
    response = ''
    if len(args) > 1:
        response = 'snuggles ' + ' '.join(args[1:])
    else:
        response = 'snuggles ' + nick

    return response, Action


@command('unsnuggle')
def unsnuggle_command(bot, database, nick, channel, message, args):
    """ Tell someone the cold hard truth. """
    return "Go ahead and call the cops... You can't be unsnuggled!"


@command('pat')
def pat_command(bot, database, nick, channel, message, args):
    """ Pat someone who deserves it. """
    response = ''
    if len(args) > 1:
        response = 'pat pats ' + ' '.join(args[1:])
    else:
        response = 'pat pats ' + nick

    return response, Action


@command('pet')
def pet_command(bot, database, nick, channel, message, args):
    """ Pet someone who really deserves it. """
    response = ''
    if len(args) > 1:
        response = 'pets ' + ' '.join(args[1:])
    else:
        response = 'pets ' + nick

    return response, Action


@match(r'\*(.+? )pets desubot')
def purr_match(bot, database, nick, channel, message, match):
    return 'purrs', Action


@match(r'\*(?:.+? )(kicks|pokes|hits|bites) desubot')
def bite_match(bot, database, nick, channel, message, match):
    return 'bites ' + nick + (' back' if match.group(1) == 'bites' else ''), Action
