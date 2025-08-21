import os
import time
from dotenv import load_dotenv
import asyncio
from e2b_desktop import Sandbox
import math
import random

# Load environment variables
load_dotenv()


async def main():
    print("Starting desktop sandbox...")

    print("--> Sandbox creation time", end="")
    start_time = time.time()
    desktop = Sandbox.create()
    end_time = time.time()
    print(f": {end_time - start_time:.3f}s")

    print("Desktop Sandbox started, ID:", desktop.sandbox_id)
    screen_size = desktop.get_screen_size()
    print("Screen size:", screen_size)

    desktop.stream.start(require_auth=True)

    auth_key = desktop.stream.get_auth_key()
    print("Stream URL:", desktop.stream.get_url(auth_key=auth_key))

    await asyncio.sleep(5)

    print("Moving mouse to 'Applications' and clicking...")
    desktop.move_mouse(100, 100)
    desktop.left_click()
    cursor_position = desktop.get_cursor_position()
    print("Cursor position:", cursor_position)

    await asyncio.sleep(1)

    screenshot = desktop.screenshot("bytes")
    with open("1.png", "wb") as f:
        f.write(screenshot)

    for i in range(20):
        x = math.floor(random.random() * 1024)
        y = math.floor(random.random() * 768)
        desktop.move_mouse(x, y)
        await asyncio.sleep(2)
        desktop.right_click()
        print("right clicked", i)

    desktop.stream.stop()
    desktop.kill()


if __name__ == "__main__":
    asyncio.run(main())
