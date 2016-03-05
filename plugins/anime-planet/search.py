from motobot import command
from requests import get
from bs4 import BeautifulSoup


base_url = 'http://www.anime-planet.com'
results_cache = []


@command('a')
@command('anime')
def anime_search_command(bot, context, message, args):
    """ Search for an anime on anime-planet.com. """
    if len(args) > 1:
        return "Search result: {}".format(
            search_media(' '.join(args[1:]), 'anime'))
    else:
        return "Please supply a search term."


@command('m')
@command('manga')
def manga_search_command(bot, context, message, args):
    """ Search for a manga on anime-planet.com. """
    if len(args) > 1:
        return "Search result: {}".format(
            search_media(' '.join(args[1:]), 'manga'))
    else:
        return "Please supply a search term."


@command('u')
@command('user')
def user_search_command(bot, context, message, args):
    """ Search for a user on anime-planet.com. """
    format_str = "Search Results: {}"

    if len(args) > 1:
        return format_str.format(search_users(' '.join(args[1:])))
    else:
        return format_str.format(search_users(context.nick))


@command('c')
@command('char')
@command('character')
def character_search_command(bot, context, message, args):
    """ Search for a character on anime-planet.com. """
    if len(args) > 1:
        return "Search result: {}".format(
            search_characters(' '.join(args[1:])))
    else:
        return "Please supply a search term."


@command('rec')
@command('arec')
def anime_recommendations_search_command(bot, context, message, args):
    """ Search for an anime recommendation on anime-planet.com. """
    if len(args) > 1:
        return "Recommendations: {}".format(
            search_media(' '.join(args[1:]), 'anime', '/recommendations'))
    else:
        return "Please supply a search term."


@command('mrec')
def manga_recommendations_search_command(bot, context, message, args):
    """ Search for a manga recommendation on anime-planet.com. """
    if len(args) > 1:
        return "Recommendations: {}".format(
            search_media(' '.join(args[1:]), 'manga', '/recommendations'))
    else:
        return "Please supply a search term."


@command('top')
def top_anime_command(bot, context, message, args):
    """ Search for a user's lists on anime-planet.com. """
    format_str = "Top Anime: {}/lists"

    if len(args) > 1:
        return format_str.format(search_users(' '.join(args[1:])))
    else:
        return format_str.format(search_users(context.nick))


@command('tag')
@command('atag')
def atag_command(bot, context, message, args):
    """ Search for anime of the given tag. """
    tag = args[1:]
    return search_tag(tag, 'anime')


@command('mtag')
def mtag_command(bot, context, message, args):
    """ Search for manga of the given tag. """
    tag = args[1:]
    return search_tag(tag, 'manga')


def search_tag(tag, media):
    url = base_url + '/' + media + '/tags/' + '-'.join(tag)

    response = get(url)

    if response.history:
        return "Search results: {}".format(url)
    else:
        return "{} is not a valid tag.".format(' '.join(tag))


@command('more')
def more_command(bot, context, message, args):
    """ Return more results for the most recent anime-planet.com search. """
    try:
        return "More results: {}".format(results_cache.pop(0))
    except IndexError:
        return "There are no more results."


def search_media(term, type, append=''):
    global results_cache
    results_cache = []
    url = base_url + '/' + type + '/all'

    response = get(url, params={'name': term})

    if response.history:
        return response.url + append
    else:
        bs = BeautifulSoup(response.text)

        if bs.find('div', {'class': 'error'}, recursive=True):
            return "No results found."
        else:
            results = bs.find_all('li', {'class': 'card'}, recursive=True)
            results_cache = [base_url + result.find('a')['href'] + append
                             for result in results]
            return results_cache.pop(0)


def search_users(user):
    user = user.rstrip()
    url = base_url + '/users/' + user.lower()

    response = get(url)

    if response.history:
        return "No users found with name '{}'.".format(user)
    else:
        return response.url


def search_characters(character):
    global results_cache
    results_cache = []
    url = base_url + '/characters/all'

    response = get(url, params={'name': character})

    if response.history:
        return response.url
    else:
        bs = BeautifulSoup(response.text)

        if bs.find('div', {'class': 'error'}, recursive=True):
            return "No results found."
        else:
            results = bs.find_all('td', {'class': 'tableCharInfo'}, recursive=True)
            results_cache = [base_url + result.find('a')['href']
                             for result in results]
            return results_cache.pop(0)
