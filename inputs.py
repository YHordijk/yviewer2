import pygame as pg


def update():
    keys.update()
    mouse.update()


mod_keys = {
    'lshift': 1073742049,
    'rshift': 1073742053,
    'tab': 9,
}


class Key:
    def __init__(self, key, hold, down, up):
        self.key = key
        self.hold = hold
        self.down = down
        self.up = up

    def __repr__(self):
        return f'Key(name={self.key}, hold={self.hold}, down={self.down}, up={self.up})'

    def __bool__(self):
        return self.hold or self.down


class Keys:
    def __init__(self):
        self.keys = {}

    def update(self):
        for key in self.keys.values():
            if key.up:
                key.up = False
                key.hold = False
            if key.down:
                key.down = False
                key.hold = True

        # events: keydown 769, keyup 768, textinput 771
        for event in pg.event.get(768):
            self.keys[event.key] = Key(event.key, False, True, False)

        for event in pg.event.get(769):
            self.keys[event.key].hold = False
            self.keys[event.key].down = False
            self.keys[event.key].up = True

    def __getattr__(self, key):
        try:
            code = pg.key.key_code(key)
        except ValueError:
            code = mod_keys[key]
        return self.keys.get(code, Key(key, False, False, False))


keys = Keys()


class Mouse:
    def __init__(self):
        self.x = 0
        self.dx = 0
        self.y = 0
        self.dy = 0
        self.buttons = [Key('leftmousebutton',  False, False, False),
                        Key('middlemousebutton', False, False, False),
                        Key('rightmousebutton',   False, False, False)]

    def update(self):
        self.dx = 0
        self.dy = 0
        self.scrollup = False
        self.scrolldown = False

        for button in self.buttons:
            if button.up:
                button.up = False
                button.hold = False
            if button.down:
                button.down = False
                button.hold = True

        # mousemotion
        for event in pg.event.get(1024):
            self.x, self.y = event.pos
            self.dx, self.dy = event.rel
            
        for event in pg.event.get(1025):
            btn = event.button
            if btn == 4:
                self.scrollup = True
                continue
            if btn == 5:
                self.scrolldown = True
                continue
            self.buttons[btn - 1].hold = False
            self.buttons[btn - 1].down = True
            self.buttons[btn - 1].up = False

        for event in pg.event.get(1026):
            btn = event.button
            if btn in [4, 5]:
                continue
            self.buttons[btn - 1].hold = False
            self.buttons[btn - 1].down = False
            self.buttons[btn - 1].up = True

    def __getattr__(self, key):
        code = ['left', 'middle', 'right', 'scrollup', 'scrolldown'].index(key)
        return self.buttons[code]

    @property
    def pos(self):
        return self.x, self.y


mouse = Mouse()
