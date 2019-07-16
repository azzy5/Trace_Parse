try:
    import sys
except ImportError:
    print('sys : Module not found.  ')

try:
    import os
except ImportError:
    print('os : Module not found')

try:
    from flask import *
except ImportError:
    print('flask : Module not found')

try:
    import json
except ImportError:
    print('json : library not found')

try:
    import requests
except ImportError:
    print('requests : library not found')

try:
    import urllib
except ImportError:
    print('urllib : library not found')

try:
    import io
except ImportError:
    print('io : library not found')
