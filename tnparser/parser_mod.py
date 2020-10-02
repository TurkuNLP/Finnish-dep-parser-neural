import os.path
import sys
import io
from . import parser_lib
import argparse
import traceback

pdir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "Parser-v2")
sys.path.insert(0, pdir)
from nparser.scripts.transfer_morpho import process_batch

def launch(args,q_in,q_out):
    try:
        parser=parser_lib.NetworkParserWrapper(args.model,args.parser_dir)
    except:
        traceback.print_exc()
        sys.stderr.flush()
    while True:
        jobid,txt=q_in.get()
        if jobid=="FINAL":
            q_out.put((jobid,txt))
            return
        try:
            conllu=parser.parse_text(txt)
            if args.process_morpho == True:
                conllu=process_batch(conllu, detransfer=True)
            q_out.put((jobid,conllu))
        except:
            traceback.print_exc()
            sys.stderr.flush()
            
argparser = argparse.ArgumentParser(description='Parse/Tag conllu text')
argparser.add_argument('--model', default="/usr/share/ParseBank/TinyFinnish-Stanford-model/Finnish-Tagger", help='Model. Default: %(default)s')
argparser.add_argument('--parser-dir', default=pdir, help='Parser. Default: ./%(default)s')
argparser.add_argument('--process_morpho', default=False, action='store_true', help='Run transfer_morpho script to return xpos and morpho to the correct fields')
