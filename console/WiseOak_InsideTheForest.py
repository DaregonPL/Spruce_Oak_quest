import json, os.path
from tkinter import *
from errors import *


class Map():
    def __init__(self, worldmap):
        self.items = worldmap['items']
        self.scenes = {}
        self.entrys = {}
        self.local = {}
        print('- S C E N E S   L O A D I N G -:\n')
        for scenedata in worldmap['scenes']:
            self.scenes[scenedata['name']] = Scene(scenedata)
            print(f'>scene loaded: "{scenedata["name"]}" in', self.scenes[scenedata['name']], 'with:')
            [print(name, ':', ' ' * (8 - len(name)) , value) for name, value in scenedata.items()]
            print('')
        
        print('\n- C O N N E C T I N G   S C E N E S -\n')
        for name, scene in self.scenes.items():
            scene.bindToMap(self)
            print(f'scene binded to Map.scenes: {name}')
        print('ready.\n')

    def runScene(self, scenename):
        if scenename in self.scenes:
            self.scenes[scenename].run()
        else:
            raise NonExistingSceneCalledError(scenename, self)
        


class Scene():
    def __init__(self, scenedata):
        self.name = scenedata['name']
        self.type = scenedata['type']
        if self.type == 'slide':
            self.text = scenedata['text']
            self.action = takeAction(scenedata['action'])
        elif self.type == 'choice':
            self.text = scenedata['text']
            self.vidgets = []
            for x in scenedata['vidgets']:
                vidget = {}
                if x['type'] == 'btn':
                    vidget['type'] = 'btn'
                    vidget['text'] = x['text']
                    vidget['action'] = takeAction(x['action'])
                elif x['type'] == 'entry':
                    vidget['type'] = 'entry'
                    vidget['id'] = x['id']
                    vidget['value'] = x['value']
                    vidget['minLenght'] = x['minLenght']
                else:
                    raise InvalidMapFormatError
                self.vidgets.append(vidget)
        elif self.type == 'logic':
            self.action = takeAction(scenedata['action'], multiple=True)
        else:
            raise InvalidMapFormatError

    def bindToMap(self, world):
        self.scenes = world.scenes
        self.WorldMap = world

    def run(self):
        print(f'              ===== Running scene "{self.name}" =====')
        if self.type == 'slide':
            for textInfo in self.text:
                txt = AdvancedText(textInfo, self.WorldMap)
                input(txt.getPrint())
            self.runAction(self.action[0])
        elif self.type == 'choice':
            for textInfo in self.text:
                txt = AdvancedText(textInfo, self.WorldMap)
                input(txt.getPrint())
            actbind, num = {}, 0
            for vidget in self.vidgets:
                if vidget['type'] == 'btn':
                    num += 1
                    txt = AdvancedText(vidget['text'], self.WorldMap)
                    print(f'{num}. {txt.getPrint()}')
                    actbind[str(num)] = vidget['action']
                elif vidget['type'] == 'entry':
                    while True:
                        a = input('entry>')
                        if vidget['value'] == 'int' and a.isdigit() and len(a) >= vidget['minLenght']:
                            break
                        elif vidget['value'] == 'any' and len(a) >= vidget['minLenght']:
                            break
                    self.WorldMap.entrys[vidget['id']] = a
                    print(a, f'Written to Map.entrys.{vidget["id"]}')
            print(f'actbind: {actbind}')
            while 1:
                ans = input()
                if ans in actbind:
                    break
                else:
                    print('wrong')
            self.runAction(actbind[ans][0])
        elif self.type == 'logic':
            for actiondata in self.action:
                self.runAction(actiondata)

    def runAction(self, action):
        print(f'running command {action}')
        if action['command'] == 'RunScene':
            if action['scene'] in self.scenes:
                self.scenes[action['scene']].run()
            else:
                print('Cannot access the scene', actions['scene'])
        elif action['command'] == 'Dublicate':
            fromV, toV = action['from'], action['to']
            exec('WM.' + toV['dir'] + '["' + toV['name'] + '"] = WM.' + fromV['dir'] + '["' + fromV['name'] + '"]', {'WM': self.WorldMap})


class AdvancedText():
    def __init__(self, textobject, worldmap):
        """Can edit tk vidgets and hold complex text"""
        self.worldmap = worldmap
        if type(textobject) == dict:
            self.text = textobject['text']
            self.color = '#000000' if 'color' not in textobject else textobject['color']
            self.tkinter = self.tk(self)
        elif type(textobject) == list:
            self.text = textobject

    class tk():
        def __init__(self, ATobject):
            """interaction with tkinter vidgets"""
            self.text = ATobject.text
            self.color = ATobject.color
            
        def configVidget(self, tkVidget):
            """Configurates tk vidgets(Text, Button, Label etc) with set properties"""
            tkVidget.config(text=self.text, fg=self.color)
            
    def getPrint(self):
        """Returns str"""
        if type(self.text) == str:
            return self.text
        elif type(self.text) == list:
            master = ''
            for x in self.text:
                if 'text' in x:
                    master += x['text']
                elif 'variable' in x:
                    if x['variable'] in self.worldmap.local:
                        master += self.worldmap.local[x['variable']]
                    else:
                        master += '-'
                else:
                    master += '-'
            return master
            


def takeAction(actionlist, multiple=False):
    """Takes a dict with correct elements. Returns edited dict"""
    if not multiple:
        actionlist = [actionlist]
    actions = []
    for action in actionlist:
        out = {}
        if action['command'] == 'RunScene':
            out['command'] = 'RunScene'
            out['scene'] = action['scene']
        elif action['command'] == 'GiveItem':
            out['command'] = 'GiveItem'
            out['item'] = {'Id': action['item']['Id'], 'count': action['item']['count']}
        elif action['command'] == 'RemoveItem':
            out['command'] = 'RemoveItem'
            out['item'] = {'Id': action['item']['Id'], 'count': action['item']['count']}
        elif action['command'] == 'Dublicate':
            out['command'] = 'Dublicate'
            out['from'] = {'dir': action['from']['dir'], 'name': action['from']['index']}
            out['to'] = {'dir': action['to']['dir'], 'name': action['to']['index']}
        else:
            raise InvalidMapFormat
        actions.append(out)
    return actions


with open('plot.json') as plot:
    ITFmap = json.load(plot)

world = Map(ITFmap)
world.runScene('start')
