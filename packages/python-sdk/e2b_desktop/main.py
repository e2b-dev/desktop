import time
from re import search as re_search
from shlex import quote as quote_string
from typing import Dict, Iterator, Literal, Optional, overload, Tuple
from uuid import uuid4

from e2b import Sandbox as SandboxBase, CommandHandle


class _VNCServer:
    def __init__(self, desktop: "Desktop") -> None:
        self.__vnc_handle: CommandHandle | None = None
        self.__novnc_handle: CommandHandle | None = None

        self._url = f"https://{desktop.get_host(desktop._novnc_port)}/vnc.html"

        pwd_flag = "-nopw"
        if desktop._vnc_password:
            desktop.commands.run("mkdir ~/.vnc")
            desktop.commands.run(f"x11vnc -storepasswd {desktop._vnc_password} ~/.vnc/passwd")
            pwd_flag = "-usepw"

        self._vnc_command = (
            f"x11vnc -display {desktop._display} -forever -wait 50 -shared "
            f"-rfbport {desktop._vnc_port} {pwd_flag} 2>/tmp/x11vnc_stderr.log"
        )
        self._novnc_command = (
            f"cd /opt/noVNC/utils && ./novnc_proxy --vnc localhost:{desktop._vnc_port} "
            f"--listen {desktop._novnc_port} --web /opt/noVNC > /tmp/novnc.log 2>&1"
        )

        self.__desktop = desktop

    def _wait_for_port(self, port: int) -> None:
        timeout = 10 
        interval = 0.5
        elapsed = 0

        while elapsed < timeout:
            output = self.__desktop.commands.run(f'netstat -tuln | grep ":{port} "').stdout
            print(f"{output=}")
            if output:
                return
            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"Port {port} did not become available within {timeout} seconds")

    @property
    def url(self) -> str:
        return self._url

    def start(self) -> None:
        if self.__vnc_handle is not None:
            return

        self.__vnc_handle = self.__desktop.commands.run(self._vnc_command, background=True)
        self._wait_for_port(self.__desktop._vnc_port)

        self.__vnc_handle = self.__desktop.commands.run(self._novnc_command, background=True)
        self._wait_for_port(self.__desktop._novnc_port)

    def stop(self) -> None:
        if self.__vnc_handle:
            self.__vnc_handle.kill()
        
        if self.__novnc_handle:
            self.__novnc_handle.kill()


class Desktop(SandboxBase):
    default_template = "desktop"

    def __init__(
        self,
        resolution: Optional[Tuple[int, int]] = None, 
        dpi: Optional[int] = None,
        display: Optional[str] = None,
        vnc_port: Optional[int] = None,
        novnc_port: Optional[int] = None,
        enable_novnc_auth: bool = False,
        template: Optional[str] = None,
        timeout: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        envs: Optional[Dict[str, str]] = None,
        api_key: Optional[str] = None,
        domain: Optional[str] = None,
        debug: Optional[bool] = None,
        sandbox_id: Optional[str] = None,
        request_timeout: Optional[float] = None,
    ):
        """
        Create a new desktop sandbox.

        By default, the sandbox is created from the `desktop` template.

        :param resolution: Startup the desktop with custom screen resolution. Defaults to (1024, 768)
        :param dpi: Startup the desktop with custom DPI. Defaults to 96
        :param display: Startup the desktop with custom display. Defaults to ":0"
        :param vnc_port: Port number for VNC server. Defaults to 5900
        :param novnc_port: Port number for noVNC server. Defaults to 6080
        :param enable_novnc_auth: If True, use the E2B API key as the VNC password. Defaults to False
        :param template: Sandbox template name or ID
        :param timeout: Timeout for the sandbox in **seconds**, default to 300 seconds. Maximum time a sandbox can be kept alive is 24 hours (86_400 seconds) for Pro users and 1 hour (3_600 seconds) for Hobby users
        :param metadata: Custom metadata for the sandbox
        :param envs: Custom environment variables for the sandbox
        :param api_key: E2B API Key to use for authentication, defaults to `E2B_API_KEY` environment variable
        :param domain: E2B domain to use for authentication, defaults to `E2B_DOMAIN` environment variable
        :param debug: If True, the sandbox will be created in debug mode, defaults to `E2B_DEBUG` environment variable
        :param sandbox_id: Sandbox ID to connect to, defaults to `E2B_SANDBOX_ID` environment variable
        :param request_timeout: Timeout for the request in **seconds**

        :return: sandbox instance for the new sandbox
        """
        super().__init__(
            template=template,
            timeout=timeout,
            metadata=metadata,
            envs=envs,
            api_key=api_key,
            domain=domain,
            debug=debug,
            sandbox_id=sandbox_id,
            request_timeout=request_timeout,
        )
        self._display = display or ":0"
        self._vnc_port = vnc_port or 5900
        self._novnc_port = novnc_port or 6080
        self._vnc_password = self.connection_config.api_key if enable_novnc_auth else None

        width, height = resolution or (1024, 768)

        self.commands.run(
            f"Xvfb {self._display} -ac -screen 0 {width}x{height}x24 -retro -dpi {dpi or 96} -nolisten tcp -nolisten unix",
            background=True
        )
        self._wait_for_xvfb()
        
        self.commands.run("startxfce4", envs={"DISPLAY": self._display}, background=True)

        self.__vnc_server = _VNCServer(self)

    def _wait_for_xvfb(self) -> None:
        timeout = 10
        interval = 0.5
        elapsed = 0

        while elapsed < timeout:
            exit_code = self.commands.run("xdpyinfo -display :0").exit_code
            if exit_code == 0:
                return

            time.sleep(interval)
            elapsed += interval

        raise TimeoutError("Xvfb did not become available within 10 seconds")

    @property
    def vnc_server(self) -> _VNCServer:
        return self.__vnc_server

    @overload
    def take_screenshot(self, format: Literal["stream"]) -> Iterator[bytes]:
        """
        Take a screenshot and return it as a stream of bytes.
        """

    @overload
    def take_screenshot(
        self,
        format: Literal["bytes"],
    ) -> bytearray:
        """
        Take a screenshot and return it as a bytearray.
        """

    def take_screenshot(
        self,
        format: Literal["bytes", "stream"] = "bytes",
    ):
        """
        Take a screenshot and return it in the specified format.

        :param format: The format of the screenshot. Can be 'bytes', 'blob', or 'stream'.
        :returns: The screenshot in the specified format.
        """
        screenshot_path = f"/tmp/screenshot-{uuid4()}.png"

        self.commands.run(f"scrot --pointer {screenshot_path}", envs={"DISPLAY": self._display})

        file = self.files.read(screenshot_path, format=format)
        self.files.remove(screenshot_path)
        return file

    def left_click(self):
        """
        Left click on the current mouse position.
        """
        self.commands.run("xdotool click 1", envs={"DISPLAY": self._display})

    def double_click(self):
        """
        Double left click on the current mouse position.
        """
        self.commands.run("xdotool click --repeat 2 1", envs={"DISPLAY": self._display})

    def right_click(self):
        """
        Right click on the current mouse position.
        """
        self.commands.run("xdotool click 3", envs={"DISPLAY": self._display})

    def middle_click(self):
        """
        Middle click on the current mouse position.
        """
        self.commands.run("xdotool click 2", envs={"DISPLAY": self._display})

    def scroll(self, direction: Literal["up", "down"] = "down", amount: int = 1):
        """
        Scroll the mouse wheel by the given amount.

        :param direction: The direction to scroll. Can be "up" or "down".
        :param amount: The amount to scroll.
        """
        self.commands.run(
            f"xdotool click --repeat {amount} {'4' if direction == 'up' else '5'}",
            envs={"DISPLAY": self._display}
        )

    def move_mouse(self, x: int, y: int):
        """
        Move the mouse to the given coordinates.
        
        :param x: The x coordinate.
        :param y: The y coordinate.
        """
        self.commands.run(f"xdotool mousemove --sync {x} {y}", envs={"DISPLAY": self._display})

    def get_cursor_position(self) -> Optional[tuple[int, int]]:
        """
        Get the current cursor position.

        :return: A tuple with the x and y coordinates or None if the cursor is not visible.
        """
        result = self.commands.run("xdotool getmouselocation", envs={"DISPLAY": self._display})
        if output := result.stdout:
            if groups := re_search( r"x:(\d+)\s+y:(\d+)", output):
                x, y = groups.group(1), groups.group(2)
                if x and y:
                    return int(x), int(y)
        
    def get_screen_size(self) -> Optional[tuple[int, int]]:
        """
        Get the current screen size.

        :return: A tuple with the width and height or None if the screen size is not visible.
        """
        result = self.commands.run("xrandr", envs={"DISPLAY": self._display})
        if output := result.stdout:
            _match = re_search(r"(\d+x\d+)", output)
            if _match:
                return tuple(map(int, _match.group(1).split("x")))  # type: ignore

    def write(self,        
        text: str,
        *,
        chunk_size: int = 25,
        delay_in_ms: int = 75
    ) -> None:
        """
        Write the given text at the current cursor position.
        
        :param text: The text to write.
        :param chunk_size: The size of each chunk of text to write.
        :param delay_in_ms: The delay between each chunk of text.
        """
        def break_into_chunks(text: str, n: int):
            for i in range(0, len(text), n):
                yield text[i : i + n]

        for chunk in break_into_chunks(text, chunk_size):
            self.commands.run(
                f"xdotool type --delay {delay_in_ms} {quote_string(chunk)}", envs={"DISPLAY": self._display}
            )

    def press(self, key: str):
        """
        Press a key.

        :param key: The key to press (e.g. "enter", "space", "backspace", etc.).
        """
        self.commands.run(f"xdotool key {key}", envs={"DISPLAY": self._display})

    def hotkey(self, key: str):
        """
        Press a hotkey.

        :param keys: The key to press (e.g. "ctrl+c").
        """
        self.press(key)

    def open(self, file_or_url: str):
        """
        Open a file or a URL in the default application.

        :param file_or_url: The file or URL to open.
        """
        self.commands.run(f"xdg-open {file_or_url}", background=True, envs={"DISPLAY": self._display})


Sandbox = Desktop
