# E2B Desktop Sandbox - Open Source Virtual Computer for Computer Use

E2B Desktop Sandbox is an open source secure virtual desktop ready for Computer Use. Powered by [E2B](https://e2b.dev).

Each sandbox is isolated from the others and can be customized with any dependencies you want.

![Desktop Sandbox](readme-assets/screenshot.png)

## Examples

### Open computer use

Check out the [example open-source app](https://github.com/e2b-dev/open-computer-use) in a separate repository.

### Basic SDK usage examples

Check out the examples directory for more examples on how to use the SDK:
- [Python](./examples/basic-python)
- [JavaScript](./examples/basic-javascript)

## 🚀 Getting started

The E2B Desktop Sandbox is built on top of [E2B Sandbox](https://e2b.dev/docs).

### 1. Get E2B API key

Sign up at [E2B](https://e2b.dev) and get your API key.
Set environment variable `E2B_API_KEY` with your API key.

### 2. Install SDK

**Python**

```bash
pip install e2b-desktop
```

**JavaScript**

```bash
npm install @e2b/desktop
```

### 3. Create Desktop Sandbox

**Python**

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

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

// Basic initialization
const desktop = await Sandbox.create()

// With custom configuration
const desktop = await Sandbox.create({
  display: ':0', // Custom display (defaults to :0)
  resolution: [1920, 1080], // Custom resolution
  dpi: 96, // Custom DPI
})
```

## Features

### Streaming desktop's screen

**Python**

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

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

// Start the stream
await desktop.stream.start()

// Get stream URL
const url = desktop.stream.getUrl()
console.log(url)

// Stop the stream
await desktop.stream.stop()
```

### Streaming with password protection

**Python**

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Start the stream
desktop.stream.start(
    require_auth=True  # Require authentication with an auto-generated key
)

# Retrieve the authentication key
auth_key = desktop.stream.get_auth_key()

# Get stream URL
url = desktop.stream.get_url(auth_key=auth_key)
print(url)

# Stop the stream
desktop.stream.stop()
```

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

// Start the stream
await desktop.stream.start({
  requireAuth: true, // Require authentication with an auto-generated key
})

// Retrieve the authentication key
const authKey = await desktop.stream.getAuthKey()

// Get stream URL
const url = desktop.stream.getUrl({ authKey })
console.log(url)

// Stop the stream
await desktop.stream.stop()
```

### Mouse control

**Python**

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

desktop.double_click()
desktop.left_click()
desktop.right_click()
desktop.middle_click()
desktop.scroll(10) # Scroll by the amount. Positive for up, negative for down.
desktop.move_mouse(100, 200) # Move to x, y coordinates
desktop.drag((100, 100), (200, 200)) # Drag using the mouse
desktop.mouse_press("left") # Press the mouse button
desktop.mouse_release("left") # Release the mouse button
```

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

await desktop.doubleClick()
await desktop.leftClick()
await desktop.rightClick()
await desktop.middleClick()
await desktop.scroll(10) // Scroll by the amount. Positive for up, negative for down.
await desktop.moveMouse(100, 200) // Move to x, y coordinates
await desktop.drag([100, 100], [200, 200]) // Drag using the mouse
await desktop.mousePress("left") // Press the mouse button
await desktop.mouseRelease("left") // Release the mouse button
```

### Keyboard control

**Python**

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
desktop.press(["ctrl", "c"]) # Key combination
```

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

// Write text at the current cursor position with customizable typing speed
await desktop.write('Hello, world!')
await desktop.write('Fast typing!', { chunkSize: 50, delayInMs: 25 }) // Faster typing

// Press keys
await desktop.press('enter')
await desktop.press('space')
await desktop.press('backspace')
await desktop.press(['ctrl', 'c']) // Key combination
```

### Screenshot

**Python**

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Take a screenshot and save it as "screenshot.png" locally
image = desktop.screenshot()
# Save the image to a file
with open("screenshot.png", "wb") as f:
    f.write(image)
```

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()
const image = await desktop.screenshot()
// Save the image to a file
fs.writeFileSync('screenshot.png', image)
```

### Open file

**Python**

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Open file with default application
desktop.files.write("/home/user/index.js", "console.log('hello')") # First create the file
desktop.open("/home/user/index.js") # Then open it
```

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

// Open file with default application
await desktop.files.write('/home/user/index.js', "console.log('hello')") // First create the file
await desktop.open('/home/user/index.js') // Then open it
```

### Run any bash commands

**Python**

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

# Run any bash command
out = desktop.commands.run("ls -la /home/user")
print(out)
```

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

// Run any bash command
const out = await desktop.commands.run('ls -la /home/user')
console.log(out)
```

### Wait

**Python**

```python
from e2b_desktop import Sandbox
desktop = Sandbox()

desktop.wait(1000) # Wait for 1 second
``` 

**JavaScript**

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()
await desktop.wait(1000) // Wait for 1 second
```

## Under the hood

The desktop-like environment is based on Linux and [Xfce](https://www.xfce.org/) at the moment. We chose Xfce because it's a fast and lightweight environment that's also popular and actively supported. However, this Sandbox template is fully customizable and you can create your own desktop environment.
Check out the sandbox template's code [here](./template/).
