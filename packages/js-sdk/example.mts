import { config } from 'dotenv'

config()
import { Desktop } from './dist'
// import { Desktop } from './src'
import { writeFileSync } from 'fs';


console.log("Starting desktop sandbox...")
const desktop = await Desktop.create('desktop-dev-v2', { enableNoVncAuth: true })
console.log("Screen size:", await desktop.getScreenSize())

await desktop.vncServer.start()

console.log("VNC URL:", desktop.vncServer.getUrl(true))
console.log("VNC Password:", desktop.vncServer.password)

await new Promise(resolve => setTimeout(resolve, 10000));

// If you have logged out from the desktop, you can restart the session and vnc server using:
// await desktop.refresh()

console.log("Desktop Sandbox started, ID:", desktop.sandboxId)

console.log("Moving mouse to 'Applications' and clicking...")
await desktop.moveMouse(100, 100)
await desktop.leftClick()
console.log("Cursor position:", await desktop.getCursorPosition())

await new Promise(resolve => setTimeout(resolve, 1000));

const screenshot = await desktop.takeScreenshot("bytes")
writeFileSync('1.png', Buffer.from(screenshot));


for (let i = 0; i < 1; i++) {
  const x = Math.floor(Math.random() * 1024);
  const y = Math.floor(Math.random() * 768);
  await desktop.moveMouse(x, y);
  await new Promise(resolve => setTimeout(resolve, 2000));
  await desktop.rightClick();
  console.log('right clicked', i)
}


await desktop.vncServer.stop()
await desktop.kill()
