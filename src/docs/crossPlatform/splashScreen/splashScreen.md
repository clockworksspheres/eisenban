# Cross Platform Splash Screen

Grock prompt:

# Can I do a tk splash screen cross platform?

**Yes, you can implement a cross-platform splash screen using Tkinter** — and it works reliably on **Windows**, **macOS**, and **Linux**.

Tkinter itself is fully cross-platform (it's the standard GUI library bundled with Python), and a custom splash screen is just a borderless `Toplevel` or `Tk` window with an image/label/progress indicator + a timer or condition to close it. No platform-specific hacks are needed in most cases.

### Key advantages over PyInstaller splash
- Works on macOS (where PyInstaller's Tcl/Tk-based splash fails due to threading restrictions).
- Fully customizable (static image, animated GIF, text, fake progress bar, etc.).
- You control when it closes (after X seconds, after real loading finishes, etc.).
- No extra dependencies beyond Pillow (for better image handling).

### Basic cross-platform example (fixed timer)

```python
import tkinter as tk
from tkinter import ttk
import time  # only for simulation

def create_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)          # remove window decorations (frameless)
    splash.attributes('-topmost', True)    # keep on top
    splash.geometry("400x300+{}+{}".format(
        splash.winfo_screenwidth()//2 - 200,
        splash.winfo_screenheight()//2 - 150
    ))  # center it

    # Optional: semi-transparent background (works on Windows/macOS/Linux with some limits)
    # splash.attributes('-alpha', 0.9)     # uncomment if desired

    # Background image or color
    canvas = tk.Canvas(splash, width=400, height=300, highlightthickness=0)
    canvas.pack()

    # Example: add your logo/image (use Pillow for better formats)
    # from PIL import Image, ImageTk
    # img = Image.open("eisenbanSplashScreen.png")
    # photo = ImageTk.PhotoImage(img)
    # canvas.create_image(200, 120, image=photo)
    # canvas.image = photo  # keep reference!

    # Simple text instead
    canvas.create_text(200, 100, text="Eisenban", font=("Helvetica", 32, "bold"), fill="white")
    canvas.create_text(200, 160, text="Loading...", font=("Helvetica", 16), fill="gray")

    # Optional: progress bar style (fake or real)
    progress = ttk.Progressbar(splash, mode='indeterminate', length=300)
    progress.place(x=50, y=220)
    progress.start()  # animated indeterminate mode

    splash.update()  # force draw before any heavy work

    return splash, progress

# ── Your real app starts here ──
if __name__ == "__main__":
    splash, progress = create_splash()

    # Simulate loading (replace with your actual init code: load data, connect DB, etc.)
    def finish_loading():
        # Do your real heavy initialization here instead of time.sleep
        time.sleep(4)           # ← simulation
        progress.stop()
        splash.destroy()        # close splash

        # Now create & show the MAIN window
        root = tk.Tk()
        root.title("Eisenban - Main App")
        root.geometry("800x600")
        tk.Label(root, text="Welcome to the real application!", font=("Helvetica", 24)).pack(pady=50)
        root.mainloop()

    # Run loading in "background" (here just after delay; use threading for real async)
    splash.after(100, finish_loading)   # start almost immediately

    splash.mainloop()  # keeps splash alive until destroyed
```

### Animated GIF version (very common for loading feel)

Add this inside the canvas or as a Label:

```python
from PIL import Image, ImageTk, ImageSequence

## ... inside create_splash ...

gif_label = tk.Label(splash)
gif_label.place(relx=0.5, rely=0.4, anchor="center")

def animate_gif(ind):
    frame = gif_frames[ind]
    ind += 1
    if ind == len(gif_frames):
        ind = 0
    gif_label.configure(image=frame)
    splash.after(100, animate_gif, ind)  # adjust delay for speed

## Load your animated GIF
gif = Image.open("loading.gif")
gif_frames = []
for frame in ImageSequence.Iterator(gif):
    photo = ImageTk.PhotoImage(frame.copy())
    gif_frames.append(photo)

gif_label.configure(image=gif_frames[0])
animate_gif(0)  # start animation
```

### Tips for best cross-platform results

| Feature                  | Windows | macOS                  | Linux                  | Notes / Workarounds |
|--------------------------|---------|------------------------|------------------------|----------------------|
| `overrideredirect(True)` | Yes     | Yes                    | Yes                    | Makes it frameless   |
| `-topmost`               | Yes     | Yes (usually)          | Yes                    | May need focus tricks on some WMs |
| Transparency (`-alpha`)  | Yes     | Partial (no per-pixel) | Varies by WM           | Avoid if critical    |
| Centering                | Yes     | Yes                    | Yes                    | Use `winfo_screenwidth/height` |
| Animated GIF             | Yes     | Yes                    | Yes                    | Pillow required      |
| Progressbar indeterminate| Yes     | Yes                    | Yes                    | ttk looks native-ish |

- Use `threading.Thread` if you have real background work (don't block Tkinter mainloop).
- For very long loads → update a label with messages via `after()` calls.
- Test on all three OSes — Tkinter look varies slightly (ttk helps unify widgets).

This approach is widely used in real Tkinter apps and avoids all the PyInstaller splash pitfalls on macOS.

If you share more about your app (e.g. do you want timed close or close-after-loading-done? Static image or animated?), I can refine the code further!


