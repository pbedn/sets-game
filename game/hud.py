import pyglet


class TextBase(pyglet.text.Label):
    """
    Display text on the screen
    """
    def __init__(self, x, y, text, batch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_name = 'Arial'
        self.font_size = 30
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.batch = batch
        self.text = text
        self.x = x
        self.y = y


class TextCountable(TextBase):
    def __init__(self, x, y, _text, batch, *args, **kwargs):
        super().__init__(x, y, _text, batch, *args, **kwargs)
        self._text = _text
        self._count = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        self.text = self._text + str(self._count)
