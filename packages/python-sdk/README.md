# E2B Desktop Sandbox - Virtual Computer for Computer Use

E2B Desktop Sandbox is a secure virtual desktop ready for Computer Use. Powered by [E2B](https://e2b.dev).

Each sandbox is isolated from the others and can be customized with any dependencies you want.

![Desktop Sandbox](../../readme-assets/screenshot.png)

### Example app using Computer Use with Anthropic's Claude

Check out the [example open-source app](https://github.com/e2b-dev/secure-computer-use) in a separate repository.

## 🚀 Getting started

The E2B Desktop Sandbox is built on top of [E2B Sandbox](https://e2b.dev/docs).

### 1. Get E2B API key

Sign up at [E2B](https://e2b.dev) and get your API key.
Set environment variable `E2B_API_KEY` with your API key.

### 2. Install SDK

```bash
pip install e2b-desktop
```

### 3. Create Desktop Sandbox

```python
from e2b_desktop import Sandbox

# Basic initialization
desktop = Sandbox()

# With custom configuration
desktop = Sandbox(
    display=":0",  # Custom display (defaults to :0)
    resolution=(1920, 1080),  # Custom resolution
    dpi=96,  # Custom DPI
)
```

## Features

### Streaming desktop's screen

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Start the stream
desktop.stream.start()

# Get stream URL
url = desktop.stream.get_url()
print(url)

# Stop the stream
desktop.stream.stop()
```

### Streaming with password protection

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Start the stream
desktop.stream.start(
    enable_auth=True  # Enable authentication with an auto-generated password that will be injected in the stream URL
)

# Get stream URL
url = desktop.stream.get_url()
print(url)

# Stop the stream
desktop.stream.stop()
```

### Mouse control

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

desktop.double_click()
desktop.left_click()
desktop.right_click()
desktop.middle_click()
desktop.scroll(10) # Scroll by the amount. Positive for up, negative for down.
desktop.mouse_move(100, 200) # Move to x, y coordinates
```

### Keyboard control

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Write text at the current cursor position with customizable typing speed
desktop.write("Hello, world!")  # Default: chunk_size=25, delay_in_ms=75
desktop.write("Fast typing!", chunk_size=50, delay_in_ms=25)  # Faster typing

# Press keys
desktop.press("enter")
desktop.press("space")
desktop.press("backspace")
desktop.press("ctrl+c")
```

### Screenshot

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Take a screenshot and save it as "screenshot.png" locally
image = desktop.screenshot()
# Save the image to a file
with open("screenshot.png", "wb") as f:
    f.write(image)
```

### Open file

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Open file with default application
desktop.files.write("/home/user/index.js", "console.log('hello')") # First create the file
desktop.open("/home/user/index.js") # Then open it
```

### Run any bash commands

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Run any bash command
out = desktop.commands.run("ls -la /home/user")
print(out)
```

## Under the hood

The desktop-like environment is based on Linux and [Xfce](https://www.xfce.org/) at the moment. We chose Xfce because it's a fast and lightweight environment that's also popular and actively supported. However, this Sandbox template is fully customizable and you can create your own desktop environment.
Check out the sandbox template's code [here](./template/).
