import os, sys
ADDIN_DIR = os.path.dirname(os.path.abspath(__file__))
if ADDIN_DIR not in sys.path:
    sys.path.insert(0, ADDIN_DIR)

import lib.fusionbootstrap.bootstrap as bootstrap
# import importlib
# importlib.reload(bootstrap)

def run(context):
    bootstrap.run(context, __file__)

def stop(context):
    bootstrap.stop(context, __file__)
