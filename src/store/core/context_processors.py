import random


quotes = [
    'gur gur behet mur',
    'no pain no gain',
    'e bardhe a jeshile',
]


def qotd(request):
    quote = random.choice(quotes)
    return {
        "quote": quote
    }
