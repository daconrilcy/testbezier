from PIL import Image as Img, ImageTk
import wx
import os


# creer une premiere fenetre

img_path = os.path.abspath("../pict/la_naissance-de-venus-1024x643.png")

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Mon Frame Principal")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
                 pos=(0,0), size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title, pos, size, style, name)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.BLACK)
        button = wx.Button(self.panel, label="Push Me", pos=(50, 50))
        self.btnId = button.GetId()
        self.Bind(wx.EVT_BUTTON, self.OnButton, button)
        self.clic = 0
        bitmap = wx.Bitmap(img_path, type=wx.BITMAP_TYPE_PNG)
        self.SetSize(bitmap.GetWidth(), bitmap.GetHeight())

        self.bitmap = wx.StaticBitmap(self.panel, bitmap=bitmap)
        bx, by = self.panel.GetSize()
        print(bx, by)

    def OnButton(self, event):
        print("\nPanel FindWindowByID:")
        button = self.panel.FindWindowById(self.btnId)
        print("%s" % repr(button))
        self.clic += 1
        button.SetLabel('Lb chang '+str(self.clic))


if __name__ == "__main__":
    app = MyApp(False)
    displays = (wx.Display(i) for i in range(wx.Display.GetCount()))
    sizes = [display.GetGeometry().GetSize() for display in displays]
    print("d :", wx.Display(0).GetGeometry())
    print(app.frame.GetSize())
    print(app.GetVendorDisplayName())
    app.MainLoop()

