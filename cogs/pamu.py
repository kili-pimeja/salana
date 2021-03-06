import discord
from discord.ext import commands, tasks
import json
import os
import re
from emoji import demojize, emojize
import random
from math import ceil
import asyncio

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(pamu(client))

class pamu(commands.Cog, name='PA MU'):

    '''A module for pa mu servers.'''

    def __init__(self, client):
        self.client = client
        self.pamu_dict = {
            'ja': 'ja:\n**NOUN:** question, what\n**VERB:** request, ask for, ask\n**MODIFIER:** what, which',
            'jali': 'jali:\n**NOUN:** front, in line of sight, vertical surface\n**VERB:** put in front, prioritize, show\n**MODIFIER:** in front, relating to the front or a vertical surface',
            'jalu': 'jalu:\n**NOUN:** time, hour, day\n**VERB:** schedule\n**MODIFIER:** timely, daily, relating to time, new',
            'ju': 'ju:\n**NOUN:** living thing, person, animal, plant\n**VERB:** grow, nourish, birth, be conscious\n**MODIFIER:** alive, active',
            'juli': 'juli:\n**NOUN:** ground, space beneath\n**VERB:** defeat\n**MODIFIER:** humble, downwards',
            'ka': 'ka:\n**NOUN:** group, collection\n**VERB:** multiply, group together\n**MODIFIER:** many, a lot, general emphasis or strengthening',
            'kalu': 'kalu:\n**NOUN:** destruction, war\n**VERB:** divide, break, wage war on\n**MODIFIER:** broken, divided, split',
            'ki': 'ki:\n**NOUN:** nothing\n**VERB:** annihilate, make into nothing\n**MODIFIER:** none, not, no, opposite',
            'kila': 'kila:\n**NOUN:** hole, opening\n**VERB:** make into hole, throw away, get rid of\n**MODIFIER:** removed, relating to holes',
            'ku': 'ku:\n**NOUN:** the number one\n**VERB:** make one, unify\n**MODIFIER:** one, exception, only',
            'kuli': 'kuli:\n**NOUN:** liquid, water, soft thing\n**VERB:** liquify, water, make soft\n**MODIFIER:** soft, watery, liquid',
            'kula': 'kula:\n**NOUN:** border, skin, clothing, barrier\n**VERB:** wrap around oneself, make into a border or barrier\n**MODIFIER:** regarding a border or barrier',
            'ma': 'ma:\n**NOUN:** air, gas, spirit\n**VERB:** breathe, vaporize\n**MODIFIER:** intangible, supernatural, spiritual',
            'mali': 'mali:\n**NOUN:** money, value, exchange, wealth\n**VERB:** exchange, buy, sell\n**MODIFIER:** rich, monetary, of value',
            'mi': 'mi:\n**NOUN:** same thing\n**VERB:** equalize\n**MODIFIER:** same, equal',
            'mila': 'mila:\n**NOUN:** origin, reason\n**VERB:** come from\n**MODIFIER:** original',
            'mu': 'mu:\n**NOUN:** communication, speech, word\n**VERB:** communicate, talk, speak\n**MODIFIER:** relating to communication',
            'muli': 'muli:\n**NOUN:** gift\n**VERB:** give, set, send, emit\n**MODIFIER:** relating to or similar to a gift',
            'na': 'na:\n**NOUN:** happiness, goodness\n**VERB:** fix, make well, cheer up\n**MODIFIER:** good, desirable, happy',
            'ni': 'ni: verb marker',
            'nila': 'nila:\n**NOUN:** truth, existence, continuum\n**VERB:** exist, wait\n**MODIFIER:** true, existing, continuing',
            'nu': 'nu: sentence marker',
            'nuli': 'nuli:\n**NOUN:** possibility, something\n**VERB:** allow, make possible\n**MODIFIER:** uncertain',
            'nulu': 'nulu:\n**NOUN:** knowledge\n**VERB:** know, realize, learn\n**MODIFIER:** relating to knowledge, known',
            'pa': 'pa:\n**NOUN:** method, way, path, doctrine, direction\n**VERB:** put on a path, make into a way or path\n**MODIFIER:** doctrinal, relating to a method, directional',
            'pala': 'pala:\n**NOUN:** ownership, guidance, rule\n**VERB:** receive, own, hold, have charge over, rule, lead, guide\n**MODIFIER:** owned, received, ruled, of the head',
            'pi': 'pi:\n**NOUN:** inside, container\n**VERB:** put inside, hide, eat\n**MODIFIER:** inside, within, hidden',
            'pila': 'pila:\n**NOUN:** sense, sight, vision, touch, hearing\n**VERB:** sense, see, hear, feel, listen\n**MODIFIER:** sensory, relating to the senses',
            'pu': 'pu: object marker',
            'puli': 'puli:\n**NOUN:** light, sunlight\n**VERB:** shine, emit light, remove color from\n**MODIFIER:** bright, white, regarding light',
            'sa': 'sa: context marker',
            'sala': 'sala:\n**NOUN:** tool, instrument, usage\n**VERB:** use\n**MODIFIER:** useful',
            'si': 'si: subject marker',
            'sili': 'sili:\n**NOUN:** beginning, coming, arrival\n**VERB:** open, start, begin, become, arrive\n**MODIFIER:** beginning, becoming',
            'silu': 'silu:\n**NOUN:** something important or big\n**VERB:** enlarge\n**MODIFIER:** large, important',
            'su': 'su:\n**NOUN:** desire, obligation, attempt\n**VERB:** need, try, want\n**MODIFIER:** needful, desired',
            'sula': 'sula:\n**NOUN:** heat\n**VERB:** heat, make hot\n**MODIFIER:** hot, spicy',
            'ta': 'ta:\n**NOUN:** proximity, area around\n**VERB:** bring near\n**MODIFIER:** near, close, neighboring',
            'tali': 'tali:\n**NOUN:** building, structure, creation\n**VERB:** build, make\n**MODIFIER:** created, made, built',
            'tu': 'tu:\n**NOUN:** everything, universe\n**VERB:** make whole\n**MODIFIER:** all, every, each',
            'tula': 'tula:\n**NOUN:** stick, rod\n**VERB:** make into a stick, make thin, make long\n**MODIFIER:** thin, skinny, long',
            'wa': 'wa:\n**NOUN:** solid, something hard or strong\n**VERB:** solidify, harden, strengthen\n**MODIFIER:** hard, solid, strong',
            'wali': 'wali:\n**NOUN:** place, land, city, country, house, property\n**VERB:** make into a place or country\n**MODIFIER:** regarding a place, land, etc.',
            'wi': 'wi: modifier regrouping marker',
            'wilu': 'wilu:\n**NOUN:** movement\n**VERB:** move\n**MODIFIER:** moving, regarding movement'
        }

    async def ifpamu(self, ctx):
        if ctx.guild is None:
            return False
        return config[str(ctx.guild.id)]['tp'] is None

    async def pamu_check(self, msg):
        msg= str(msg)
        step1 = re.sub(r'\|\|[^\|]+\|\||\s', '', msg) #removes between spoiler tags and whitespace characters
        step2 = demojize(step1) #textifies emojis
        step3 = re.sub(r':[^ ]+:', '', step2) #deletes emojis
        step4 = re.sub('([mnptksljw][uia])', '', step3) #deletes all possible syllables
        if step4 == '':
            return True
        else:
            return False

    @commands.command(aliases=['check_for_pamu', 'cfpm'])
    async def pamucheck(self, ctx, *, text):
        """Checks if the input text is valid in pa mu or not. It does so by first removing anything behind spoiler bars and any whitespace characters, then removing emojis, and then it runs the text through all possible syllables in pa mu."""
        if not await self.ifpamu(ctx):
            return
        if await self.pamu_check(text):
            await ctx.send("pa mu confirmed. :sleepy:")
        else:
            await ctx.send(":rotating_light: Not pa mu! :rotating_light:")