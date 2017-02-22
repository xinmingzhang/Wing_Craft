from itertools import cycle
import string
import random

import pygame as pg

from .. import prepare, tools


#To avoid instantiating unnecessary Font objects,
#Fonts are stored in this dict. When creating a Label or
#Button object, this dict is checked first to see if the
#font already exists in LOADED_FONTS.
LOADED_FONTS = {}

#Default values for Button objects - see Button class for specifics
BUTTON_DEFAULTS = {
        "button_size": (128, 32),
        "call": None,
        "args": None,
        "call_on_up": True,
        "font": None,
        "font_size": 36,
        "text": None,
        "hover_text": None,
        "disable_text": None,
        "text_color": pg.Color("white"),
        "hover_text_color": None,
        "disable_text_color": None,
        "fill_color": None,
        "hover_fill_color": None,
        "disable_fill_color": None,
        "idle_image": None,
        "hover_image": None,
        "disable_image": None,
        "hover_sound": None,
        "click_sound": None,
        "visible": True,
        "active": True,
        "bindings": ()}

#Default values for Label objects - see Label class for specifics
LABEL_DEFAULTS = {
        "font_path": None,
        "font_size": 12,
        "text_color": "white",
        "fill_color": None,
        "alpha": 255}



#Helper function for MultiLineLabel class
def wrap_text(text, char_limit, separator=" "):
    """
    Split a string into a list of strings no longer than char_limit
    without splitting individual words.
    """
    words = text.split(separator)
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if len(word) + current_length <= char_limit:
            current_length += len(word) + len(separator)
            current_line.append(word)
        else:
            lines.append(separator.join(current_line))
            current_line = [word]
            current_length = len(word) + len(separator)
    if current_line:
        lines.append(separator.join(current_line))
    return lines


#Helper function to allow multiple ways to pass color arguments
def _parse_color(color):
    """
    Accepts an RGB, RGBA or pygame color-name and returns
    a pygame.Color object.
    """
    if color is not None:
        try:
            return pg.Color(str(color))
        except ValueError as e:
            return pg.Color(*color)
    return color


class Label(pg.sprite.Sprite, tools._KwargMixin):
    """
    Parent class all labels inherit from. Color arguments can use color names
    or an RGB tuple. rect_attr should be a dict with keys of pygame.Rect
    attribute names (strings) and the relevant position(s) as values.

    Creates a surface with text blitted to it (self.image) and an associated
    rectangle (self.rect). Label will have a transparent bg if
    fill_color is not passed to __init__.
    """
    def __init__(self, text, rect_attr, *groups, **kwargs):
        """
        text: the text to be displayed on the screen
        rect_attr: a dict of pygame.Rect attributes
                        ex. {"midtop": (100, 100)}
        groups: sprite groups the label should be added to

        KEYWORD ARGS
        args
        args that are not passed will use the default values in LABEL_DEFAULTS
        """



        super(Label, self).__init__(*groups)
        self.process_kwargs("Label", LABEL_DEFAULTS, kwargs)
        path, size = self.font_path, self.font_size
        if (path, size) not in LOADED_FONTS:
            LOADED_FONTS[(path, size)] = pg.font.Font(path, size)
        self.font = LOADED_FONTS[(path, size)]
        self.fill_color = _parse_color(self.fill_color)
        self.text_color = _parse_color(self.text_color)
        self.rect_attr = rect_attr
        self.set_text(text)

        self.original_text = self.text
        self.frequency = 500
        self.timer = 0
        self.visible = True

    def set_text(self, text):
        """Set the text to display."""
        self.text = text
        self.update_text()

    def update_text(self):
        """Update the surface using the current properties and text."""
        if self.alpha != 255:
            self.fill_color = pg.Color(*[x + 1 if x < 255 else x - 1 for x in self.text_color[:3]])
        if self.fill_color:
            render_args = (self.text, True, self.text_color, self.fill_color)

        else:
            render_args = (self.text, True, self.text_color)
        self.image = self.font.render(*render_args)
        if self.alpha != 255:
            self.image.set_colorkey(self.fill_color)
            self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(**self.rect_attr)


    def draw(self, surface):
        """Blit self.image to target surface."""
        surface.blit(self.image, self.rect)

    def blink(self,dt):
        '''well, I will merge Blinker class ^v^'''

        self.timer += dt
        if self.timer > self.frequency:
            self.timer -= self.frequency
            self.visible = not self.visible
            text = self.original_text if self.visible else ""
            self.set_text(text)

    def unblink(self):
        self.set_text(self.original_text)







class Blinker(Label):
    def __init__(self, text, rect_attributes, frequency, *groups, **kwargs):
        super(Blinker, self).__init__(text, rect_attributes, *groups, **kwargs)
        self.original_text = text
        self.frequency = frequency
        self.timer = 0
        self.visible = True

    def update(self, dt):
        self.timer += dt
        if self.timer > self.frequency:
            self.timer -= self.frequency
            self.visible = not self.visible
            text = self.original_text if self.visible else ""
            self.set_text(text)


class MultiLineLabel(pg.sprite.Sprite):
    """Create a single surface with multiple lines of text rendered on it."""
    def __init__(self, path, size, text, color, rect_attr, bg=None,
                         char_limit=42, align="left", vert_space=0):
        """
        Instantiate a MultiLineLabel object.

        ARGS

        path: path to font
        size: font size
        text_color: color of rendered text
        rect_attr: dict of Rect atrribute values for positioning the
                       final surface, e.g., {"midbottom": (100, 100)}
                       or {"centerx": 100, "bottom": 100}
        bg: background color of final surface, transparent if None
        char_limit: max number of characters in each line of text
                         text is split by words, not characters
        align: how text should be aligned/justified - valid args are
                 "left", "center", or "right"
        vert_space: vertical space in between each line
        """
        attr = {"center": (0, 0)}
        lines = wrap_text(text, char_limit)
        labels = [Label(path, size, line, color, attr, bg) for line in lines]
        width = max([label.rect.width for label in labels])
        spacer = vert_space*(len(lines)-1)
        height = sum([label.rect.height for label in labels])+spacer
        self.image = pg.Surface((width, height)).convert()
        self.image.set_colorkey(pg.Color("black"))
        self.image.fill(pg.Color("black"))
        self.rect = self.image.get_rect(**rect_attr)
        aligns = {"left"  : {"left": 0},
                  "center": {"centerx": self.rect.width//2},
                  "right" : {"right": self.rect.width}}
        y = 0
        for label in labels:
            label.rect = label.image.get_rect(**aligns[align])
            label.rect.top = y
            label.draw(self.image)
            y += label.rect.height+vert_space

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class ButtonGroup(pg.sprite.Group):
    """
    A sprite Group modified to allow calling each sprite in the group's
    get_event method similar to using Group.update to call each sprite's
    update method.
    """
    def get_event(self, event, *args, **kwargs):
        check = (s for s in self.sprites() if s.active and s.visible)
        for s in check:
            s.get_event(event, *args, **kwargs)


class Button(pg.sprite.Sprite, tools._KwargMixin):
    """
    A clickable button which accepts a number of keyword
    arguments to allow customization of a button's
    appearance and behavior.
    """
    _invisible = pg.Surface((1,1)).convert_alpha()
    _invisible.fill((0,0,0,0))

    def __init__(self, topleft, *groups, **kwargs):
        """
        Instantiate a Button object based on the keyword arguments. Buttons
        have three possible states (idle, hovered and disabled) and appearance
        options for each state. The button is idle when the mouse is not over
        the button and hovered when it is. The button is disabled when
        Button.active is False and will not respond to events.

        USAGE

        For buttons to function properly, Button.update must be called
        each frame/tick/update with the current mouse position and
        Button.get_event must be called for each event in the event queue.

        ARGS

        topleft: the topleft screen position of the button

        KWARGS

        Buttons accept a number of keyword arguments that may be
        passed individually, as a dict of "keyword": value pairs or a combination
        of the two. Any args that are not passed to __init__ will use the default
        values stored in the BUTTON_DEAFULTS dict

        "button_size": the size of the button in pixels
        "call": callback function
        "args": args to be passed to callback function
        "call_on_up": set to True for clicks to occur on mouseup/keyup
                             set to False for clicks to occur on mousedown/keydown
        "font": path to font - uses pygame's default if None
        "font_size": font size in pixels
        "text": text to be displayed when button is idle
        "hover_text": text to be displayed when mouse is over button
        "disable_text": text to be displayed when button is disabled
        "text_color": text color when button is idle
        "hover_text_color": text_color when mouse is hovering over button
        "disable_text_color": text color when button is disabled (self.active == False)
        "fill_color": button color when button is idle, transparent if None
        "hover_fill_color": button color when hovered, transparent if None
        "disable_fill_color": button color when disabled, transparent if None
        "idle_image": button image when idle, ignored if None
        "hover_image": button image when hovered, ignored if None
        "disable_image": button image when disabled, ignored if None
        "hover_sound": Sound object to play when hovered, ignored if None
        "click_sound": Sound object to play when button is clicked, ignored if None
        "visible": whether the button should be drawn to the screen
        "active": whether the button should respond to events
        "bindings": which buttons, if any, should be able to click the button - values should
                         be a sequence of pygame key constants, e.g, (pg.K_UP, pg.K_w)
        """
        super(Button, self).__init__(*groups)
        color_args = ("text_color", "hover_text_color", "disable_text_color",
                           "fill_color", "hover_fill_color", "disable_fill_color")
        for c_arg in color_args:
            if c_arg in kwargs and kwargs[c_arg] is not None:
                 kwargs[c_arg] = _parse_color(kwargs[c_arg])
        self.process_kwargs("Button", BUTTON_DEFAULTS, kwargs)
        self.rect = pg.Rect(topleft, self.button_size)
        rendered = self.render_text()
        self.idle_image = self.make_image(self.fill_color, self.idle_image,
                                          rendered["text"])
        self.hover_image = self.make_image(self.hover_fill_color,
                                           self.hover_image, rendered["hover"])
        self.disable_image = self.make_image(self.disable_fill_color,
                                             self.disable_image,
                                             rendered["disable"])
        self.image = self.idle_image
        self.clicked = False
        self.hover = False

    def render_text(self):
        """Render text for each button state."""
        font, size = self.font, self.font_size
        if (font, size) not in LOADED_FONTS:
            LOADED_FONTS[font, size] = pg.font.Font(font, size)
        self.font = LOADED_FONTS[font, size]
        text = self.text and self.font.render(self.text, 1, self.text_color)
        hover = self.hover_text and self.font.render(self.hover_text, 1,
                                                     self.hover_text_color)
        disable = self.disable_text and self.font.render(self.disable_text, 1,
                                                       self.disable_text_color)
        return {"text": text, "hover": hover, "disable": disable}

    def make_image(self, fill, image, text):
        """Create needed button images."""
        if not any((fill, image, text)):
            return None
        final_image = pg.Surface(self.rect.size).convert_alpha()
        final_image.fill((0,0,0,0))
        rect = final_image.get_rect()
        fill and final_image.fill(fill, rect)
        image and final_image.blit(image, rect)
        text and final_image.blit(text, text.get_rect(center=rect.center))
        return final_image

    def get_event(self, event):
        """Process events."""
        if self.active and self.visible:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.on_up_event(event)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.on_down_event(event)
            elif event.type == pg.KEYDOWN and event.key in self.bindings:
                self.on_down_event(event, True)
            elif event.type == pg.KEYUP and event.key in self.bindings:
                self.on_up_event(event, True)

    def on_up_event(self, event, onkey=False):
        """Process mouseup and keyup events."""
        if self.clicked and self.call_on_up:
            self.click_sound and self.click_sound.play()
            self.call and self.call(self.args or self.text)
        self.clicked = False

    def on_down_event(self, event, onkey=False):
        """Process mousedown and keydown events."""
        if self.hover or onkey:
            self.clicked = True
            if not self.call_on_up:
                self.click_sound and self.click_sound.play()
                self.call and self.call(self.args or self.text)

    def update(self, prescaled_mouse_pos):
        """
        Determine whehter the mouse is over the button and
        change button appearance if necessary. Calling
        ButtonGroup.update will call update on any Buttons
        in the group.
        """
        hover = self.rect.collidepoint(prescaled_mouse_pos)
        pressed = pg.key.get_pressed()
        if any(pressed[key] for key in self.bindings):
            hover = True
        if not self.visible:
            self.image = Button._invisible
        elif self.active:
            self.image = (hover and self.hover_image) or self.idle_image
            if not self.hover and hover:
                self.hover_sound and self.hover_sound.play()
            self.hover = hover
        else:
            self.image = self.disable_image or self.idle_image

    def draw(self, surface):
        """Draw the button to the screen."""
        surface.blit(self.image, self.rect)


class TextBox(object):
    def __init__(self,rect,**kwargs):
        self.rect = pg.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.accepted = string.ascii_letters+string.digits+string.punctuation+" "
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : pg.Color("white"),
                    "font_color" : pg.Color("black"),
                    "outline_color" : pg.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pg.Color("blue"),
                    "font" : pg.font.Font(None, self.rect.height+4),
                    "clear_on_enter" : False,
                    "inactive_on_enter" : True,
                    "click_sounds": None}

        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self,event, mouse_pos):
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN,pg.K_KP_ENTER):
                self.execute()
                
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
                    self.play_click()
            elif event.unicode in self.accepted:
                self.buffer.append(event.unicode)
                self.play_click()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(mouse_pos)

    def play_click(self):
        if self.click_sounds:
            random.choice(self.click_sounds).play()
            
    def execute(self):
        if self.command:
            self.command(self.id,self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            #centerx = self.rect.centerx - (self.rendered.get_width() // 2)
            self.render_rect = self.rendered.get_rect(centerx=self.rect.centerx,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pg.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        if pg.time.get_ticks()-self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()

    def draw(self,surface):
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2,self.outline_width*2)
        if outline_color:
            surface.fill(outline_color,outline)
        if self.color:
            surface.fill(self.color,self.rect)
        if self.rendered:
            surface.blit(self.rendered,self.render_rect,self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color,(curse.right+1,curse.y,2,curse.h))
