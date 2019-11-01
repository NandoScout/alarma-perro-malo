# coding=UTF-8
import os
import cv2
import time
import vlc #pip install python-vlc


class QueryTrailer:
    def __init__(self, file):
        self.dirname = os.path.dirname(file)
        self.basename = os.path.splitext(os.path.basename(file))[0]
        self.extension = os.path.splitext(file)[1]
        self.stream = cv2.VideoCapture(file)
        self.width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.time_started = time.time()

    def finished(self):
        self.time_finished = time.time()

    def total_time(self):
        return self.time_finished - self.time_started

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def open_trailer(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(self.dirname + '/'+ self.basename +'.' + self.extension)
        self.player.set_media(self.media)
        self.player.play()
        self.player.set_fullscreen(True)
        self.media = self.player.get_media()