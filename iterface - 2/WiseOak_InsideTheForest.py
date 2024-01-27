import json, os.path
from tkinter import *
from errors import *
from tkVideoPlayer import TkinterVideo


class _Game():
    def __init__(self, MapName):
        self.valid = 0
        print(' == == ==  G  A  M  E      I  N  I  T  .  == == ==\n')

        with open('maps.json') as mapsconfig:
            maps = json.load(mapsconfig)
        if MapName in maps:
            with open(maps[MapName]['path']) as mapfile:
                print(f'initialization map {MapName}\n')
                self.world = Map(json.load(mapfile), self)
            self.mapconf = maps[MapName]
            self.valid = 1
        else:
            print(f'No map named "{MapName}" found. Check maps.json')

    def start(self):
        print('\n- B U I L D I N G   A P P -')
        self.fullscreenstatus = 0
        self.root = Tk()
        #self.root.resizable(0, 0)
        self.root.config(cursor='none')
        self.root.attributes('-topmost', 1)
        self.root.update()
        self.root.attributes('-topmost', 0)
        self.root.geometry('1920x1080')
        self.root.configure(bg='#000000')
        self.FullScreenSwitch()
        self.root.bind('<F11>', lambda a: self.FullScreenSwitch())
        self.root.update()
        self.videoplayer = TkinterVideo(self.root,height=1920,width=1080)
        self.videoplayer.load('intro.mp4')
        self.videoplayer.pack(expand=True, fill="both")
        self.videoplayer.bind("<<Loaded>>", lambda e: e.widget.config(width=1920, height=1080))
        self.videoplayer.bind('<<Ended>>', lambda a: self.body())
        self.videoplayer.play()
        self.root.mainloop()

    def body(self):
        self.root.config(cursor='arrow')
        self.videoplayer.pack_forget()
        self.menubg = PhotoImage(file='images/menubg.png')
        self.VLGM = PhotoImage(file='images/VLGmini.png')
        self.logoD = Label(self.root, image=self.menubg, bg='#1e382d')
        self.decframe = Frame(self.root, bg='#487361')
        self.logoD.place(x=0, y=0)
        self.decframe.pack(side='right', fill='y')
        self.menu()

    def menu(self, framedestroy=None):
        framedestroy.destroy() if framedestroy else 0
        self.logo = PhotoImage(file='images/logo.png')
        self.coframe = Frame(self.decframe, bg='#588572')
        self.logoL = Label(self.coframe, image=self.logo, bg='#588572')
        self.cobut = Frame(self.coframe, bg='#588572')
        self.GS_btn = self.menuButton(self.new_game, '  Начать игру  ', self.cobut, var=1)
        self.LD_btn = self.menuButton(self.savesc, 'Загрузить', self.cobut, var=2)
        self.ST_btn = self.menuButton(self.settings, 'Настройки', self.cobut, var=2)
        self.EX_btn = Button(self.cobut, text='Выход', font=('Bahnschrift', 20, 'bold'),
                      bd=3, fg='#ff0000', bg='#400000', relief='groove', activebackground='#100000',
                      activeforeground='#7a0000', command=self.root.destroy)
        self.EX_btn.bind('<Enter>', lambda a: self.EX_btn.config(bg='#200000'))
        self.EX_btn.bind('<Leave>', lambda a: self.EX_btn.config(bg='#400000'))
        self.logoVL = Button(self.coframe, image=self.VLGM, bg='#588572', bd=0, activebackground='#487361')
        self.logoVL.bind('<Enter>', lambda a: self.logoVL.config(bg='#689984'))
        self.logoVL.bind('<Leave>', lambda a: self.logoVL.config(bg='#588572'))
        
        self.coframe.pack(side='right', fill='y', padx=10)
        self.logoL.pack(side='top', padx=10, pady=30)
        self.cobut.pack(side='top', padx=30, pady=30)
        self.GS_btn.pack(anchor='n', pady=5, fill='x')
        self.LD_btn.pack(anchor='n', pady=5, fill='x')
        self.ST_btn.pack(anchor='n', pady=5, fill='x')
        self.EX_btn.pack(anchor='n', pady=5, fill='x')
        self.logoVL.pack(side='bottom', anchor='e')
        #self.world.runScene(self.mapconf['startscene'])

    def new_game(self):
        self.matcount = 0
        self.newimg = PhotoImage(file='images/newGame.png')
        self.cobut.destroy()
        self.sbut = Frame(self.coframe, bg='#487361')
        self.logoL.config(image=self.newimg)
        self.nameLabel = Label(self.sbut, bg='#487361', text='Введити вагша има', font=('Bahnschrift', 20, 'bold'), bd=3,
                               fg='#00ffd5')
        self.nameEntry = Entry(self.sbut, font=('Bahnschrift', 20, 'bold'), fg='#00ffd5', bg='#00473b', bd=3,
                               relief='sunken')
        self.warnL = Label(self.sbut, bg='#487361', text='', font=('Bahnschrift', 10, 'bold'),
                               fg='#ff5900')
        self.CM_btn = self.menuButton(self.nameValid, 'Подтвердить', self.sbut, var=2)
        self.BK_btn = self.menuButton(lambda: self.menu(self.coframe), 'Назад', self.sbut, var=2)

        self.sbut.pack(side='top', padx=30, pady=30)
        self.nameLabel.pack(anchor='n', pady=5, fill='x')
        self.nameEntry.pack(anchor='n', pady=5, padx=10, fill='x')
        self.warnL.pack(anchor='n', pady=5, padx=10, fill='x')
        self.CM_btn.pack(anchor='n', pady=5, padx=10, fill='x')
        self.BK_btn.pack(anchor='n', pady=5, padx=10, fill='x')

    def nameValid(self):
        v = self.nameEntry.get()
        llist = ['Нет. Нельзя использовать маты', 'Ты думаешь, что я ничего не вижу?', 'Хорош пытаться меня надурить.']
        if self.matcount in [0, 1, 2] and len(v) >= 4:
            self.warnL.config(text=llist[self.matcount])
            self.matcount += 1
        elif self.matcount == 3 and len(v) >= 4:
            self.warnL.config(text='Или... Блин, тут действительно ничего нет(')
            self.nameEntry.config(state='disabled', disabledforeground='#00ff00', disabledbackground='#004a00')
            self.CM_btn.config(fg='#45ff9f', bg='#005227', activeforeground='#74fcb5', activebackground='#009949')
            self.CM_btn.bind('<Enter>', lambda a: self.CM_btn.config(bg='#007337'))
            self.CM_btn.bind('<Leave>', lambda a: self.CM_btn.config(bg='#005227'))
            self.matcount += 1
        elif self.matcount == 4 and len(v) >= 4:
            self.world.local['name'] = v
            self.SCprep()
        else:
            self.warnL.config(text='тут ничего нет')

    def settings(self):
        self.setimg = PhotoImage(file='images/settings.png')
        self.coframe.destroy()
        self.setframe = Frame(self.decframe, bg='#588572')
        logoS = Label(self.setframe, image=self.setimg, bg='#588572')
        self.setbut = Frame(self.setframe, bg='#588572')
        self.RT_btn = self.menuButton(lambda: self.restart(),
                                      'Перезапуск', self.setbut, var=2)
        self.BK_btn = self.menuButton(lambda: self.menu(self.setframe),
                                      'Назад', self.setbut, var=2)

        self.setframe.pack(side='right', fill='y', padx=10)
        logoS.pack(side='top', padx=10, pady=30)
        self.setbut.pack(side='top', padx=30, pady=30)
        self.RT_btn.pack(anchor='n', pady=5, fill='x')
        self.BK_btn.pack(anchor='n', pady=5, fill='x')

    def savesc(self):
        self.savesimg = PhotoImage(file='images/saves.png')
        self.coframe.destroy()
        self.saveframe = Frame(self.decframe, bg='#588572')
        logoSV = Label(self.saveframe, image=self.savesimg, bg='#588572')
        self.savebut = Frame(self.saveframe, bg='#588572')
        self.BKS_btn = self.menuButton(lambda: self.menu(self.saveframe),
                                      'Назад', self.savebut, var=2)

        self.saveframe.pack(side='right', fill='y', padx=10)
        logoSV.pack(side='top', padx=10, pady=30)
        self.savebut.pack(side='top', padx=30, pady=30)
        self.BKS_btn.pack(anchor='n', pady=5, fill='x')

    def FullScreenSwitch(self):
        if self.fullscreenstatus:
            self.fullscreenstatus = 0
            self.root.attributes('-fullscreen', False)
        else:
            self.fullscreenstatus = 1
            self.root.attributes('-fullscreen', True)

    def menuButton(self, command, text, master, var=2):
        if var == 1:
            btn = Button(master, text=text, font=('Bahnschrift', 25, 'bold'),
                          bd=3, fg='#4eff45', bg='#193817', relief='groove', activebackground='#193817',
                          activeforeground='#aeffab', command=command)
            btn.bind('<Enter>', lambda a: btn.config(bg='#245221'))
            btn.bind('<Leave>', lambda a: btn.config(bg='#193817'))
            btn.bind('<FocusIn>', lambda a: btn.config(bg='#0000ff'))
            btn.bind('<FocusOut>', lambda a: btn.config(bg='#193817'))
            return btn
        if var == 2:
            btn = Button(master, text=text, font=('Bahnschrift', 20, 'bold'),
                          bd=3, fg='#45ffd1', bg='#193b37', relief='groove', activebackground='#193b37',
                          activeforeground='#a6fffc', command=command)
            btn.bind('<Enter>', lambda a: btn.config(bg='#224d47'))
            btn.bind('<Leave>', lambda a: btn.config(bg='#193b37'))
            btn.bind('<FocusIn>', lambda a: btn.config(bg='#0000ff'))
            btn.bind('<FocusOut>', lambda a: btn.config(bg='#193b37'))
            return btn

    def restart(self):
        self.root.destroy()
        self.start()

    #                           -- G A M E   L A U N C H E R --

    def SCprep(self):
        self.decframe.destroy()
        self.logoD.destroy()


class Map():
    def __init__(self, worldmap, game):
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
            scene.bindToMap(self, game)
            print(f'scene binded to Map.scenes: {name}')
        print('----------MAP BUILT!.\n')

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

    def bindToMap(self, world, game):
        self.scenes = world.scenes
        self.WorldMap = world
        self.game = game

    def run(self):
        print(f'              ===== Running scene "{self.name}" =====')
        if self.type == 'slide':
            for textInfo in self.text:
                txt = AdvancedText(textInfo, self.WorldMap)
            for action in self.action:
                self.runAction(action)
        elif self.type == 'choice':
            for textInfo in self.text:
                txt = AdvancedText(textInfo, self.WorldMap)
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


    # start
game = _Game('ITF')
input('s.')
game.start()
