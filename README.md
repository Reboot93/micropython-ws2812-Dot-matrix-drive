# micropython-ws2812-Dot-matrix-drive
micropython的ws2812点阵屏驱动，继承framebuffer | MicroPython's ws2812 dot matrix screen driver inherits framebuffer

# Usage
``` python
from ws2812 import WS2812

ws = WS2812(27, 5, 20) # pin(27), w(5), h(20)
ws.brightness = 50
ws.fill_888((255, 0, 0))
ws.show()
```

``` python
# framebuffer.fill()
ws.fill(0x0000) # rgb565
ws.fill_888(0, 0, 0) # rgb888

# rgb565 to rgb888
rgb565 = 0x0000
rgb888 = ws.rgb565_to_rgb888(rgb565)

# rgb888 to rgb565
# rgb565 to rgb888
rgb888 = (0, 0, 0)
rgb565 = ws.rgb565_to_rgb888(rgb888)
```
