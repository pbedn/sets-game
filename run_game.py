import pyglet

from game.director import GameWindow

if __name__ == '__main__':
    window = GameWindow(width=1024, height=600, caption="Sets", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()