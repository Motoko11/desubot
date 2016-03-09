from motobot import match
from requests import get


def format_duration(duration):
    x = i = h = m = s = 0

    for c in duration:
        if c.isdigit():
            x = x * 10 + int(c)
            i += 1
        elif c == 'H':
            h = x
            i = x = 0
        elif c == 'M':
            m = x
            i = x = 0
        elif c == 'S':
            s = x
            i = x = 0

    time = '' if h == 0 else '{}:'.format(h)
    return time + "{:02d}:{:02d}".format(m, s)


@match(r'((youtube\.com\/watch\?\S*v=)|(youtu\.be/))([a-zA-Z0-9-_]+)')
def youtube_match(bot, context, message, match):
    invalid_channels = ['#animu', '#bakalibre']
    if context.channel in invalid_channels:
        return None
    vid = match.group(4)
    params = {
        'id': vid,
        'part': 'contentDetails,snippet',
        'key': bot.youtube_api_key
    }
    response = get('https://www.googleapis.com/youtube/v3/videos', params=params, timeout=5)
    if response.status_code == 400:
        return "{}: invalid id".format(context.nick)
    video = response.json()['items'][0]
    title = video['snippet']['title']
    duration = format_duration(video['contentDetails']['duration'])
    return "{}'s video: {} - {}".format(
        context.nick, title, duration
    )
