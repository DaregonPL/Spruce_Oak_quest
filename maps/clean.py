import json
with open('ITF.json') as itf:
    a = json.load(itf)
with open('ITF.json', 'w') as itf:
    json.dump(a, itf, indent=4)
