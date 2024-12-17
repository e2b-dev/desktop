import os
import time
from e2b_desktop import Sandbox

# def test_right_click(sandbox: Sandbox):
#   sandbox.right_click()
#   time.sleep(5)
#   pos = sandbox.locate_on_screen("Create Document")
#   print(pos)
#   assert pos is not None


# def test_screenshot(sandbox: Sandbox):
#   screenshot_path = "test-screenshot.png"
#   sandbox.screenshot(screenshot_path)
#   assert os.path.exists(screenshot_path)

def test_get_cursor_position(sandbox: Sandbox):
  pos = sandbox.get_cursor_position()
  assert pos == (512, 384) # In the middle of the screen


# def test_get_screen_size(sandbox: Sandbox):
#   size = sandbox.get_screen_size()
#   assert size == (1024, 768) # 1024x768 screen

# def test_write(sandbox: Sandbox):
#   # Create a file and open it in a text editor
#   text_file_path = "/home/user/test.txt"
#   sandbox.write(text_file_path, "hello")
#   sandbox.open_file(text_file_path)
