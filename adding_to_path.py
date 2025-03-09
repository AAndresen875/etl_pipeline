# imports
import sys
import os

# getting current state of path:
print("current sys path:", sys.path)

# getting the repo path:
repo_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
print("path to this repo: ", repo_path)

# adding the repo path to the sys path:
if repo_path not in sys.path:
    sys.path.append(repo_path)
print(sys.path)
