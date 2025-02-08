import time
import random

from dotenv import load_dotenv
from e2b_desktop import Desktop

load_dotenv()

print("Starting desktop sandbox...")
desktop = Desktop(template="desktop-dev-v2", enable_novnc_auth=True) # Use desktop-dev-v2 If you haven't built desktop-dev
print("Screen size:", desktop.get_screen_size())

desktop.vnc_server.start()

print("VNC URL:", desktop.vnc_server.get_url(auto_connect=True))
print("VNC Password:", desktop.vnc_server.password)

input("Press enter to continue...")

# If you have logged out from the desktop, you can restart the session and vnc server using:
# desktop.refresh()

print("Desktop Sandbox started, ID:", desktop.sandbox_id)

screenshot = desktop.take_screenshot(format="bytes")

with open("1.png", "wb") as f:
    f.write(screenshot)

print("Moving mouse to 'Applications' and clicking...")
desktop.move_mouse(100, 100)
desktop.left_click()
print("Cursor position:", desktop.get_cursor_position())

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

desktop.vnc_server.stop()
desktop.kill()
