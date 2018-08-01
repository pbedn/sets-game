import random
from collections import namedtuple

import pyglet
from pyglet.window import mouse, key


COLORS = ['red', 'purple', 'green']
SHAPES = ['oval', 'diamond', 'squiggle']
NUMBERS = ['one', 'two', 'three']
PATTERNS = ['solid', 'striped', 'outlined']

# coordinates [x, y, right: x + width, top: y + height] of image on viewport
Box = namedtuple("Box", "x y right top")

SCALE_CARD_SELECTED = 0.85
SCALE_CARD_UNSELECTED = 0.75


class Card(pyglet.sprite.Sprite):
    """
    Single Card sprite object
    """
    def __init__(self, img, card_color, card_shape, card_pattern, card_number):
        super().__init__(img)
        self.colour = card_color
        self.shape = card_shape
        self.pattern = card_pattern
        self.number = card_number
        self.scale = SCALE_CARD_UNSELECTED

        self.box = Box(5000, 5000, 100, 100)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.box = Box(self.x, self.y, self.x+self.width, self.y+self.height)

    def is_in_the_box(self, x, y):
        if self.box.x <= x <= self.box.right \
                and self.box.y <= y <= self.box.top:
            return True

    def __str__(self):
        return "Card: {}, {}, {}, {}".format(self.colour, self.shape, self.pattern, self.number)


def read_card_images():
    red_deck = pyglet.image.load('res/sets-red.png')
    green_deck = pyglet.image.load('res/sets-green.png')
    purple_deck = pyglet.image.load('res/sets-purple.png')
    red_deck_seq = pyglet.image.ImageGrid(red_deck, 9, 3)
    green_deck_seq = pyglet.image.ImageGrid(green_deck, 9, 3)
    purple_deck_seq = pyglet.image.ImageGrid(purple_deck, 9, 3)

    seq = {'red': red_deck_seq, 'green': green_deck_seq, 'purple': purple_deck_seq}

    card_list = []
    for color, s in seq.items():
        card_seq = iter(reversed(s))
        for pattern in PATTERNS:
            for shape in SHAPES:
                for number in NUMBERS:
                    card = card_seq.__next__()
                    card_list.append(Card(card, color, shape, pattern, number))
    return card_list


class Score(pyglet.text.Label):
    def __init__(self, text, x, y, batch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_name = 'Arial'
        self.font_size = 30
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.batch = batch
        self.text = "Sets found: " + text
        self.x = x
        self.y = y

    def reset(self):
        self.text = '0'


class Cards:
    def __init__(self, rows, cols, batch):
        self.rows = rows
        self.cols = cols
        self.batch = batch

        self.cards = read_card_images()
        self.cards_used = []

        for i in range(self.cols):
            self.draw_random(i*250)

    def __iter__(self):
        for card in self.cards:
            yield card

    def draw_selected(self, color, shape, pattern, number, x, y):
        for card in self.cards:
            if card.shape == shape and card.pattern == pattern \
                    and card.number == number and card.colour == color:
                card.set_position(x, y)
                card.batch = self.batch

    def draw_random(self, x):
        cards = [c for c in self.cards if c not in self.cards_used]
        random.shuffle(cards)
        for i, card in enumerate(cards):
            if i >= self.rows:
                break
            self.draw_selected(card.colour, card.shape, card.pattern, card.number, x+50, 150*i)
            self.cards_used.append(card)


class GameWindow(pyglet.window.Window):
    """
    Game Director managing all actions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(100, 100)
        self.frame_rate = 1/60.0

        self.batch = pyglet.graphics.Batch()

        FeatSwitch = namedtuple("FeatSwitch", "pattern number shape color")
        feat_switch = FeatSwitch(pattern=False, number=False, shape=False, color=True)

        self.cards = Cards(rows=4, cols=4, feat_switch=feat_switch, batch=self.batch)

        self.score = Score('0', self.width-180, self.height-20, batch=self.batch)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            for card in self.cards:
                if card.is_in_the_box(x, y):
                    card.scale = SCALE_CARD_SELECTED
                    print(card)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = GameWindow(width=1024, height=600, caption="Sets", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
