import wx
import wolframalpha
import wikipedia
import requests
import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 125)     # setting up new voice rate
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


engine.say('WELCOME, WHAT IS YOUR QUESTION')
engine.runAndWait()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                pos=wx.DefaultPosition, size=wx.Size(450, 100),
                style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                title="Ngutana")

        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel, label="Just Ngutana if you have something to ask")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(400, 30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def on_enter(self, event):
        ngutana = self.txt.GetValue()
        # ngutana = ngutana.lower()

        try:
            # wikipedia
            url = 'https://en.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'format': 'json',
                'titles': ngutana,
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
            }
            response = requests.get(url, params=params)
            data = response.json()
            page = next(iter(data['query']['pages'].values()))
            print(page['extract'])
            engine.say(page['extract'])
            engine.runAndWait()

            # Alternative by using the Wikipedia Library
            # print(wikipedia.summary(ngutana, sentences=2))
            # engine.say(wikipedia.summary(ngutana, sentences=2))
            # engine.runAndWait()

        finally:
            # Wolframalpha
            app_id = "JEJAY2-V3VXL6VXA4"
            client = wolframalpha.Client(app_id)
            result = client.query(ngutana)
            answer = next(result.results).text
            print(answer)
            engine.say(answer)
            engine.runAndWait()


if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
