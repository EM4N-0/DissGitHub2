# from interstate75 import Interstate75, SWITCH_A, SWITCH_B
# from mqtt_as import MQTTClient, config
# from config import wifi_led, blue_led
# import uasyncio as asyncio
# import machine
# import math
# import time
# 
# 
# # Setup display
# i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
# display = i75.display
# WIDTH = i75.width
# HEIGHT = i75.height
# BLACK = display.create_pen(0, 0, 0)
# 
# # Animation settings
# spiral_intensity = 1.0
# running_spiral = True
# 
# # Time window
# START_HOUR = 0    # 9am
# END_HOUR = 24     # 6pm
# 
# # Spiral animation
# async def spiral():
#     global spiral_intensity, running_spiral
#     n = 0from interstate75 import Interstate75, SWITCH_A, SWITCH_B
# from mqtt_as import MQTTClient, config
# from config import wifi_led, blue_led
# import uasyncio as asyncio
# import machine
# import math
# import time
# 
# 
# # Setup display
# i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
# display = i75.display
# WIDTH = i75.width
# HEIGHT = i75.height
# BLACK = display.create_pen(0, 0, 0)
# 
# # Animation settings
# spiral_intensity = 1.0
# running_spiral = True
# 
# # Time window
# START_HOUR = 0    # 9am
# END_HOUR = 24     # 6pm
# 
# # Spiral animation
# async def spiral():
#     c = 2
#     while True:
#         # Check time window
#         current_hour = time.localtime()[3]  # hour in 24h format
#         if START_HOUR <= current_hour < END_HOUR:
#             # Run animation
#             t = time.ticks_ms() / 1000
#             a = n * 140
#             r = c * math.sqrt(n)
#             x = int(r * math.cos(a) + WIDTH // 2)
#             y = int(r * math.sin(a) + HEIGHT // 2)
#             pen = display.create_pen_hsv((t * spiral_intensity) % 1.0, 1.0, spiral_intensity)
#             display.set_pen(pen)
#             display.circle(x, y, 1)
#             i75.update()
#             n += 1
#             if n > 800:
#                 display.set_pen(BLACK)
#                 display.clear()
#                 n = 0
#             await asyncio.sleep(0.001)
#         else:
#             # Outside time window: clear display and pause
#             display.set_pen(BLACK)
#             display.clear()
#             i75.update()
#             await asyncio.sleep(1)  # check again in 1 second
# 
# # Simulate changes in noise level 
# async def change_intensity_loop():
#     global spiral_intensity
#     while True:
#         for level in [1.0, 0.8, 0.6, 0.1]:
#             spiral_intensity = level
#             await asyncio.sleep(15 * 60)  # change every 15 minutes
# 
# # MQTT handling
# def sub_cb(topic, msg, retained):
#     print(f'Topic: "{topic.decode()}" Message: "{msg.decode()}" Retained: {retained}')
#     
# 
# async def heartbeat():
#     s = True
#     while True:
#         await asyncio.sleep_ms(500)
#         blue_led(s)
#         s = not s
# 
# async def wifi_han(state):
#     wifi_led(not state)
#     print('Wifi is ', 'up' if state else 'down')
#     await asyncio.sleep(1)
# 
# async def conn_han(client):
#     await client.subscribe('student/ucfneeg/status', 1)
# 
# async def main(client):
#     try:
#         await client.connect()
#     except OSError:
#         print('Connection failed.')
#         machine.reset()
#         return
#     # Start tasks
#     asyncio.create_task(spiral())
#     asyncio.create_task(change_intensity_loop())
#     while True:
#         await asyncio.sleep(5)
# 
# # MQTT config
# config['subs_cb'] = sub_cb
# config['wifi_coro'] = wifi_han
# config['connect_coro'] = conn_han
# config['clean'] = True
# MQTTClient.DEBUG = True
# 
# client = MQTTClient(config)
# asyncio.create_task(heartbeat())
# 
# try:
#     asyncio.run(main(client))
# finally:
#     client.close()
#     asyncio.new_event_loop()

# from interstate75 import Interstate75, SWITCH_A, SWITCH_B
# from mqtt_as import MQTTClient, config
# from config import wifi_led, blue_led
# import uasyncio as asyncio
# import machine
# import math
# import time
# 
# # =============================
# # Setup display
# # =============================
# i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
# display = i75.display
# WIDTH = i75.width
# HEIGHT = i75.height
# BLACK = display.create_pen(0, 0, 0)
# 
# # =============================
# # Animation settings
# # =============================
# BRIGHTNESS_CAP = 0.3   # overall brightness limit (0.0 to 1.0)
# spiral_intensity = 0.3
# running_spiral = True
# 
# # =============================
# # Time window
# # =============================
# START_HOUR = 9    # 9am
# END_HOUR = 18     # 6pm
# 
# # =============================
# # Spiral animation
# # =============================
# async def spiral():
#     global spiral_intensity, running_spiral
#     n = 0
#     c = 2
#     while True:
#         current_hour = time.localtime()[3]  # hour in 24h format
#         if START_HOUR <= current_hour < END_HOUR:
#             # Run animation
#             t = time.ticks_ms() / 1000
#             a = n * 140
#             r = c * math.sqrt(n)
#             x = int(r * math.cos(a) + WIDTH // 2)
#             y = int(r * math.sin(a) + HEIGHT // 2)
#             # use spiral_intensity as value (brightness)
#             pen = display.create_pen_hsv((t * spiral_intensity) % 1.0, 1.0, spiral_intensity)
#             display.set_pen(pen)
#             display.circle(x, y, 1)
#             i75.update()
#             n += 1
#             if n > 800:
#                 display.set_pen(BLACK)
#                 display.clear()
#                 n = 0
#             await asyncio.sleep(0.001)
#         else:
#             # Outside time window: clear display and pause
#             display.set_pen(BLACK)
#             display.clear()
#             i75.update()
#             await asyncio.sleep(1)
# 
# # =============================
# # Adjust intensity every 15 minutes
# # =============================
# async def change_intensity_loop():
#     global spiral_intensity
#     while True:
#         # base levels are scaled by the brightness cap
#         for level in [1.0, 0.8, 0.6, 0.1]:
#             spiral_intensity = level * BRIGHTNESS_CAP
#             await asyncio.sleep(15 * 60)  # change every 15 minutes
# 
# # =============================
# # MQTT handling
# # =============================
# def sub_cb(topic, msg, retained):
#     print(f'Topic: \"{topic.decode()}\" Message: \"{msg.decode()}\" Retained: {retained}')
# 
# async def heartbeat():
#     s = True
#     while True:
#         await asyncio.sleep_ms(500)
#         blue_led(s)
#         s = not s
# 
# async def wifi_han(state):
#     wifi_led(not state)
#     print('Wifi is ', 'up' if state else 'down')
#     await asyncio.sleep(1)
# 
# async def conn_han(client):
#     await client.subscribe('student/ucfneeg/status', 1)
# 
# # =============================
# # Main
# # =============================
# async def main(client):
#     try:
#         await client.connect()
#     except OSError:
#         print('Connection failed.')
#         machine.reset()
#         return
#     # Start tasks
#     asyncio.create_task(spiral())
#     asyncio.create_task(change_intensity_loop())
#     while True:
#         await asyncio.sleep(5)
# 
# # =
# # MQTT config
# # =============================
# config['subs_cb'] = sub_cb
# config['wifi_coro'] = wifi_han
# config['connect_coro'] = conn_han
# config['clean'] = True
# MQTTClient.DEBUG = True
# 
# client = MQTTClient(config)
# asyncio.create_task(heartbeat())
# 
# try:
#     asyncio.run(main(client))
# finally:
#     client.close()
#     asyncio.new_event_loop()


# from interstate75 import Interstate75, SWITCH_A, SWITCH_B
# from mqtt_as import MQTTClient, config
# from config import wifi_led, blue_led
# import uasyncio as asyncio
# import machine
# import math
# import time
# 
# # =============================
# # Setup display
# # =============================
# i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
# display = i75.display
# WIDTH = i75.width
# HEIGHT = i75.height
# BLACK = display.create_pen(0, 0, 0)
# 
# # =============================
# # Animation settings
# # =============================
# spiral_hue = 0.33     # start green
# spiral_speed = 0.003  # start slow
# running_spiral = True
# 
# # Time window (active all day for exhibition)
# START_HOUR = 0
# END_HOUR = 24
# 
# # =============================
# # Spiral animation
# # =============================
# async def spiral():
#     global spiral_hue, spiral_speed, running_spiral
#     n = 0
#     c = 2
#     while True:
#         current_hour = time.localtime()[3]  # hour in 24h format
#         if START_HOUR <= current_hour < END_HOUR:
#             t = time.ticks_ms() / 1000
#             a = n * 140
#             r = c * math.sqrt(n)
#             x = int(r * math.cos(a) + WIDTH // 2)
#             y = int(r * math.sin(a) + HEIGHT // 2)
#             # Use hue and speed
#             pen = display.create_pen_hsv(spiral_hue, 1.0, 1.0)
#             display.set_pen(pen)
#             display.circle(x, y, 1)
#             i75.update()
#             n += 1
#             if n > 800:
#                 display.set_pen(BLACK)
#                 display.clear()
#                 n = 0
#             await asyncio.sleep(spiral_speed)
#         else:
#             display.set_pen(BLACK)
#             display.clear()
#             i75.update()
#             await asyncio.sleep(1)
# 
# # =============================
# # Change color & speed based on time
# # =============================
# async def change_intensity_loop():
#     global spiral_hue, spiral_speed
#     while True:
#         current_hour = time.localtime()[3]
#         if current_hour < 12:
#             # Morning: quiet
#             spiral_hue = 0.33      # green
#             spiral_speed = 0.003   # slow
#         elif current_hour < 18:
#             # Afternoon: medium busy
#             spiral_hue = 0.16      # yellow
#             spiral_speed = 0.0015  # medium
#         else:
#             # Evening: loud
#             spiral_hue = 0.0       # red
#             spiral_speed = 0.0005  # fast
#         await asyncio.sleep(60)  # check every minute
# 
# # =============================
# # MQTT handling (optional)
# # =============================
# def sub_cb(topic, msg, retained):
#     print(f'Topic: \"{topic.decode()}\" Message: \"{msg.decode()}\" Retained: {retained}')
# 
# async def heartbeat():
#     s = True
#     while True:
#         await asyncio.sleep_ms(500)
#         blue_led(s)
#         s = not s
# 
# async def wifi_han(state):
#     wifi_led(not state)
#     print('Wifi is ', 'up' if state else 'down')
#     await asyncio.sleep(1)
# 
# async def conn_han(client):
#     await client.subscribe('student/ucfneeg/status', 1)
# 
# # =============================
# # Main entry point
# # =============================
# async def main(client):
#     try:
#         await client.connect()
#     except OSError:
#         print('Connection failed.')
#         machine.reset()
#         return
#     asyncio.create_task(spiral())
#     asyncio.create_task(change_intensity_loop())
#     while True:
#         await asyncio.sleep(5)
# 
# # =============================
# # MQTT config
# # =============================
# config['subs_cb'] = sub_cb
# config['wifi_coro'] = wifi_han
# config['connect_coro'] = conn_han
# config['clean'] = True
# MQTTClient.DEBUG = True
# 
# client = MQTTClient(config)
# asyncio.create_task(heartbeat())
# 
# try:
#     asyncio.run(main(client))
# finally:
#     client.close()
#     asyncio.new_event_loop()

# from interstate75 import Interstate75, SWITCH_A, SWITCH_B
# from mqtt_as import MQTTClient, config
# from config import wifi_led, blue_led
# import uasyncio as asyncio
# import machine
# import math
# import time
# import random
# 
# # =============================
# # Setup display
# # =============================
# i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
# display = i75.display
# WIDTH = i75.width
# HEIGHT = i75.height
# BLACK = display.create_pen(0, 0, 0)
# 
# # =============================
# # Animation settings
# # =============================
# spiral_hue = 0.0       # forced to red
# spiral_speed = 0.001   # fast
# spiral_brightness = 1.0
# running_spiral = True
# 
# # =============================
# # Spiral animation
# # =============================
# async def spiral():
#     global spiral_hue, spiral_speed, spiral_brightness
#     n = 0
#     c = 2
#     while True:
#         # Always run regardless of time
#         t = time.ticks_ms() / 1000
#         a = n * 140
#         r = c * math.sqrt(n)
#         x = int(r * math.cos(a) + WIDTH // 2)
#         y = int(r * math.sin(a) + HEIGHT // 2)
#         pen = display.create_pen_hsv(spiral_hue, 1.0, spiral_brightness)
#         display.set_pen(pen)
#         display.circle(x, y, 1)
#         i75.update()
#         n += 1
#         if n > 800:
#             display.set_pen(BLACK)
#             display.clear()
#             n = 0
#         await asyncio.sleep(spiral_speed)
# 
# # =============================
# # Reactive effect (optional)
# # =============================
# async def reactive_effect():
#     global spiral_speed, spiral_brightness
#     while True:
#         # Randomly tweak brightness and speed to simulate sound reactivity
#         spiral_brightness = random.uniform(0.4, 1.0)
#         spiral_speed = max(0.0003, 0.001 * random.uniform(0.5, 1.5))
#         await asyncio.sleep(0.5)
# 
# # =============================
# # MQTT handling (optional)
# # =============================
# def sub_cb(topic, msg, retained):
#     print(f'Topic: \"{topic.decode()}\" Message: \"{msg.decode()}\" Retained: {retained}')
# 
# async def heartbeat():
#     s = True
#     while True:
#         await asyncio.sleep_ms(500)
#         blue_led(s)
#         s = not s
# 
# async def wifi_han(state):
#     wifi_led(not state)
#     print('Wifi is ', 'up' if state else 'down')
#     await asyncio.sleep(1)
# 
# async def conn_han(client):
#     await client.subscribe('student/ucfneeg/status', 1)
# 
# # =============================
# # Main entry point
# # =============================
# async def main(client):
#     try:
#         await client.connect()
#     except OSError:
#         print('Connection failed.')
#         machine.reset()
#         return
#     asyncio.create_task(spiral())
#     asyncio.create_task(reactive_effect())  # add reactive flicker
#     while True:
#         await asyncio.sleep(5)
# 
# # =============================
# # MQTT config
# # =============================
# config['subs_cb'] = sub_cb
# config['wifi_coro'] = wifi_han
# config['connect_coro'] = conn_han
# config['clean'] = True
# MQTTClient.DEBUG = True
# 
# client = MQTTClient(config)
# asyncio.create_task(heartbeat())
# 
# try:
#     asyncio.run(main(client))
# finally:
#     client.close()
#     asyncio.new_event_loop()
# 

from interstate75 import Interstate75, SWITCH_A, SWITCH_B
from mqtt_as import MQTTClient, config
from config import wifi_led, blue_led
import uasyncio as asyncio
import machine

# =============================
# Setup display
# =============================
i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
display = i75.display
WIDTH = i75.width
HEIGHT = i75.height
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

current_message = "Waiting for data..."

# =============================
# Scroll message forever
# =============================
async def scroll_message():
    global current_message
    scale = 1
    y = (HEIGHT - 8) // 2

    while True:
        text_width = display.measure_text(current_message, scale)
        for x in range(WIDTH, -text_width - 1, -1):
            display.set_pen(BLACK)
            display.clear()
            display.set_pen(WHITE)
            display.text(current_message, x, y, scale=scale)
            i75.update()
            await asyncio.sleep(0.02)
        await asyncio.sleep(1)  # pause before next scroll cycle

# =============================
# MQTT Callback
# =============================
def sub_cb(topic, msg, retained):
    global current_message
    current_message = msg.decode()
    print(f'Topic: \"{topic.decode()}\" Message: \"{current_message}\" Retained: {retained}')

# =============================
# LED Heartbeat
# =============================
async def heartbeat():
    s = True
    while True:
        await asyncio.sleep_ms(500)
        blue_led(s)
        s = not s

# =============================
# WiFi and MQTT Handlers
# =============================
async def wifi_han(state):
    wifi_led(not state)
    print('WiFi is', 'up' if state else 'down')
    await asyncio.sleep(1)

async def conn_han(client):
    await client.subscribe('student/ucfneeg/status', 1)

# =============================
# Main entry point
# =============================
async def main(client):
    try:
        await client.connect()
    except OSError:
        print('MQTT connection failed. Rebooting...')
        machine.reset()
        return

    asyncio.create_task(scroll_message())  # start scrolling loop

    while True:
        await asyncio.sleep(5)

# =============================
# MQTT config
# =============================
config['subs_cb'] = sub_cb
config['wifi_coro'] = wifi_han
config['connect_coro'] = conn_han
config['clean'] = True
MQTTClient.DEBUG = True

client = MQTTClient(config)
asyncio.create_task(heartbeat())

try:
    asyncio.run(main(client))
finally:
    client.close()
    asyncio.new_event_loop()
