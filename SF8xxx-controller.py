#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""
Main

Created on Sun May 19 12:03:18 2024

@author: drm1g20
"""

import Console as co
import sys

if len(sys.argv) > 1:
  co.Console(logfile=sys.argv[1])
else:
  co.Console()
