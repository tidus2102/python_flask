#!/usr/bin/env python

from app import *
from app.models import *
from app.nodes.api.v1 import *
import os

os.environ['PYTHONINSPECT'] = 'True'

ctx = app.test_request_context()
ctx.push()
