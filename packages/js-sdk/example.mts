import { config } from 'dotenv'

config()
import { Desktop } from './dist'
import { writeFileSync } from 'fs';


console.log("Starting desktop sandbox...")
const desktop = await Desktop.create({
  enableStreamAuth: true,
})
console.log("Desktop Sandbox started, ID:", desktop.sandboxId)
console.log("Screen size:", await desktop.getScreenSize())

await desktop.stream.start()

console.log("Stream URL:", desktop.stream.getUrl())

await new Promise(resolve => setTimeout(resolve, 5000));

// If you have logged out from the desktop, you can restart the session and stream using:
// await desktop.refresh()

console.log("Moving mouse to 'Applications' and clicking...")
await desktop.moveMouse(100, 100)
await desktop.leftClick()
console.log("Cursor position:", await desktop.getCursorPosition())

await new Promise(resolve => setTimeout(resolve, 1000));

const screenshot = await desktop.takeScreenshot("bytes")
writeFileSync('1.png', Buffer.from(screenshot));


for (let i = 0; i < 20; i++) {
  const x = Math.floor(Math.random() * 1024);
  const y = Math.floor(Math.random() * 768);
  await desktop.moveMouse(x, y);
  await new Promise(resolve => setTimeout(resolve, 2000));
  await desktop.rightClick();
  console.log('right clicked', i)
}


await desktop.stream.stop()
await desktop.kill()
