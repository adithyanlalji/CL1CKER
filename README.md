# 100 CPS Insane Autoclicker

This is a simple Python-based autoclicker with a graphical user interface. It allows you to run up to two autoclickers (one left, one right) at a fixed 100 clicks per second. The second autoclicker (right-click) is optional.

## Features

- **100 CPS** left and optional right autoclicker
- Customizable toggle keybinds for each clicker
- Status display within UI
- Prevents assigning the same key to both clickers

## Requirements

- Python 3.6 or newer
- [pynput](https://pypi.org/project/pynput/) (for mouse/keyboard control)

Install the dependency:

```bash
pip install pynput
```

## Usage

1. Run the script:

   ```bash
   python autoclicker.py
   ```

2. In the UI:
   - Set keybinds for left and right toggles (defaults: `F6` and `F7`).
   - Click **Apply Keybinds** to store them.
   - Use the configured keys to start/stop each autoclicker.
   - You must assign different keys; the program will warn you otherwise.

3. Close the window to exit the program.

> ⚠️ The second autoclicker (right click) is optional; leave its keybind blank to disable it.

## Notes

- The application enforces that both autoclickers cannot be set to the same button (left/left or right/right) by design: one controls left clicks, the other right clicks.
- Use responsibly and ensure it complies with application/game rules.

---

Enjoy the insane clicking! 🖱️