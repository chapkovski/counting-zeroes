# from channels import Group
import json
from channels.sessions import channel_session
from .models import Player, Constants
from .views import update_seq_dict, get_seq, get_seqname
import random
from random import choice
from string import ascii_uppercase


def ws_message(message):
    # obtaining the message content
    jsonmessage = json.loads(message.content['text'])
    playerpk = str(jsonmessage['playerpk'])
    subsessionpk = str(jsonmessage['subsession'])
    seqname = str(jsonmessage['seq_name'])
    myplayer = Player.objects.get(pk=playerpk, subsession=subsessionpk)
    seqcounter = myplayer.seqcounter
    curplayerseq = json.loads(myplayer.seqdict)
    curplayerseq[seqname]['answer'] = jsonmessage['answer']
    seqdict = update_seq_dict(curplayerseq, myplayer.seqcounter+1)
    myplayer.seqdict = json.dumps(seqdict)
    myplayer.seqcounter += 1
    myplayer.save()

    message.reply_channel.send({
        "text": json.dumps({
            "newseq": seqdict[get_seqname(myplayer.seqcounter)],
            "seqcounter": myplayer.seqcounter,
        }),
    })


def ws_connect(message):
    pass

def ws_disconnect(message):
    pass
