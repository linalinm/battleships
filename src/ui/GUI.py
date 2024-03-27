import asyncio
import wx
from wxasync import WxAsyncApp, AsyncBind, StartCoroutine, AsyncShowDialog
import pathlib
from PIL import Image as PILImage
from board.MapRepository import MapRepository
from entities.Ship import Ship
from exceptions.ExceptionsEnum import MapException
from gamedataclasses.Coordinates import Coordinates
from random import randint

from players.Player import Player



class GUI(wx.Frame):

    def __init__(self, player : Player):
        self.player = player
        player.set_ui(self)
        self.app = WxAsyncApp()
        super().__init__(None,title="Battleships",size=(1200,900))
        self.assets_path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/assets/"

        self._friendly = {}
        self._enemy = {}

        self._enemy_ships = None
        self._friendly_ships = None
        self._ship_placement_options = None
        self._ship_placement_text = None
        self._ship_placement_box = None

        """
            self._ships will have elements with keys (x,y), and values ("start"/"end"/"middle", True/False - vertical/horisontal)
        """
        self._ships = {}

        self._seed1 = randint(0,100)
        self._seed2 = randint(0,100)

        self.SetMinSize([1200,900])
        self.SetMaxSize([1200,900])

        self.generate_enemy_side()
        self.generate_friendly_side()
        self.running = True

        StartCoroutine(self.update_self, self)

    def generate_image_for(self, coords : Coordinates, map : MapRepository):
        friendly = map == self.player.board.friendly
        if friendly:
            seed = self._seed1
        else:
            seed = self._seed2
        if map.get_tile(coords) == "sea" or map.get_tile(coords) == "unknown":
            img = PILImage.open(self.assets_path + "sea" + str((seed+coords.x*2+coords.y)%6) + ".png")
            if map.get_tile(coords) == "unknown":
                fog = PILImage.open(self.assets_path + "unknown.png")
                img = PILImage.blend(img, fog, 0.1)
        elif map.get_tile(coords) == "miss":
            img = PILImage.open(self.assets_path + "miss.png")
        elif map.get_tile(coords) == "hit" and not friendly:
            img = PILImage.open(self.assets_path + "miss.png")
            hit = PILImage.open(self.assets_path + "hit.png")
            img.paste(hit,(0,0),mask=hit)
        elif map.get_tile(coords) == "hit" or map.get_tile(coords) == "ship":
            img = PILImage.open(self.assets_path + "sea" + str((seed+coords.x*2+coords.y)%6) + ".png")
            if (coords.x,coords.y) in self._ships:
                ship_to_load = self._ships[(coords.x,coords.y)][0]
            else:
                ship_to_load = "middle"
            if ship_to_load == "start" or ship_to_load == "end":
                ship = PILImage.open(self.assets_path + "ship_end.png")
                if ship_to_load == "end":
                    ship = ship.rotate(180)
            else:
                ship = PILImage.open(self.assets_path + "ship_middle.png")
            if (coords.x,coords.y) in self._ships:
                if self._ships[(coords.x,coords.y)][1]:
                    ship = ship.rotate(270)
            img.paste(ship,(0,0),mask=ship)
            if map.get_tile(coords) == "hit":
                hit = PILImage.open(self.assets_path + "hit.png")
                img.paste(hit,(0,0),mask=hit)
        image = wx.Image(50,50)
        image.SetData(img.convert("RGB").tobytes())
        return image
    

    async def attack(self, event : wx.CommandEvent):
        name = event.GetEventObject().GetName()
        if not self.player.turn:
            return
        name = name[-2:]
        x = int(name[0:1])
        y = int(name[1:2])
        if not self.player.board.enemy.get_tile(Coordinates(x,y)) == "unknown":
            return
        self.player.attack(Coordinates(x,y))

    async def place(self, event : wx.CommandEvent):
        name = event.GetEventObject().GetName()
        if not self.player.placem:
            return
        name = name[-2:]
        x = int(name[0:1])
        y = int(name[1:2])
        new_id = len(self.player.board.friendly.get_ship_ids())
        vertical = self._ship_placement_box.IsChecked()
        ship = Ship(new_id,self.player.ship_to_place)
        try:
            self.player.place_ship(ship,Coordinates(x,y), vertical)
        except MapException:
            return
        if new_id in self.player.board.friendly.get_ship_ids():
            for i in range(ship.size):
                if i == 0:
                    self._ships[(x,y)] = ("start",vertical)
                elif i+1 == ship.size:
                    self._ships[(x,y)] = ("end",vertical)
                else:
                    self._ships[(x,y)] = ("middle",vertical)
                if vertical:
                    y = y+1
                else:
                    x = x+1

    def place_abs(self, ship, coords, vertical):
        x = coords.x
        y = coords.y
        for i in range(ship.size):
            if i == 0:
                self._ships[(x,y)] = ("start",vertical)
            elif i+1 == ship.size:
                self._ships[(x,y)] = ("end",vertical)
            else:
                self._ships[(x,y)] = ("middle",vertical)
            if vertical:
                y = y+1
            else:
                x = x+1


    def generate_enemy_side(self):
        fnt = wx.Font(15,family = wx.FONTFAMILY_MODERN, style = 0, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        self._enemy_ships = wx.StaticText(self,label="Enemy ships:\n", pos=(50,50),size=(200,400))
        self._enemy_ships.SetFont(fnt)
        for y in range(self.player.board.enemy.get_size().y):
            for x in range(self.player.board.enemy.get_size().x):
                posx = x * 50 + 50
                posy = y * 50 + 350
                image = self.generate_image_for(Coordinates(x,y),self.player.board.enemy)
                bmp = wx.Bitmap(image)
                button = wx.BitmapButton(self,bitmap=bmp,id=wx.ID_ANY,pos=(posx,posy),size=(49,49),style=wx.NO_BORDER,name=f"enemy{x}{y}")
                AsyncBind(wx.EVT_BUTTON,self.attack,button)
                button.Show()
                self._enemy[(x,y)] = button

    def generate_friendly_side(self):
        fnt = wx.Font(15,family = wx.FONTFAMILY_MODERN, style = 0, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        fnt2 = wx.Font(13,family = wx.FONTFAMILY_MODERN, style = 0, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        self._friendly_ships = wx.StaticText(self,label="Friendly ships:\n",pos=(650,50),size=(200,400))
        self._friendly_ships.SetFont(fnt)

        self._ship_placement_options = wx.Panel(self,id=wx.ID_ANY,pos=(950,100),size=(200,200))
        self._ship_placement_text = wx.StaticText(self._ship_placement_options,id=wx.ID_ANY,label="Ship to place:",pos=(10,10),size=(300,100))
        self._ship_placement_text.SetFont(fnt)
        self._ship_placement_box = wx.CheckBox(self._ship_placement_options,id=wx.ID_ANY,label="Place as vertical",pos=(10,110),size=(300,100))
        self._ship_placement_box.SetFont(fnt2)
        self._ship_placement_options.Hide()

        for y in range(self.player.board.enemy.get_size().y):
            for x in range(self.player.board.enemy.get_size().x):
                posx = x * 50 + 650
                posy = y * 50 + 350
                image = self.generate_image_for(Coordinates(x,y),self.player.board.friendly)
                bmp = wx.Bitmap(image)
                button = wx.BitmapButton(self,bitmap=bmp,id=wx.ID_ANY,pos=(posx,posy),size=(49,49),style=wx.NO_BORDER,name=f"friendly{x}{y}")
                AsyncBind(wx.EVT_BUTTON,self.place,button)
                button.Show()
                self._friendly[(x,y)] = button
    
    def update_enemy_side(self):
        if self._enemy_ships is not None:
            text = "Enemy ships:\n"
            for ship in self.player.board.enemy.get_ships():
                text = text + "\n" + ship.ship_type
                if ship.sunk:
                    text = text + "  - sunk"
            self._enemy_ships.SetLabelText(text)
        for key in self._enemy:
            self._enemy[key].SetBitmap(wx.Bitmap(self.generate_image_for(Coordinates(*key),self.player.board.enemy)))

    def update_friendly_side(self):
        if self._friendly_ships is not None:
            text = "Friendly ships:\n"
            for ship in self.player.board.friendly.get_ships():
                text = text + "\n" + ship.ship_type
                if ship.sunk:
                    text = text + "  - sunk"
            self._friendly_ships.SetLabelText(text)
        if self.player.placem and self._ship_placement_options is not None:
            self._ship_placement_options.Show()
            ship_to_place = "Ship to place:\n " + self.player.ship_to_place + "\n (size " + str(Ship(0,self.player.ship_to_place).size) + ")" 
            self._ship_placement_text.SetLabel(ship_to_place)
        if not self.player.placem:
            self._ship_placement_options.Hide()
        for key in self._friendly:
            self._friendly[key].SetBitmap(wx.Bitmap(self.generate_image_for(Coordinates(*key),self.player.board.friendly)))

    async def display_winner(self):
        popup = wx.Dialog(self,title="Game over!",size=(400,90))
        if self.player.won():
            text = "You won!"
        else:
            text = "You lost..."
        txt = wx.StaticText(popup,label=text,size=(400,90),style=wx.ALIGN_CENTRE)
        txt.SetFont(wx.Font(13,family = wx.FONTFAMILY_MODERN, style = 0, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT))
        await AsyncShowDialog(popup)
        while popup.IsShown():
            continue


    async def update_self(self):
        while self.running:
            self.update_enemy_side()
            self.update_friendly_side()
            if self.player.won() or self.player.lost():
                await self.display_winner()
                self.Close()
            await asyncio.sleep(0.2)


    async def main(self):
        self.Show()
        await self.app.MainLoop()
        self.running = False
