import os
import random


video_path = "../videos"


class VideoSeq(object):
    def __init__(self):
        videos = os.listdir(video_path)
        self.videos = [i for i in videos if i.split('.')[-1] == "mp4"]
        random.shuffle(self.videos)
        self.step = 0
        self.length = len(self.videos)
        self.scores = [0 for _ in range(self.length)]

    def reset(self):
        self.step = 0
        self.scores = [0 for _ in range(self.length)]

    def move(self, evt):
        step = self.step + evt
        self.step = min(self.length-1, max(0, step))

    def play(self):
        video_name = self.videos[self.step]
        full_path = os.path.join(video_path, video_name)
        cmd = f"ffplay {full_path}"
        os.system(cmd)

    def scoring(self, mos):
        self.scores[self.step] = mos
        self.move(1)
        self.play()
