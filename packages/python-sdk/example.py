import time
import random

from dotenv import load_dotenv
from e2b_desktop import Sandbox

load_dotenv()

print("Starting desktop sandbox...")
desktop = Sandbox()
print("Screen size:", desktop.get_screen_size())

desktop.stream.start(enable_auth=True)

print("Stream URL:", desktop.stream.get_url())

input("Press enter to continue...")

print("Desktop Sandbox started, ID:", desktop.sandbox_id)

screenshot = desktop.screenshot(format="bytes")

with open("1.png", "wb") as f:
    f.write(screenshot)

print("Moving mouse to 'Applications' and clicking...")
desktop.move_mouse(100, 100)
desktop.left_click()
print("Cursor position:", desktop.get_cursor_position())

time.sleep(1)
screenshot = desktop.screenshot(format="bytes")
with open("2.png", "wb") as f:
    f.write(screenshot)

for i in range(20):

    x = random.randint(0, 1024)
    y = random.randint(0, 768)
    desktop.move_mouse(x, y)
    desktop.right_click()
    print("Right clicked", i)
    time.sleep(2)

desktop.stream.stop()
desktop.kill()
