import time
import random

from dotenv import load_dotenv
from e2b_desktop import Desktop

load_dotenv()

print("Starting desktop sandbox...")
desktop = Desktop()

print("VNC URL:", desktop.vnc_url)
input("Press enter to continue...")
print("Desktop Sandbox started, ID:", desktop.sandbox_id)

screenshot = desktop.take_screenshot(format="bytes")
with open("1.png", "wb") as f:
    f.write(screenshot)

print("Moving mouse to 'Applications' and clicking...")
desktop.move_mouse(100, 100)
desktop.left_click()

time.sleep(1)
screenshot = desktop.take_screenshot(format="bytes")
with open("2.png", "wb") as f:
    f.write(screenshot)

for i in range(20):

    x = random.randint(0, 1024)
    y = random.randint(0, 768)
    desktop.move_mouse(x, y)
    desktop.right_click()
    print("Right clicked", i)
    time.sleep(2)

desktop.kill()
