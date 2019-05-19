# -*- coding: utf-8 -*-

import wx
import win32api
import sys, os

from videos import VideoSeq


APP_TITLE = "Subjective Experiment"
APP_ICON = "icon.ico"


class MainFrame(wx.Frame):
    """程序主窗口类，继承自wx.Frame"""

    def __init__(self, parent):
        """构造函数"""

        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((520, 320))
        self.Center()

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # introduction and choices
        font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        st_intro = wx.StaticText(self, -1, "Give your opinion score after watching the video", pos=(10, 80),
                                 size=(500, -1), style=wx.ALIGN_CENTER)
        st_score = wx.StaticText(self, -1, "5(excellent), 4(good), 3(fair）, 2（poor）, 1（bad）", pos=(10, 110), size=(500, -1),
                                 style=wx.ALIGN_CENTER)
        st_intro.SetFont(font)
        st_score.SetFont(font)

        # input/get user name
        st_id = wx.StaticText(self, -1, "Input user name: ", pos=(10, 20), size=(100, -1), style=wx.ALIGN_CENTER)
        tc_id = wx.TextCtrl(self, -1, '', pos=(120, 20), size=(100, -1), style=wx.TE_CENTER)
        st_id.SetFont(font)
        tc_id.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)

        # buttons for scores choices
        btn_1 = wx.Button(self, -1, '1', pos=(355, 150), size=(50, 25))
        btn_2 = wx.Button(self, -1, '2', pos=(295, 150), size=(50, 25))
        btn_3 = wx.Button(self, -1, '3', pos=(235, 150), size=(50, 25))
        btn_4 = wx.Button(self, -1, '4', pos=(175, 150), size=(50, 25))
        btn_5 = wx.Button(self, -1, '5', pos=(115, 150), size=(50, 25))

        btn_1.Bind(wx.EVT_BUTTON, self.OnScoreClicked)
        btn_2.Bind(wx.EVT_BUTTON, self.OnScoreClicked)
        btn_3.Bind(wx.EVT_BUTTON, self.OnScoreClicked)
        btn_4.Bind(wx.EVT_BUTTON, self.OnScoreClicked)
        btn_5.Bind(wx.EVT_BUTTON, self.OnScoreClicked)

        # text for progress bar
        self.progress_bar = "Current Progress : 0 / 0"
        self.st_bar = wx.StaticText(self, -1, pos=(10, 200), size=(500, -1), style=wx.ALIGN_CENTER)
        self.st_bar.SetFont(font)
        self.st_bar.SetLabel(self.progress_bar)

        # buttons for move
        btn_pre = wx.Button(self, -1, "Previous", pos=(100, 250), size=(100, 25))
        btn_next = wx.Button(self, -1, "Next", pos=(220, 250), size=(100, 25))
        btn_close = wx.Button(self, -1, "Exit", pos=(340, 250), size=(100, 25))

        btn_pre.Bind(wx.EVT_BUTTON, self.OnMoveClicked)
        btn_next.Bind(wx.EVT_BUTTON, self.OnMoveClicked)

        # 控件事件
        self.Bind(wx.EVT_BUTTON, self.OnClose, btn_close)

        # 系统事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # 其它变量
        self.user_id = None
        self.VideoSeq = None

    def OnEnterPressed(self, event):
        """输入用户名事件函数"""
        if self.user_id is None:
            self.user_id = event.GetString()
            self.VideoSeq = VideoSeq(self.user_id)
            self.VideoSeq.play()

            self.progress_bar = f"Current Progress : {self.VideoSeq.step+1} / {self.VideoSeq.length}"
            self.st_bar.SetLabel(self.progress_bar)

    def OnScoreClicked(self, event):
        """打分事件函数"""
        if self.user_id is None:
            self.NoUserWarning()
        else:
            btn = event.GetEventObject().GetLabel()
            # print("Label of pressed button = ", btn)
            self.VideoSeq.scoring(int(btn))
            exceed = self.VideoSeq.move(1)
            self.UpdateProgress()
            if exceed:
                self.LastOneWarning()

    def OnMoveClicked(self, event):
        """前后移动事件函数"""
        if self.user_id is None:
            self.NoUserWarning()
        else:
            btn = event.GetEventObject().GetLabel()
            move_dict = {"Previous": -1, "Next": 1}
            step = move_dict[btn]
            # print("Move Label of pressed button = ", btn)
            exceed = self.VideoSeq.move(step)
            self.UpdateProgress()
            if exceed:
                self.LastOneWarning()

    def OnClose(self, event):
        """关闭窗口事件函数"""
        dlg = wx.MessageDialog(None, "Comfirm exit?", "Operation prompt", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            if self.VideoSeq is not None:
                self.VideoSeq.finish()
            self.Destroy()

    def UpdateProgress(self):
        self.progress_bar = f"Current Progress : {self.VideoSeq.step + 1} / {self.VideoSeq.length}"
        self.st_bar.SetLabel(self.progress_bar)

    def NoUserWarning(self):
        dlg = wx.MessageDialog(None, "Please enter a username first ...", "No user name", wx.OK | wx.ICON_QUESTION)
        dlg.ShowModal()

    def LastOneWarning(self):
        dlg = wx.MessageDialog(None, "This is the last video ...", "No more videos", wx.OK | wx.ICON_QUESTION)
        dlg.ShowModal()


class MainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = MainFrame(None)
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
