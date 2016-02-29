from motobot import command, sink, Notice, Priority, Eat, Action, split_response
from random import choice, uniform
from re import compile, IGNORECASE


@sink(priority=Priority.lowest)
def regex_sink(bot, context, message):
    responses = []

    for pattern, reply, extra in context.database.get([]):
        match = pattern.search(message)
        if match:
            reply = parse_reply(reply, extra, match, context.nick)
            if reply is not None:
                responses.append(reply)

    return responses


def parse_reply(reply, extra, match, nick):
    chance = float(extra.get('chance', 100))
    if chance >= uniform(0, 100):
        reply = choice(reply.split('|'))

        tokens = [
            ('{nick}', nick)
        ]
        for token, replace in tokens:
            reply = reply.replace(token, replace)

        for i, group in enumerate(match.groups()):
            reply = reply.replace('${}'.format(i), group)

        if reply.startswith('/me '):
            reply = (reply[4:], Action)
        return reply


@command('re', priority=Priority.lower, hidden=True)
def regex_command(bot, context, message, args):
    """ Manage regex matches on bot.

    Valid arguments are: 'add', 'del', 'set', and 'show'.
    'add' usage: re add [pattern] <=> [response];
    'del' usage: re del [pattern];
    'set' usage: re set [pattern] <=> [attribute] [value];
    'show' usage: re show [pattern];
    If pattern is not specified, a list of triggers will be returned.
    """
    arg = args[1].lower()
    if arg == 'add':
        response = add_regex(' '.join(args[2:]), context.database)
    elif arg == 'del' or arg == 'rem':
        response = rem_regex(' '.join(args[2:]), context.database)
    elif arg == 'show':
        search = ' '.join(args[2:])
        if search != '':
            response = show_patterns(context.database, search)
        else:
            response = show_triggers(context.database)
    elif arg == 'set':
        response = set_attrib(' '.join(args[2:]), context.database)
    else:
        response = "Error: Unrecognised argument."

    return response, Eat, Notice(context.nick)


def match_pattern(string, pattern):
    return string.lower() == pattern.pattern.lower() \
        or pattern.search(string) is not None


def add_regex(string, database):
    response = None
    try:
        pattern, reply = map(str.strip, string.split('<=>', 1))
        patterns = database.get([])
        patterns.append((compile(pattern, IGNORECASE), reply, {}))
        database.set(patterns)
        response = "Pattern added successfully."
    except ValueError:
        response = "Error: Invalid syntax."
    return response


def rem_regex(string, database):
    remove = []
    response = "No patterns matched the string."
    patterns = database.get([])

    for pattern, reply, extra in patterns:
        if match_pattern(string, pattern):
            remove.append((pattern, reply, extra))

    for entry in remove:
        patterns.remove(entry)

    if remove != []:
        response = "Pattern(s) matching the string have been removed."
        database.set(patterns)

    return response


def show_patterns(database, string):
    responses = []

    for pattern, reply, extra in database.get([]):
        if match_pattern(string, pattern):
            extras = []
            for x, y in extra.items():
                extra = '{}: {};'.format(x, y)
                extras.append(extra)
            extras = ["None"] if extras == [] else extras
            reply = "{} - {} - {}".format(
                pattern.pattern, reply, ' '.join(extras))
            responses.append(reply)

    if responses == []:
        responses = "There are no patterns that match the given string."

    return responses


def show_triggers(database):
    patterns = database.get(None)

    if patterns is None:
        responses = "There are no patterns currently saved."
    else:
        triggers = map(lambda x: x[0].pattern, patterns)
        responses = split_response(triggers, "Triggers: {};")

    return responses


def set_attrib(string, database):
    response = None
    try:
        query, trailing = map(str.strip, string.split('<=>', 1))
        try:
            attrib, val = trailing.split(' ')
        except ValueError:
            attrib = trailing
            val = None
        patterns = database.get([])
        response = "No patterns matched the given string."

        for pattern, reply, extra in patterns:
            if match_pattern(query, pattern):
                response = "Attribute set on matching patterns successfully."
                if val is None:
                    if attrib in extra:
                        extra.pop(attrib)
                else:
                    extra[attrib] = val
        database.set(patterns)
    except ValueError:
        response = "Error: Invalid syntax."
    return response
