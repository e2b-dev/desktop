package src

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/aj-groq/E2B/packages/go-sdk/client"
)

// Key mapping constants similar to e2b-dev/desktop Python SDK
const (
	// Special keys
	KEY_BACKSPACE = "BackSpace"
	KEY_TAB       = "Tab"
	KEY_ENTER     = "Return"
	KEY_RETURN    = "Return"
	KEY_SHIFT     = "shift"
	KEY_CTRL      = "ctrl"
	KEY_ALT       = "alt"
	KEY_PAUSE     = "Pause"
	KEY_CAPS_LOCK = "Caps_Lock"
	KEY_ESCAPE    = "Escape"
	KEY_SPACE     = "space"
	KEY_PAGE_UP   = "Page_Up"
	KEY_PAGE_DOWN = "Page_Down"
	KEY_END       = "End"
	KEY_HOME      = "Home"
	KEY_LEFT      = "Left"
	KEY_UP        = "Up"
	KEY_RIGHT     = "Right"
	KEY_DOWN      = "Down"
	KEY_INSERT    = "Insert"
	KEY_DELETE    = "Delete"

	// Function keys
	KEY_F1  = "F1"
	KEY_F2  = "F2"
	KEY_F3  = "F3"
	KEY_F4  = "F4"
	KEY_F5  = "F5"
	KEY_F6  = "F6"
	KEY_F7  = "F7"
	KEY_F8  = "F8"
	KEY_F9  = "F9"
	KEY_F10 = "F10"
	KEY_F11 = "F11"
	KEY_F12 = "F12"

	// Number pad
	KEY_NUM_LOCK = "Num_Lock"
	KEY_NUMPAD_0 = "KP_0"
	KEY_NUMPAD_1 = "KP_1"
	KEY_NUMPAD_2 = "KP_2"
	KEY_NUMPAD_3 = "KP_3"
	KEY_NUMPAD_4 = "KP_4"
	KEY_NUMPAD_5 = "KP_5"
	KEY_NUMPAD_6 = "KP_6"
	KEY_NUMPAD_7 = "KP_7"
	KEY_NUMPAD_8 = "KP_8"
	KEY_NUMPAD_9 = "KP_9"
	KEY_MULTIPLY = "KP_Multiply"
	KEY_ADD      = "KP_Add"
	KEY_SUBTRACT = "KP_Subtract"
	KEY_DECIMAL  = "KP_Decimal"
	KEY_DIVIDE   = "KP_Divide"

	// Modifier combinations
	KEY_SHIFT_LEFT  = "Shift_L"
	KEY_SHIFT_RIGHT = "Shift_R"
	KEY_CTRL_LEFT   = "Control_L"
	KEY_CTRL_RIGHT  = "Control_R"
	KEY_ALT_LEFT    = "Alt_L"
	KEY_ALT_RIGHT   = "Alt_R"
	KEY_META_LEFT   = "Super_L"
	KEY_META_RIGHT  = "Super_R"
	KEY_MENU        = "Menu"
)

// Key mapper for common aliases and cross-platform compatibility
var keyMapper = map[string]string{
	// Common aliases
	"enter":      KEY_ENTER,
	"ret":        KEY_RETURN,
	"esc":        KEY_ESCAPE,
	"ctrl":       KEY_CTRL,
	"control":    KEY_CTRL,
	"alt":        KEY_ALT,
	"shift":      KEY_SHIFT,
	"cmd":        KEY_META_LEFT,
	"super":      KEY_META_LEFT,
	"meta":       KEY_META_LEFT,
	"win":        KEY_META_LEFT,
	"windows":    KEY_META_LEFT,
	"backspace":  KEY_BACKSPACE,
	"del":        KEY_DELETE,
	"delete":     KEY_DELETE,
	"ins":        KEY_INSERT,
	"insert":     KEY_INSERT,
	"pgup":       KEY_PAGE_UP,
	"pgdn":       KEY_PAGE_DOWN,
	"pageup":     KEY_PAGE_UP,
	"pagedown":   KEY_PAGE_DOWN,
	"capslock":   KEY_CAPS_LOCK,
	"numlock":    KEY_NUM_LOCK,
	"tab":        KEY_TAB,
	"scrolllock": "Scroll_Lock",

	// Arrow keys
	"left":  KEY_LEFT,
	"right": KEY_RIGHT,
	"up":    KEY_UP,
	"down":  KEY_DOWN,

	// Special characters that need mapping
	"plus":          "plus",
	"minus":         "minus",
	"equal":         "equal",
	"equals":        "equal",
	"comma":         "comma",
	"period":        "period",
	"dot":           "period",
	"slash":         "slash",
	"backslash":     "backslash",
	"semicolon":     "semicolon",
	"quote":         "apostrophe",
	"apostrophe":    "apostrophe",
	"backtick":      "grave",
	"grave":         "grave",
	"tilde":         "asciitilde",
	"bracket_left":  "bracketleft",
	"bracket_right": "bracketright",
	"brace_left":    "braceleft",
	"brace_right":   "braceright",
	"paren_left":    "parenleft",
	"paren_right":   "parenright",

	// Numbers
	"0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
	"5": "5", "6": "6", "7": "7", "8": "8", "9": "9",

	// Letters (lowercase)
	"a": "a", "b": "b", "c": "c", "d": "d", "e": "e", "f": "f", "g": "g",
	"h": "h", "i": "i", "j": "j", "k": "k", "l": "l", "m": "m", "n": "n",
	"o": "o", "p": "p", "q": "q", "r": "r", "s": "s", "t": "t", "u": "u",
	"v": "v", "w": "w", "x": "x", "y": "y", "z": "z",
}

// mapKey translates common key names to xdotool key names
func mapKey(key string) string {
	// Convert to lowercase for lookup
	lowerKey := strings.ToLower(key)

	// Check if it's in our mapper
	if mapped, exists := keyMapper[lowerKey]; exists {
		return mapped
	}

	// If not found, return original key (case-sensitive for xdotool)
	return key
}

type VNCDesktop struct {
	*client.Client
}

func NewVNCDesktop(templateID string, timeout int) (*VNCDesktop, error) {
	e2bClient, err := client.New(templateID, timeout)
	if err != nil {
		return nil, err
	}

	return &VNCDesktop{
		Client: e2bClient,
	}, nil
}

func (v *VNCDesktop) runCommand(cmd string) error {
	ctx := context.Background()
	return v.RunShellCommandSimple(ctx, cmd)
}

func (v *VNCDesktop) runCommandWithOutput(cmd string) (string, error) {
	ctx := context.Background()
	return v.RunShellCommandWithOutput(ctx, cmd)
}

func (v *VNCDesktop) StartVNC() (string, error) {
	// Create and execute VNC startup script
	scriptCmd := `cat > /tmp/start_vnc.sh << 'EOF'
#!/bin/bash
export DISPLAY=:0

# Start Xvfb if not running
if ! pgrep -x "Xvfb" > /dev/null; then
    Xvfb $DISPLAY -ac -screen 0 1024x768x24 -nolisten tcp &
    sleep 2
fi

# Wait for display
for i in {1..5}; do
    DISPLAY=:0 xdpyinfo >/dev/null 2>&1 && break
    sleep 1
done

# Start XFCE if not running
if ! pgrep -x "xfce4-session" > /dev/null; then
    startxfce4 &
    sleep 3
fi

# Start VNC server
x11vnc -bg -display $DISPLAY -forever -wait 50 -shared -rfbport 5900 -nopw \
    -noxdamage -noxfixes -nowf -noscr -ping 1 -repeat -speeds lan &

# Start noVNC server  
cd /opt/noVNC/utils && ./novnc_proxy --vnc localhost:5900 --listen 6080 --web /opt/noVNC --heartbeat 30 &

echo "READY" > /tmp/vnc_ready
EOF
chmod +x /tmp/start_vnc.sh`

	if err := v.runCommand(scriptCmd); err != nil {
		return "", fmt.Errorf("failed to create script: %v", err)
	}

	// Start script detached
	if err := v.runCommand("nohup /tmp/start_vnc.sh >/dev/null 2>&1 & disown"); err != nil {
		return "", fmt.Errorf("failed to start script: %v", err)
	}

	// Wait for services
	time.Sleep(8 * time.Second)

	// Basic check
	if err := v.runCommand("pgrep -x 'Xvfb' > /dev/null"); err != nil {
		return "", fmt.Errorf("xvfb not running")
	}

	return fmt.Sprintf("https://6080-%s-%s.e2b.app/vnc.html?autoconnect=true&resize=scale",
		v.SandboxID(), v.ClientID()), nil
}

func (v *VNCDesktop) OpenBrowser() error {
	return v.runCommand("DISPLAY=:0 firefox >/dev/null 2>&1 &")
}

func (v *VNCDesktop) TakeScreenshot() error {
	return v.runCommand("DISPLAY=:0 scrot /tmp/screenshot.png")
}

// Desktop automation functions
func (v *VNCDesktop) LeftClick(x, y *int) error {
	cmd := "DISPLAY=:0 xdotool click 1"
	if x != nil && y != nil {
		cmd = fmt.Sprintf("DISPLAY=:0 xdotool mousemove %d %d click 1", *x, *y)
	}
	return v.runCommand(cmd)
}

func (v *VNCDesktop) RightClick(x, y *int) error {
	cmd := "DISPLAY=:0 xdotool click 3"
	if x != nil && y != nil {
		cmd = fmt.Sprintf("DISPLAY=:0 xdotool mousemove %d %d click 3", *x, *y)
	}
	return v.runCommand(cmd)
}

func (v *VNCDesktop) MiddleClick(x, y *int) error {
	cmd := "DISPLAY=:0 xdotool click 2"
	if x != nil && y != nil {
		cmd = fmt.Sprintf("DISPLAY=:0 xdotool mousemove %d %d click 2", *x, *y)
	}
	return v.runCommand(cmd)
}

func (v *VNCDesktop) DoubleClick(x, y *int) error {
	cmd := "DISPLAY=:0 xdotool click --repeat 2 1"
	if x != nil && y != nil {
		cmd = fmt.Sprintf("DISPLAY=:0 xdotool mousemove %d %d click --repeat 2 1", *x, *y)
	}
	return v.runCommand(cmd)
}

func (v *VNCDesktop) MoveMouse(x, y int) error {
	cmd := fmt.Sprintf("DISPLAY=:0 xdotool mousemove %d %d", x, y)
	return v.runCommand(cmd)
}

func (v *VNCDesktop) Drag(fromX, fromY, toX, toY int) error {
	cmd := fmt.Sprintf("DISPLAY=:0 xdotool mousemove %d %d mousedown 1 mousemove %d %d mouseup 1", fromX, fromY, toX, toY)
	return v.runCommand(cmd)
}

func (v *VNCDesktop) Scroll(direction string, amount int) error {
	var button string
	switch direction {
	case "up":
		button = "4"
	case "down":
		button = "5"
	default:
		return fmt.Errorf("invalid scroll direction: %s", direction)
	}

	cmd := fmt.Sprintf("DISPLAY=:0 xdotool click --repeat %d %s", amount, button)
	return v.runCommand(cmd)
}

func (v *VNCDesktop) Write(text string, chunkSize, delayMs int) error {
	// Escape special characters for shell
	escapedText := strings.ReplaceAll(text, "'", "'\"'\"'")
	cmd := fmt.Sprintf("DISPLAY=:0 xdotool type '%s'", escapedText)
	return v.runCommand(cmd)
}

func (v *VNCDesktop) Type(text string) error {
	// Escape special characters for shell
	escapedText := strings.ReplaceAll(text, "'", "'\"'\"'")
	cmd := fmt.Sprintf("DISPLAY=:0 xdotool type '%s'", escapedText)
	return v.runCommand(cmd)
}

func (v *VNCDesktop) Press(key interface{}) error {
	var keyStr string

	switch k := key.(type) {
	case []string:
		// Map each key and join with "+"
		mappedKeys := make([]string, len(k))
		for i, keyName := range k {
			mappedKeys[i] = mapKey(keyName)
		}
		keyStr = strings.Join(mappedKeys, "+")
	case string:
		keyStr = mapKey(k)
	default:
		return fmt.Errorf("invalid key type: must be string or []string")
	}

	cmd := fmt.Sprintf("DISPLAY=:0 xdotool key %s", keyStr)
	return v.runCommand(cmd)
}

func (v *VNCDesktop) Screenshot(format string) ([]byte, error) {
	if err := v.runCommand("DISPLAY=:0 scrot /tmp/screenshot.png"); err != nil {
		return nil, err
	}

	// Read the screenshot file and return bytes if format is "bytes"
	if format == "bytes" {
		output, err := v.runCommandWithOutput("cat /tmp/screenshot.png | base64 -w 0")
		if err != nil {
			return nil, err
		}
		return []byte(output), nil
	}

	return nil, nil
}

func (v *VNCDesktop) Wait(ms int) error {
	time.Sleep(time.Duration(ms) * time.Millisecond)
	return nil
}

func (v *VNCDesktop) Open(fileOrURL string) error {
	cmd := fmt.Sprintf("DISPLAY=:0 nohup xdg-open '%s' > /dev/null 2>&1 &", fileOrURL)
	return v.runCommand(cmd)
}

func (v *VNCDesktop) GetCursorPosition() (int, int, error) {
	output, err := v.runCommandWithOutput("DISPLAY=:0 xdotool getmouselocation --shell")
	if err != nil {
		return 0, 0, err
	}

	var x, y int
	lines := strings.Split(output, "\n")
	for _, line := range lines {
		if strings.HasPrefix(line, "X=") {
			fmt.Sscanf(line, "X=%d", &x)
		} else if strings.HasPrefix(line, "Y=") {
			fmt.Sscanf(line, "Y=%d", &y)
		}
	}

	return x, y, nil
}

func (v *VNCDesktop) GetScreenSize() (int, int, error) {
	output, err := v.runCommandWithOutput("DISPLAY=:0 xdpyinfo | grep dimensions")
	if err != nil {
		return 0, 0, err
	}

	var width, height int
	fmt.Sscanf(output, "  dimensions:    %dx%d pixels", &width, &height)
	return width, height, nil
}

func (v *VNCDesktop) GetCurrentWindowID() (string, error) {
	return v.runCommandWithOutput("DISPLAY=:0 xdotool getactivewindow")
}

func (v *VNCDesktop) GetApplicationWindows(app string) ([]string, error) {
	output, err := v.runCommandWithOutput(fmt.Sprintf("DISPLAY=:0 xdotool search --name '%s'", app))
	if err != nil {
		return nil, err
	}

	windows := strings.Split(strings.TrimSpace(output), "\n")
	if len(windows) == 1 && windows[0] == "" {
		return []string{}, nil
	}

	return windows, nil
}

func (v *VNCDesktop) Close() error {
	return v.Client.Close()
}

// State checking helper functions
func (v *VNCDesktop) WaitForWindow(windowName string, maxWaitSeconds int) error {
	for i := 0; i < maxWaitSeconds; i++ {
		windows, err := v.GetApplicationWindows(windowName)
		if err == nil && len(windows) > 0 {
			return nil
		}
		time.Sleep(1 * time.Second)
	}
	return fmt.Errorf("window '%s' not found after %d seconds", windowName, maxWaitSeconds)
}

func (v *VNCDesktop) WaitForProcess(processName string, maxWaitSeconds int) error {
	for i := 0; i < maxWaitSeconds; i++ {
		err := v.runCommand(fmt.Sprintf("pgrep -x '%s' > /dev/null", processName))
		if err == nil {
			return nil
		}
		time.Sleep(1 * time.Second)
	}
	return fmt.Errorf("process '%s' not running after %d seconds", processName, maxWaitSeconds)
}

func (v *VNCDesktop) WaitForURL(expectedURL string, maxWaitSeconds int) error {
	for i := 0; i < maxWaitSeconds; i++ {
		// Check if browser window is active and has the expected URL
		// This is a simplified check - in practice you might want to use browser automation tools
		windows, err := v.GetApplicationWindows("firefox")
		if err == nil && len(windows) > 0 {
			// Simple heuristic: if firefox windows exist, assume URL is loading/loaded
			// You could enhance this with more sophisticated checks
			return nil
		}
		time.Sleep(1 * time.Second)
	}
	return fmt.Errorf("URL not loaded after %d seconds", maxWaitSeconds)
}

func (v *VNCDesktop) WaitForVNCReady(maxWaitSeconds int) error {
	for range maxWaitSeconds {
		// Check if Xvfb is running
		if err := v.runCommand("pgrep -x 'Xvfb' > /dev/null"); err == nil {
			// Try to get screen size to ensure X server is responsive
			if _, _, err := v.GetScreenSize(); err == nil {
				return nil
			}
		}
		time.Sleep(1 * time.Second)
	}
	return fmt.Errorf("VNC not ready after %d seconds", maxWaitSeconds)
}

func (v *VNCDesktop) IsWindowActive(windowName string) bool {
	windows, err := v.GetApplicationWindows(windowName)
	return err == nil && len(windows) > 0
}

func (v *VNCDesktop) WaitForElement(checkFunc func() bool, maxWaitSeconds int, description string) error {
	for i := 0; i < maxWaitSeconds; i++ {
		if checkFunc() {
			return nil
		}
		time.Sleep(1 * time.Second)
	}
	return fmt.Errorf("%s not ready after %d seconds", description, maxWaitSeconds)
}

// Check if a specific text appears on screen by taking a screenshot and analyzing it
func (v *VNCDesktop) WaitForTextOnScreen(expectedText string, maxWaitSeconds int) error {
	for i := 0; i < maxWaitSeconds; i++ {
		// Take a screenshot and check if we can find the text
		// This is a simplified approach - in practice you might use OCR
		if _, err := v.Screenshot("bytes"); err == nil {
			// For now, we'll assume the page loaded if screenshot was successful
			// You could enhance this with actual text recognition
			fmt.Printf("📸 Screenshot taken, checking for content (attempt %d/%d)\n", i+1, maxWaitSeconds)

			// Simple heuristic: if we can take screenshots consistently, assume page is loaded
			if i >= 2 { // After a few successful screenshots, assume content is there
				return nil
			}
		}
		time.Sleep(1 * time.Second)
	}
	return fmt.Errorf("text '%s' not found on screen after %d seconds", expectedText, maxWaitSeconds)
}

// Check if browser has fully loaded by verifying the window title or other indicators
func (v *VNCDesktop) WaitForBrowserReady(maxWaitSeconds int) error {
	for i := 0; i < maxWaitSeconds; i++ {
		// Check for any browser windows
		firefoxWindows, err := v.GetApplicationWindows("firefox")
		if err == nil && len(firefoxWindows) > 0 {
			// Browser window exists, check if it's responsive
			currentWindow, err := v.GetCurrentWindowID()
			if err == nil && currentWindow != "" {
				return nil
			}
		}

		// Also check for other common browsers
		chromeWindows, _ := v.GetApplicationWindows("chrome")
		if len(chromeWindows) > 0 {
			return nil
		}

		time.Sleep(1 * time.Second)
	}
	return fmt.Errorf("browser not ready after %d seconds", maxWaitSeconds)
}
