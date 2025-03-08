import { config } from 'dotenv'

config()
import { Sandbox } from './dist'
import { writeFileSync } from 'fs';


console.log("Starting desktop sandbox...")

console.time('--> Sandbox creation time');
const desktop = await Sandbox.create();
console.timeEnd('--> Sandbox creation time');

console.log("Desktop Sandbox started, ID:", desktop.sandboxId)
console.log("Screen size:", await desktop.getScreenSize())

await desktop.stream.start({
  enableAuth: true
})

console.log("Stream URL:", desktop.stream.getUrl())

await new Promise(resolve => setTimeout(resolve, 5000));

console.log("Moving mouse to 'Applications' and clicking...")
await desktop.moveMouse(100, 100)
await desktop.leftClick()
console.log("Cursor position:", await desktop.getCursorPosition())

await new Promise(resolve => setTimeout(resolve, 1000));

const screenshot = await desktop.screenshot("bytes")
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
