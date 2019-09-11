from neopixel import *
import time
import atexit

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = None

# strip helpers
"""set a pixel color, but do not show it yet"""
def setPixel(strip, pixel, color):
    strip.setPixelColor(pixel, color)

"""change the color of all pixels, then show it"""
def setAll(strip, r, g, b):
    for i in range(strip.numPixels()):
        setPixel(strip, i, Color(r, g, b))
        # strip.setPixelColor(i, color)
        # strip.show()
        # time.sleep(wait_ms/1000.0)

# FX
"""fade out from a color"""
def fadeOut(strip, _r, _g, _b):
    for k in range(256):
        brightness = (k/256)
        r = brightness * _r
        g = brightness * _g
        b = brightness * _b
        setAll(strip, r, g, b)
        strip.show()

"""fade in to a color"""
def fadeIn(strip, _r, _g, _b):
    for k in range(255, -1, -1):
        brightness = (k/256)
        r = brightness * _r
        g = brightness * _g
        b = brightness * _b
        setAll(strip, r, g, b)
        strip.show()

"""Wipe color across display a pixel at a time."""
def colorWipe(strip, r, g, b, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r, g, b))
        strip.show()
        time.sleep(wait_ms/1000.0)




def exit_handler():
    print("Clearing strip before exit")
    setAll(strip, 0, 0, 0)
    print("Goodbye")



def setup():
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    atexit.register(exit_handler)


colorWipe(strip, 0, 0, 255)