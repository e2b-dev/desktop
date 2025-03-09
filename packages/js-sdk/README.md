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
npm install @e2b/desktop
```

### 3. Create Desktop Sandbox

```javascript
import { Sandbox } from '@e2b/desktop'

// Basic initialization
const desktop = await Sandbox.create()

// With custom configuration
const desktop = await Sandbox.create({
  display: ':0', // Custom display (defaults to :0)
  resolution: [1920, 1080], // Custom resolution
  dpi: 96 // Custom DPI
})
```

## Features

### Streaming desktop's screen

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

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

// Start the stream
await desktop.stream.start({
  enableAuth: true, // Enable authentication with an auto-generated password that will be injected in the stream UR
})

// Get stream URL
const url = desktop.stream.getUrl()
console.log(url)

// Stop the stream
await desktop.stream.stop()
```

### Mouse control

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

await desktop.doubleClick()
await desktop.leftClick()
await desktop.rightClick()
await desktop.middleClick()
await desktop.scroll(10) // Scroll by the amount. Positive for up, negative for down.
await desktop.moveMouse(100, 200) // Move to x, y coordinates
```

### Keyboard control

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
await desktop.press('ctrl+c') // Copy
```

### Screenshot

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()
const image = await desktop.screenshot()
// Save the image to a file
fs.writeFileSync('screenshot.png', image)
```

### Open file

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

// Open file with default application
await desktop.files.write('/home/user/index.js', "console.log('hello')") // First create the file
await desktop.open('/home/user/index.js') // Then open it
```

### Run any bash commands

```javascript
import { Sandbox } from '@e2b/desktop'

const desktop = await Sandbox.create()

// Run any bash command
const out = await desktop.commands.run('ls -la /home/user')
console.log(out)
```

## Under the hood

The desktop-like environment is based on Linux and [Xfce](https://www.xfce.org/) at the moment. We chose Xfce because it's a fast and lightweight environment that's also popular and actively supported. However, this Sandbox template is fully customizable and you can create your own desktop environment.
Check out the sandbox template's code [here](./template/).
