import { Sandbox as SandboxBase, SandboxOpts as SandboxOptsBase, CommandHandle, CommandResult, CommandExitError, ConnectionConfig, TimeoutError } from 'e2b'

import { generateRandomString } from './utils'


interface CursorPosition {
  x: number;
  y: number;
}

interface ScreenSize {
  width: number;
  height: number;
}

/**
 * Configuration options for the Sandbox environment.
 * @interface SandboxOpts
 * @extends {SandboxOptsBase}
 */
export interface SandboxOpts extends SandboxOptsBase {
  /**
   * The screen resolution in pixels, specified as [width, height].
   * @type {[number, number]}
   */
  resolution?: [number, number]

  /**
   * Dots per inch (DPI) setting for the display.
   * @type {number}
   */
  dpi?: number

  /**
   * Display identifier.
   * @type {string}
   */
  display?: string

  /**
   * Port number for the VNC server.
   * @type {number}
   */
  vncPort?: number

  /**
   * Port number for the noVNC proxy server.
   * @type {number}
   */
  novncPort?: number

  /**
   * Whether to enable authentication for noVNC connections.
   * @type {boolean}
   */
  enableNoVncAuth?: boolean
}


export class Desktop extends SandboxBase {
  protected static override readonly defaultTemplate: string = 'desktop'
  private lastXfce4Pid: number | null = null;
  readonly display: string;
  readonly vncPort: number;
  readonly novncPort: number;
  readonly novncAuthEnabled: boolean;
  readonly vncServer: VNCServer;
  private readonly changeWallpaperCmd: string = (
    `xfconf-query --create -t string -c xfce4-desktop -p ` +
    `/backdrop/screen0/monitorscreen/workspace0/last-image -s /usr/share/backgrounds/xfce/wallpaper.png`
  )

  /**
   * Use {@link Sandbox.create} to create a new Sandbox instead.
   *
   * @hidden
   * @hide
   * @internal
   * @access protected
   */
  constructor(opts: Omit<SandboxOpts, 'timeoutMs' | 'envs' | 'metadata'> & {
    sandboxId: string;
    envdVersion?: string;
  }) {
    super(opts);
    this.display = opts.display || ':0';
    this.vncPort = opts.vncPort || 5900;
    this.novncPort = opts.novncPort || 6080;
    this.novncAuthEnabled = opts.enableNoVncAuth || false;
    this.lastXfce4Pid = null;
    this.vncServer = new VNCServer(this);
  }
  /**
   * Create a new sandbox from the default `desktop` sandbox template.
   *
   * @param opts connection options.
   *
   * @returns sandbox instance for the new sandbox.
   *
   * @example
   * ```ts
   * const sandbox = await Desktop.create()
   * ```
   * @constructs Desktop
   */
  static async create<S extends typeof Desktop>(
    this: S,
    opts?: SandboxOpts
  ): Promise<InstanceType<S>>
  /**
   * Create a new sandbox from the specified sandbox template.
   *
   * @param template sandbox template name or ID.
   * @param opts connection options.
   *
   * @returns sandbox instance for the new sandbox.
   *
   * @example
   * ```ts
   * const sandbox = await Desktop.create('<template-name-or-id>')
   * ```
   * @constructs Desktop
   */
  static async create<S extends typeof Desktop>(
    this: S,
    template: string,
    opts?: SandboxOpts
  ): Promise<InstanceType<S>>
  static async create<S extends typeof Desktop>(
    this: S,
    templateOrOpts?: SandboxOpts | string,
    opts?: SandboxOpts
  ): Promise<InstanceType<S>> {
    const { template, sandboxOpts } =
      typeof templateOrOpts === 'string'
        ? { template: templateOrOpts, sandboxOpts: opts }
        : { template: this.defaultTemplate, sandboxOpts: templateOrOpts }

    const config = new ConnectionConfig(sandboxOpts)

    let sbx
    if (config.debug) {
      sbx = new this({ sandboxId: 'debug_sandbox_id', ...sandboxOpts, ...config }) as InstanceType<S>
    } else {
      const sandbox = await this.createSandbox(
        template,
        sandboxOpts?.timeoutMs ?? this.defaultSandboxTimeoutMs,
        sandboxOpts
      )
      sbx = new this({ ...sandbox, ...sandboxOpts, ...config }) as InstanceType<S>
    }

    const [width, height] = sandboxOpts?.resolution ?? [1024, 768]
    await sbx.commands.run(
      `Xvfb ${sbx.display} -ac -screen 0 ${width}x${height}x24 ` +
      `-retro -dpi ${sandboxOpts?.dpi ?? 96} -nolisten tcp -nolisten unix`,
      { background: true }
    )

    let hasStarted = await sbx.waitAndVerify(
      `xdpyinfo -display ${sbx.display}`, (r: CommandResult) => r.exitCode === 0
    )
    if (!hasStarted) {
      throw new TimeoutError("Could not start Xvfb")
    }

    await sbx.startXfce4()

    return sbx
  }

  /**
   * Wait for a command to return a specific result.
   * @param cmd - The command to run.
   * @param onResult - The function to check the result of the command.
   * @param timeout - The maximum time to wait for the command to return the result.
   * @param interval - The interval to wait between checks.
   * @returns `true` if the command returned the result within the timeout, otherwise `false`.
   */
  async waitAndVerify(
    cmd: string,
    onResult: (result: CommandResult) => boolean,
    timeout: number = 10,
    interval: number = 0.5
  ): Promise<boolean> {
    let elapsed = 0;

    while (elapsed < timeout) {
      try {
        if (onResult(await this.commands.run(cmd))) {
          return true;
        }
      } catch (e) {
        if (e instanceof CommandExitError) {
          continue;
        }
        throw e;
      }

      await new Promise(resolve => setTimeout(resolve, interval * 1000));
      elapsed += interval;
    }

    return false;
  }

  /**
   * Start xfce4 session if logged out or not running.
   */
  private async startXfce4(): Promise<void> {
    if (this.lastXfce4Pid === null || (
      await this.commands.run(
        `ps aux | grep ${this.lastXfce4Pid} | grep -v grep | head -n 1`
      )).stdout.trim().includes("[xfce4-session] <defunct>")
    ) {
      const result = await this.commands.run(
        "startxfce4", { envs: { DISPLAY: this.display }, background: true }
      );
      this.lastXfce4Pid = result.pid;
      await this.commands.run(this.changeWallpaperCmd, { envs: { DISPLAY: this.display } });
    }
  }

  /**
   * Restart xfce4 session and VNC server. It can be used If you have been logged out.
   */
  async refresh(): Promise<void> {
    await this.startXfce4();
    await this.vncServer.start();
  }

  /**
   * Take a screenshot and save it to the given name.
   * @param format - The format of the screenshot.
   * @returns A Uint8Array bytes representation of the screenshot.
   */
  async takeScreenshot(): Promise<Uint8Array>
  /**
   * Take a screenshot and save it to the given name.
   * @param format - The format of the screenshot.
   * @returns A Uint8Array bytes representation of the screenshot.
   */
  async takeScreenshot(format: 'bytes'): Promise<Uint8Array>
  /**
   * Take a screenshot and save it to the given name.
   * @returns A Blob representation of the screenshot.
   */
  async takeScreenshot(format: 'blob'): Promise<Blob>
  /**
   * Take a screenshot and save it to the given name.
   * @returns A ReadableStream of bytes representation of the screenshot.
   */
  async takeScreenshot(format: 'stream'): Promise<ReadableStream<Uint8Array>>
  async takeScreenshot(format: 'bytes' | 'blob' | 'stream' = 'bytes') {
    const path = `/tmp/screenshot-${generateRandomString()}.png`
    await this.commands.run(`scrot --pointer ${path}`, { envs: { DISPLAY: this.display } })

    // @ts-expect-error
    const file = await this.files.read(path, { format })
    this.files.remove(path)
    return file
  }

  /**
   * Left click on the current mouse position.
   */
  async leftClick(): Promise<void> {
    await this.commands.run("xdotool click 1", { envs: { DISPLAY: this.display } });
  }

  /**
   * Double left click on the current mouse position.
   */
  async doubleClick(): Promise<void> {
    await this.commands.run("xdotool click --repeat 2 1", { envs: { DISPLAY: this.display } });
  }

  /**
   * Right click on the current mouse position.
   */
  async rightClick(): Promise<void> {
    await this.commands.run("xdotool click 3", { envs: { DISPLAY: this.display } });
  }

  /**
   * Middle click on the current mouse position.
   */
  async middleClick(): Promise<void> {
    await this.commands.run("xdotool click 2", { envs: { DISPLAY: this.display } });
  }

  /**
   * Scroll the mouse wheel by the given amount.
   * @param direction - The direction to scroll. Can be "up" or "down".
   * @param amount - The amount to scroll.
   */
  async scroll(direction: 'up' | 'down' = 'down', amount: number = 1): Promise<void> {
    const button = direction === 'up' ? '4' : '5';
    await this.commands.run(
      `xdotool click --repeat ${amount} ${button}`, { envs: { DISPLAY: this.display } }
    );
  }

  /**
   * Move the mouse to the given coordinates.
   * @param x - The x coordinate.
   * @param y - The y coordinate.
   */
  async moveMouse(x: number, y: number): Promise<void> {
    await this.commands.run(
      `xdotool mousemove --sync ${x} ${y}`, { envs: { DISPLAY: this.display } }
    );
  }

  /**
   * Get the current cursor position.
   * @returns A object with the x and y coordinates or null if the cursor is not visible.
   */
  async getCursorPosition(): Promise<CursorPosition | null> {
    const result = await this.commands.run(
      "xdotool getmouselocation", { envs: { DISPLAY: this.display } }
    );

    const match = result.stdout.match(/x:(\d+)\s+y:(\d+)/);
    if (match) {
      const [, x, y] = match;
      if (x && y) {
        return { x: parseInt(x), y: parseInt(y) };
      }
    }
    return null;
  }
  /**
   * Get the current screen size.
   * @returns An {@link ScreenSize} object or null if the screen size is not visible.
   */
  async getScreenSize(): Promise<ScreenSize | null> {
    const result = await this.commands.run(
      "xrandr", { envs: { DISPLAY: this.display } }
    );

    const match = result.stdout.match(/(\d+x\d+)/);
    if (match) {
      const [width, height] = match[1].split('x').map(Number);
      return { width, height };
    }
    return null;
  }

  private *breakIntoChunks(text: string, n: number): Generator<string> {
    for (let i = 0; i < text.length; i += n) {
      yield text.slice(i, i + n);
    }
  }

  private quoteString(s: string): string {
    if (!s) {
      return "''";
    }

    if (!/[^\w@%+=:,./-]/.test(s)) {
      return s;
    }

    // use single quotes, and put single quotes into double quotes
    // the string $'b is then quoted as '$'"'"'b'
    return "'" + s.replace(/'/g, "'\"'\"'") + "'";
  }

  /**
   * Write the given text at the current cursor position.
   * @param text - The text to write.
   * @param chunkSize - The size of each chunk of text to write.
   * @param delayInMs - The delay between each chunk of text.
   */
  async write(
    text: string,
    chunkSize: number = 25,
    delayInMs: number = 75
  ): Promise<void> {
    const chunks = this.breakIntoChunks(text, chunkSize);

    for (const chunk of chunks) {
      await this.commands.run(
        `xdotool type --delay ${delayInMs} ${this.quoteString(chunk)}`,
        { envs: { DISPLAY: this.display } }
      );
    }
  }

  /**
   * Press a key.
   * @param key - The key to press (e.g. "enter", "space", "backspace", etc.).
   */
  async press(key: string): Promise<void> {
    await this.commands.run(
      `xdotool key ${key}`, { envs: { DISPLAY: this.display } }
    );
  }

  /**
   * Press a hotkey.
   * @param key - The key to press (e.g. "ctrl+c").
   */
  async hotkey(key: string): Promise<void> {
    await this.press(key);
  }

  /**
   * Open a file or a URL in the default application.
   * @param fileOrUrl - The file or URL to open.
   */
  async open(fileOrUrl: string): Promise<void> {
    await this.commands.run(
      `xdg-open ${fileOrUrl}`, { background: true, envs: { DISPLAY: this.display } }
    );
  }
}


class VNCServer {
  private vncHandle: CommandHandle | null = null;
  private novncHandle: CommandHandle | null = null;
  private readonly url: URL;
  readonly password: string;
  private vncCommand: string = "";
  private readonly novncCommand: string;
  private readonly desktop: Desktop;

  constructor(desktop: Desktop) {
    this.desktop = desktop;
    this.url = new URL(`https://${desktop.getHost(desktop.novncPort)}/vnc.html`);
    this.password = generateRandomString();

    this.novncCommand = (
      `cd /opt/noVNC/utils && ./novnc_proxy --vnc localhost:${desktop.vncPort} ` +
      `--listen ${desktop.novncPort} --web /opt/noVNC > /tmp/novnc.log 2>&1`
    );
  }

  /**
   * Set the VNC command to start the VNC server.
   */
  private async setVncCommand(): Promise<void> {
    let pwdFlag = "-nopw";
    if (this.desktop.novncAuthEnabled) {
      await this.desktop.commands.run("mkdir ~/.vnc");
      await this.desktop.commands.run(`x11vnc -storepasswd ${this.password} ~/.vnc/passwd`);
      pwdFlag = "-usepw";
    }

    this.vncCommand = (
      `x11vnc -display ${this.desktop.display} -forever -wait 50 -shared ` +
      `-rfbport ${this.desktop.vncPort} ${pwdFlag} 2>/tmp/x11vnc_stderr.log`
    );
  }

  private async waitForPort(port: number): Promise<boolean> {
    return await this.desktop.waitAndVerify(
      `netstat -tuln | grep ":${port} "`, (r: CommandResult) => r.stdout.trim() !== ""
    );
  }

  /**
   * Get the URL to connect to the VNC server.
   * @param autoConnect - Whether to automatically connect to the server after opening the URL.
   * @returns The URL to connect to the VNC server.
   */
  public getUrl(autoConnect: boolean = true): string {
    let url = new URL(this.url);
    if (autoConnect) {
      url.searchParams.set('autoconnect', 'true');
    }
    return url.toString()
  }

  /**
   * Start the VNC server.
   */
  public async start(): Promise<void> {
    await this.stop(); // If start is called while the server is already running, we just restart it

    if (this.vncCommand === "") {
      await this.setVncCommand();
    }
    this.vncHandle = await this.desktop.commands.run(this.vncCommand, { background: true });
    if (!await this.waitForPort(this.desktop.vncPort)) {
      throw new Error("Could not start VNC server");
    }

    this.novncHandle = await this.desktop.commands.run(this.novncCommand, { background: true });
    if (!await this.waitForPort(this.desktop.novncPort)) {
      throw new Error("Could not start noVNC server");
    }
  }

  /**
   * Stop the VNC server.
   */
  public async stop(): Promise<void> {
    if (this.vncHandle) {
      await this.vncHandle.kill();
      this.vncHandle = null;
    }

    if (this.novncHandle) {
      await this.novncHandle.kill();
      this.novncHandle = null;
    }
  }
}

export class Sandbox extends Desktop { }
