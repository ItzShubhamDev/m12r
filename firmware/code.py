import board
import busio
import displayio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.scanners import DiodeOrientation

from kmk.modules.layers import Layers
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler

from adafruit_st7789 import ST7789
displayio.release_displays()

spi = board.SPI()
while not spi.try_lock():
  pass

spi.configure(baudrate=24000000)
spi.unlock()

tft_cs = board.GP16
tft_dc = board.GP17
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.GP11)
display = ST7789(display_bus, width=240, height=280, rowstart=80, bgr=True, invert=True)

keyboard = KMKKeyboard()
macros = Macros()
encoder_handler = EncoderHandler()

keyboard.modules.append(encoder_handler)
keyboard.modules.append(macros)

keyboard.col_pins = (board.GP21, board.GP20, board.GP19, board.GP18)
keyboard.row_pins = (board.GP4, board.GP3, board.GP2, board.GP5)

keyboard.diode_orientation = DiodeOrientation.COL2ROW
encoder_handler.pins = ((board.GP6, board.GP7, None), (board.GP14, board.GP15, None))

keyboard.keymap = [
  [
    KC.Macro(Press(KC.LCTRL), Tap(KC.S), Release(KC.LCTRL)), KC.Macro(Press(KC.LALT), Press(KC.LSHIFT), Tap(KC.F), Release(KC.LSHIFT), Release(KC.LALT)), KC.Macro(Press(KC.LALT), Tap(KC.Tab), Release(KC.LALT)), KC.Macro(Press(KC.LGUI), Tap(KC.PSCREEN), Release(KC.LGUI)),
    KC.Macro(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL)), KC.Macro(Press(KC.LCTRL), Tap(KC.X), Release(KC.LCTRL)), KC.Macro(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL)), KC.Macro(Press(KC.LGUI), Press(KC.LSHIFT), Tap(KC.S), Release(KC.LSHIFT), Release(KC.LGUI)),
    KC.MUTE
  ]
]

encoder_handler.map = [
  ((KC.VOLU, KC.VOLD), (KC.BRIGHTNESS_UP, KC.BRIGHTNESS_DOWN))
]

text_group = displayio.Group(scale=2, x=50, y=120)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)
splash.append(text_group)

if __name__ == '__main__':
    keyboard.go()