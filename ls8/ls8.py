#!/usr/bin/env python3

"""Main."""

import sys

from cpu import *


cpu = CPU()
path = f'examples/{sys.argv[1]}'

cpu.load(path)
cpu.run()