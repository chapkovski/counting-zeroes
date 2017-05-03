from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import collections
import json


def get_seq(size=Constants.seqsize, threshold=Constants.seqthreshold):
    seq = [random.random() for i in range(size)]
    seq = [0 if i < threshold else 1 for i in seq]
    return seq


def get_seqname(id):
    return 'seq' + str(id)


def update_seq_dict(seqdict, seq_id):
    seqname = get_seqname(seq_id)
    if seqname not in seqdict:
        seq = get_seq()
        corranswer = Constants.seqsize - sum(seq)
        seqdict[seqname] = {'seq_to_show': seq,
                            'corranswer': None,
                            'answer': None,
                            'name': str(seqname)}
    return seqdict


class Introduction(Page):
    timeout_seconds = 20

    def vars_for_template(self):
        seqdict = json.loads(self.player.seqdict)
        seqdict = update_seq_dict(seqdict, self.player.seqcounter)
        self.player.seqdict = json.dumps(seqdict)
        return {'seq': json.dumps(seqdict[get_seqname(self.player.seqcounter)])}


class Results(Page):
    ...

    def vars_for_template(self):
        seqdict = json.loads(self.player.seqdict)
        keys = [k for k, v in seqdict.items() if not v['answer']]
        for x in keys:
            del seqdict[x]
        for key, value in seqdict.items():
            seqdict[key]['corranswer'] = Constants.seqsize - sum(value['seq_to_show'])
            seqdict[key]['iscorrect'] = seqdict[key]['corranswer'] == int(seqdict[key]['answer'])
            seqdict[key]['seq_to_show'] = ''.join(str(e) for e in value['seq_to_show'])
        self.player.sumcorrect = sum([v['iscorrect'] for k, v in seqdict.items()])
        
        self.player.payoff = self.player.sumcorrect * \
            Constants.price_per_correct_answer
        return {'seq': seqdict}

page_sequence = [
    Introduction,
    Results,
]
