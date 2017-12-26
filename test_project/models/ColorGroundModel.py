class ColorGroundModel:

    def __init__(self, foreground=None, background=None):
        self.__foreground = foreground
        self.__background = background

    @property
    def foreground(self):
        return self.__foreground

    @property
    def background(self):
        return self.__background

    def __str__(self):
        return "foreground = {0}, background = {1}".format(self.__foreground, self.__background)
