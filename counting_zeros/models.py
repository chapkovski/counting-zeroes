from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import json
from django import forms

author = 'Filipp Chapkovskii, UZH'

doc = """
Channels example
"""


class Constants(BaseConstants):
    name_in_url = 'channel_test'
    players_per_group = None
    num_rounds = 1
    seqsize = 10
    seqthreshold = 0.5


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for p in self.get_players():
            p.seqdict = json.dumps({})

class Group(BaseGroup):
    pass



class Player(BasePlayer):
    seqdict = models.TextField()
    seqcounter = models.IntegerField(initial=0)
