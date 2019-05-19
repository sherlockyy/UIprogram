import os
import random
import subprocess


video_path = "../videos"


class VideoSeq(object):
    def __init__(self, user_id):
        self.user = user_id
        videos = os.listdir(video_path)
        self.videos = [i for i in videos if i.split('.')[-1] == "mp4"]
        random.shuffle(self.videos)
        self.step = 0
        self.length = len(self.videos)
        self.scores = [0 for _ in range(self.length)]
        self.sp = None

    def reset(self):
        self.step = 0
        self.scores = [0 for _ in range(self.length)]

    def move(self, evt):
        exceed = False
        if self.step == self.length-1 and evt == 1:
            exceed = True
        step = self.step + evt
        self.step = min(self.length-1, max(0, step))
        self.play()
        return exceed

    def play(self):
        if self.sp is not None:
            self.sp.kill()
        video_name = self.videos[self.step]
        full_path = os.path.join(video_path, video_name)
        cmd = f"ffplay {full_path}"
        self.sp = subprocess.Popen(cmd)

    def scoring(self, mos):
        self.scores[self.step] = mos

    def finish(self):
        if self.sp is not None:
            self.sp.kill()
        if self.user is not None:
            with open(f"../data/{self.user}.csv", "w") as res_file:
                for i in range(self.length):
                    res_file.write(f"{self.videos[i]}, {self.scores[i]}\n")
