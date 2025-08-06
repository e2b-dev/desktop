package main

import (
	"fmt"
	"log"
	"os/exec"
	"strings"
	"time"

	"github.com/aj-groq/desktop/packages/go-sdk/src"
)

func main() {
	fmt.Println("🚀 Starting Desktop Automation Demo")
	fmt.Println(strings.Repeat("=", 80))

	// Step 1: Create desktop sandbox
	fmt.Println("\n📱 Step 1: Creating desktop sandbox")
	desktop, err := src.NewVNCDesktop("desktop", 40)
	if err != nil {
		log.Fatalf("Failed to create desktop: %v", err)
	}
	defer desktop.Close()

	fmt.Printf("✅ Created sandbox: %s\n", desktop.SandboxID())

	// Start VNC
	vncURL, err := desktop.StartVNC()
	if err != nil {
		log.Printf("Failed to start VNC: %v", err)
	} else {
		fmt.Printf("🖥️  VNC URL: %s\n", vncURL)
	}
	// Open VNC URL in browser if available
	if vncURL != "" {
		go func() {
			fmt.Println("🌐 Opening VNC URL in local browser...")
			if err := exec.Command("open", vncURL).Start(); err != nil {
				log.Printf("Failed to open VNC URL: %v", err)
			}
		}()
	}

	// Wait for VNC to be ready instead of fixed delay
	fmt.Println("⏳ Waiting for VNC desktop to be ready...")
	if err := desktop.WaitForVNCReady(15); err != nil {
		log.Printf("VNC not ready: %v", err)
	} else {
		fmt.Println("✅ VNC desktop is ready")
	}

	// Step 2: Move mouse around to show it's working
	fmt.Println("\n🖱️  Step 2: Moving mouse to demonstrate control")

	if err := desktop.MoveMouse(100, 100); err != nil {
		log.Printf("Failed to move mouse: %v", err)
	} else {
		fmt.Println("✅ Moved mouse to (100,100)")
	}
	// Step 4: Navigate to console.groq.com
	fmt.Println("\n🌐 Step 4: Navigating to console.groq.com")

	// Type URL
	if err := desktop.Open("https://console.groq.com/chat"); err != nil {
		log.Printf("Failed to open URL: %v", err)
	} else {
		fmt.Println("✅ Opening console.groq.com")
	}

	// Wait for browser window to appear instead of fixed delay
	fmt.Println("⏳ Waiting for browser window to load...")
	if err := desktop.WaitForBrowserReady(11); err != nil {
		log.Printf("Browser may not have loaded: %v", err)
	} else {
		fmt.Println("✅ Browser window detected")
	}
	time.Sleep(3 * time.Second)
	// Step 5: Enter "computer use works"
	fmt.Println("\n⌨️  Step 5: Entering 'computer use works'")

	// Press Tab to find input field (using string)
	if err := desktop.Press("tab"); err != nil {
		log.Printf("Failed to press Tab: %v", err)
	} else {
		fmt.Println("✅ Pressed Tab")
	}

	// Small delay to allow focus to change
	time.Sleep(500 * time.Millisecond)

	// Type the message
	if err := desktop.Type("computer use works"); err != nil {
		log.Printf("Failed to write message: %v", err)
	} else {
		fmt.Println("✅ Typed 'computer use works'")
	}

	// Small delay to allow typing to complete
	time.Sleep(1 * time.Second)

	// Press Enter (using mapped key name)
	if err := desktop.Press("enter"); err != nil {
		log.Printf("Failed to press Enter: %v", err)
	} else {
		fmt.Println("✅ Pressed Enter")
	}
	// Wait a bit for the response to potentially appear
	time.Sleep(1 * time.Second)

	// Step 6: Take multiple screenshots
	fmt.Println("\n📸 Step 6: Taking multiple screenshots")

	// Take first screenshot
	if _, err := desktop.Screenshot("bytes"); err != nil {
		log.Printf("Failed to take first screenshot: %v", err)
	} else {
		fmt.Println("✅ First screenshot saved")
	}

	// Wait a moment between screenshots
	time.Sleep(1 * time.Second)

	// Take second screenshot
	if _, err := desktop.Screenshot("bytes"); err != nil {
		log.Printf("Failed to take second screenshot: %v", err)
	} else {
		fmt.Println("✅ Second screenshot saved")
	}

	// Wait a moment between screenshots
	time.Sleep(1 * time.Second)

	// Take third screenshot
	if _, err := desktop.Screenshot("bytes"); err != nil {
		log.Printf("Failed to take third screenshot: %v", err)
	} else {
		fmt.Println("✅ Third screenshot saved")
	}

	// Open the screenshots
	fmt.Println("\n🖼️  Opening screenshots")
	if err := desktop.Open("/tmp/screenshot.png"); err != nil {
		log.Printf("Failed to open screenshot: %v", err)
	} else {
		fmt.Println("✅ Opened screenshots")
	}

	fmt.Println("\n🎊 Demo completed successfully!")
	fmt.Println("Check /tmp/screenshot.png for the final result")
	fmt.Println(strings.Repeat("=", 80))

	// Keep the process running for 20 seconds
	fmt.Println("\n⏳ Keeping process alive for 20 seconds...")
	time.Sleep(20 * time.Second)
	fmt.Println("✅ Done")
}
