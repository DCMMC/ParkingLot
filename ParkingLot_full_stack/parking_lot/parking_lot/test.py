# https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
hyperLPR_path = os.path.join(parent_dir, 'HyperLPR')
sys.path.insert(0, hyperLPR_path)

import demo # noqa

demo.demo()
