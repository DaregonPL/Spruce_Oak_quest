import json, os.path
from tkinter import *

with open('plot.json') as plot:
    play = json.load(plot)

def location(location):
    """Returns PlotPoint item"""
    global play
    if location not in play:
        return None
    else:
        return PlotPoint(plot[location])

class PlotPoint():
    data = None
    
    def __init__(self, data):
        self.data = data

    def ways(self):
        """Returns Aviable ways set in plot file"""
        return self.data['ways']

    def text(self):
        """Returns Text set in plot file"""
        return self.data[text]

    def image(self):
        """Returns Background image set in plot file"""
        if 'image' in self.data:
            if os.path.exists(self.data['image']):
                return PhotoImage(file=f'images/{self.data["image"]}.png')
        return None
