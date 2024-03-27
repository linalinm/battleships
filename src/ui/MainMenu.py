import wx


class MainMenu(wx.Frame):

    def __init__(self):


        self.app = wx.App()
        super().__init__(None,id=wx.ID_ANY,title="Battleships Main Menu", size=(500,700))

        self.SetMaxSize((500,700))
        self.SetMinSize((500,700))

        self._state = "main"
        self.fnt = wx.Font(15,family = wx.FONTFAMILY_MODERN, style = 0, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)

        self._easy_button = None
        self._normal_button = None
        self._back_button = None
        self._host_button = None
        self._connect_button = None
        self._singleplayer_button = None
        self._multiplayer_button = None
        self._exit_button = None

        self.generate_main_menu()
        self.generate_singleplayer_menu()
        self.generate_multiplayer_menu()

        self.switch_to_main_menu(None)
        self.Show()

    def switch_to_main_menu(self, event):
        self._easy_button.Hide()
        self._normal_button.Hide()
        self._back_button.Hide()
        self._host_button.Hide()
        self._connect_button.Hide()

        self._singleplayer_button.Show()
        self._multiplayer_button.Show()
        self._exit_button.Show()


    def switch_to_singleplayer_menu(self, event):
        self._singleplayer_button.Hide()
        self._multiplayer_button.Hide()
        self._exit_button.Hide()

        self._easy_button.Show()
        self._normal_button.Show()
        self._back_button.Show()

    def switch_to_multiplayer_menu(self, event):
        self._singleplayer_button.Hide()
        self._multiplayer_button.Hide()
        self._exit_button.Hide()

        self._host_button.Show()
        self._connect_button.Show()
        self._back_button.Show()

    def exit(self, event):
        self._state = "exit"
        self.app.ExitMainLoop()

    def easy(self, event):
        self._state = "easy"
        self.app.ExitMainLoop()

    def normal(self, event):
        self._state = "normal"
        self.app.ExitMainLoop()

    def host(self, event):
        self._state = "host"
        self.app.ExitMainLoop()

    def connect(self, event):
        self._state = "connect"
        popup = wx.Dialog(self,title="IP to connect to:",size=(200,105))
        txt = wx.TextCtrl(popup,size=(180,30),pos=(10,10))
        popup.Bind(wx.EVT_TEXT,self.set_ip,txt)
        button = wx.Button(popup,size=(180,30),pos=(10,40),label="Connect")
        popup.Bind(wx.EVT_BUTTON,self.ret_connect,button)
        popup.Show()

    def set_ip(self, event : wx.CommandEvent):
        self._state = "connect " + event.GetString()

    def ret_connect(self, event):
        self.app.ExitMainLoop()

    def generate_main_menu(self):
        self._singleplayer_button = wx.Button(self,id=wx.ID_ANY,label="Singleplayer",pos=(50,40),size=(400,200),style=wx.CENTRE)
        self._multiplayer_button = wx.Button(self,id=wx.ID_ANY,label="Multiplayer",pos=(50,250),size=(400,200),style=wx.CENTRE)
        self._exit_button = wx.Button(self,id=wx.ID_EXIT,label="Exit",pos=(50,460),size=(400,200),style=wx.CENTRE)

        self._singleplayer_button.Hide()
        self._multiplayer_button.Hide()
        self._exit_button.Hide()

        self._singleplayer_button.SetFont(self.fnt)
        self._multiplayer_button.SetFont(self.fnt)
        self._exit_button.SetFont(self.fnt)

        self._singleplayer_button.Bind(wx.EVT_BUTTON,self.switch_to_singleplayer_menu)
        self._multiplayer_button.Bind(wx.EVT_BUTTON,self.switch_to_multiplayer_menu)
        self._exit_button.Bind(wx.EVT_BUTTON,self.exit)

        

    def generate_singleplayer_menu(self):
        self._easy_button = wx.Button(self,id=wx.ID_ANY,label="Easy",pos=(50,40),size=(400,200),style=wx.CENTRE)
        self._normal_button = wx.Button(self,id=wx.ID_ANY,label="Normal",pos=(50,250),size=(400,200),style=wx.CENTRE)
        self._back_button = wx.Button(self,id=wx.ID_ANY,label="Back",pos=(50,460),size=(400,200),style=wx.CENTRE)

        self._easy_button.Hide()
        self._normal_button.Hide()
        self._back_button.Hide()

        self._easy_button.SetFont(self.fnt)
        self._normal_button.SetFont(self.fnt)
        self._back_button.SetFont(self.fnt)

        self._easy_button.Bind(wx.EVT_BUTTON,self.easy)
        self._normal_button.Bind(wx.EVT_BUTTON,self.normal)
        self._back_button.Bind(wx.EVT_BUTTON,self.switch_to_main_menu)

        

    def generate_multiplayer_menu(self):
        self._host_button = wx.Button(self,id=wx.ID_ANY,label="Host",pos=(50,40),size=(400,200),style=wx.CENTRE)
        self._connect_button = wx.Button(self,id=wx.ID_ANY,label="Connect",pos=(50,250),size=(400,200),style=wx.CENTRE)

        self._host_button.Hide()
        self._connect_button.Hide()

        self._host_button.SetFont(self.fnt)
        self._connect_button.SetFont(self.fnt)

        self._host_button.Bind(wx.EVT_BUTTON,self.host)
        self._connect_button.Bind(wx.EVT_BUTTON,self.connect)


    def main(self):
        self.app.MainLoop()
        self.Close()
        return self._state