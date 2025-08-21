import time
import random
from multiprocessing import Process, Queue
import threading

from dotenv import load_dotenv
from e2b_desktop import Sandbox
import webview

load_dotenv()

window_frame_height = 29  # Additional px to take into the account the window border at the top

def move_around(desktop, width, height):
    for i in range(5):
        x = random.randint(0, width)
        y = random.randint(0, height)
        desktop.move_mouse(x, y)
        print(" - Moved mouse to", x, y)
        desktop.right_click()
        print(" - Right clicked", i)
        print(" - Waiting 2 seconds...\n")
        time.sleep(2)

def create_window(stream_url, width, height, command_queue):
    # We create a separate thread to check the queue for the 'close' command that can be sent from the main thread.
    def check_queue():
        while True:
            if not command_queue.empty():
                command = command_queue.get()
                if command == 'close':
                    window.destroy()
                    break
            time.sleep(1)  # Check every second

    window = webview.create_window("Desktop Stream", stream_url, width=width, height=height + window_frame_height)

    # Start queue checking in a separate thread
    t = threading.Thread(target=check_queue)
    t.daemon = True
    t.start()

    webview.start()

def main():
    print("> Starting desktop sandbox...")
    desktop = Sandbox.create()
    print(" - Desktop Sandbox started, ID:", desktop.sandbox_id)

    width, height = desktop.get_screen_size()
    print(" - Desktop Sandbox screen size:", width, height)

    print("\n> Starting desktop stream...")
    desktop.stream.start(require_auth=True)
    auth_key = desktop.stream.get_auth_key()
    stream_url = desktop.stream.get_url(auth_key=auth_key)
    print(" - Stream URL:", stream_url)

    # The webview needs to run on the main thread. That would mean that it would block the program execution.
    # To avoid that, we run it in a separate process and send commands to it via a queue.
    command_queue = Queue()
    webview_process = Process(target=create_window, args=(stream_url, width, height, command_queue))
    webview_process.start()

    print("\n> Waiting 10 seconds for the stream to start...")
    for i in range(10, 0, -1):
        print(f" - {i} seconds remaining until the next step...")
        time.sleep(1)

    print("\n> Randomly moving mouse and right clicking 5 times...")
    move_around(desktop, width, height)

    input("\nPress enter to kill the sandbox and close the window...")

    print("\n> Stopping desktop stream...")
    desktop.stream.stop()
    print(" - Desktop stream stopped")

    print("\n> Closing webview...")
    # When you want to close the window, send the 'close' command to the webview process.
    command_queue.put('close')
    webview_process.join()
    print(" - Webview closed")

    print("\n> Killing desktop sandbox...")
    # Kill the sandbox.
    desktop.kill()
    print(" - Desktop sandbox killed")


if __name__ == "__main__":
    main()
