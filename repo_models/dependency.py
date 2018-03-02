
import json
from pprint import pprint


# data = json.load(open('dependency.json'))
# print(data)

data2 = json.load(open('config/folder_structure.json'))
# pprint(data2)

for _folder, _tree in data2.items():
    print(_folder, ":", type(_tree))

    if isinstance(_tree, type("")):
        print(_tree, " - Is Folder")


