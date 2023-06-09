'''
MicroPython's ws2812 dot matrix screen driver inherits framebuffer

====================================================
MIT License

Copyright (c) 2023 Reboot93

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import framebuf, neopixel, time, struct
from machine import Pin


class WS2812(framebuf.FrameBuffer):

    def __init__(self, pin, w, h):
        self._pin = pin
        self._w = w
        self._h = h
        self._led_count = w * h
        self._brightness = 25
        self._brightness_ratio = self._brightness / 255.0
        self._buf = bytearray(self._led_count * 2)
        super().__init__(self._buf, self._w, self._h, framebuf.RGB565)
        self._np = neopixel.NeoPixel(Pin(self._pin), self._led_count)

    def fill_888(self, r, g, b):
        self.fill(self.rgb888_to_rgb565((r, g, b)))

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    def rgb565_to_rgb888(self, color):
        r = (color >> 11) & 0x1F
        g = (color >> 5) & 0x3F
        b = color & 0x1F
        r = (r * 255 // 31)
        g = (g * 255 // 63)
        b = (b * 255 // 31)
        return r, g, b

    def rgb888_to_rgb565(self, color):
        r, g, b = color
        r = (r * 31 // 255) & 0x1F
        g = (g * 63 // 255) & 0x3F
        b = (b * 31 // 255) & 0x1F
        return (r << 11) | (g << 5) | b

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        if 0 <= brightness <= 255:
            self._brightness = brightness
            self._brightness_ratio = self._brightness / 255.0
        else:
            raise ValueError

    def _rgb565_to_neopixel(self):
        buf_neo = memoryview(self._np.buf)
        index = 0
        for p in struct.unpack(f'<{len(self._buf)//2}H', self._buf):
            r, g, b = self.rgb565_to_rgb888(p)
            buf_neo[index] = int(r * self._brightness_ratio)
            buf_neo[index + 1] = int(g * self._brightness_ratio)
            buf_neo[index + 2] = int(b * self._brightness_ratio)
            index += 3

    def show(self):
        #last = time.ticks_ms()
        self._rgb565_to_neopixel()
        self._np.write()
        #print(time.ticks_diff(time.ticks_ms(), last))
