# Based off of March Madness Data on GitHub
# Source: https://github.com/danvk/march-madness-data
# Credit: Dan Vanderkam

from flask import Flask
import flask
import psycopg2 as p
import urllib
from bs4 import BeautifulSoup

from collections import defaultdict
import json
import re
import sys
import mwparserfromhell
from io import StringIO

app = Flask(__name__)

SEED_RE = re.compile(r'(\d+)')


def all_games(bracket):
    return [
        game
        for region in bracket['regions']
        for rnd in region
        for game in rnd
    ] + [
        game
        for rnd in bracket['finalfour']
        for game in rnd
    ]


def get_flattened_games(filenames):
    """Return a list of (game, year) tuples for all games in the JSON files."""
    game_years = []
    for path in filenames:
        bracket = json.load(open(path))
        year = bracket['year']
        game_years += [(game, year) for game in all_games(bracket)]
    return game_years


def extract_seed(seed):
    """Sometimes a seed is something like MW1. This extracts the 1."""
    m = SEED_RE.search(seed)
    assert m, seed
    return int(m.group(1))


def extract_year(path):
    m = re.search(r'(\d\d\d\d)', path)
    assert m, path
    return int(m.group(1))


def sum_for_game(game):
    return game[0]['seed'] + game[1]['seed']


def extract_source():
	url = "https://en.wikipedia.org/w/index.php?action=edit&title=2017_NCAA_Division_I_Men%27s_Basketball_Tournament"
	page = urllib.request.urlopen(url).read()

	soup = BeautifulSoup(page, 'html.parser')
	textareas = soup.select('textarea')
	assert len(textareas) == 1
	return textareas[0].text

NAME_RE = re.compile(r'\s*RD(\d)-(score|team|seed)(\d+)', re.I)


def dict_to_array(d):
    return [d[k] for k in sorted(d.keys())]


# The seeds in the first round are optional.
DEFAULTS16 = [
    ('RD1-seed01', '1'),
    ('RD1-seed02', '16'),
    ('RD1-seed03', '8'),
    ('RD1-seed04', '9'),
    ('RD1-seed05', '5'),
    ('RD1-seed06', '12'),
    ('RD1-seed07', '4'),
    ('RD1-seed08', '13'),
    ('RD1-seed09', '6'),
    ('RD1-seed10', '11'),
    ('RD1-seed11', '3'),
    ('RD1-seed12', '14'),
    ('RD1-seed13', '7'),
    ('RD1-seed14', '10'),
    ('RD1-seed15', '2'),
    ('RD1-seed16', '15')
]


def clear_style(text):
    """Remove ''' and '' from text."""
    return re.sub(r"''+", '', text)


def extract_template(template):
    # round # --> game # --> 0 or 1 --> {team|score|seed} --> value
    rounds = defaultdict(lambda: defaultdict(lambda: [{}, {}]))
    pairs = [
        (str(p.name), clear_style(p.value.strip_code().strip()))
        for p in template.params
    ]
    if template.name.matches('16TeamBracket'):
        pairs += DEFAULTS16
    for name, value in pairs:
        m = re.match(NAME_RE, name)
        if not m:
            continue
        round_num = int(m.group(1)) - 1
        field = m.group(2)
        slot = int(m.group(3)) - 1

        if field == 'seed' or field == 'score':
            value = int(extract_seed(value))

        game_num = slot // 2
        game_slot = slot % 2
        rounds[round_num][game_num][game_slot][field] = value

    return [dict_to_array(v) for v in dict_to_array(rounds)]


def extract_bracket(source, year):
    wikicode = mwparserfromhell.parse(source, skip_style_tags=True)
    templates = wikicode.filter_templates()
    bracket_templates = [
        t
        for t in templates
        if 'Bracket' in t.name and not t.name.matches('2TeamBracket')
    ]
    brackets = [extract_template(b) for b in bracket_templates]
    assert len(brackets) == 5  # four regions + final four
    for b in brackets[:4]:
        assert len(b) == 4  # R64, R32, Sweet Sixteen, Elite 8
    assert len(brackets[4]) == 2  # Final Four, Final

    # attach "round_of": 64, etc.
    for b in brackets[:4]:
        for i, rnd in enumerate(b):
            for game in rnd:
                for team in game:
                    team['round_of'] = 64 // (2 ** i)
    for i, rnd in enumerate(brackets[4]):
        for game in rnd:
            for team in game:
                team['round_of'] = 4 // (2 ** i)

    return {
        'year': year,
        'regions': brackets[:4],
        'finalfour': brackets[4]
    }



def main():
	source = extract_source()
	bracket = extract_bracket(source, 2017)

	io = StringIO()
	json.dump(bracket, io)
	temp = {}
	temp = json.loads(io.getvalue())
	# Keys: Region dictionary, region number, round number, matchup number
	print (temp["regions"][0][0][1])


if __name__ == '__main__':
    main()