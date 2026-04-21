<img width="143" height="142" alt="Image6" src="https://github.com/user-attachments/assets/ad205872-c1a2-407d-b6e4-9e290c457c39" /><img width="167" height="157" alt="Image2" src="https://github.com/user-attachments/assets/17800824-1f6f-4440-a681-b73ace2a86e2" /><img width="142" height="147" alt="Image3" src="https://github.com/user-attachments/assets/4d45158e-5698-462f-a815-f68602196bbd" /><img width="137" height="144" alt="Image4" src="https://github.com/user-attachments/assets/41cd841e-a4d6-4bf8-a3ba-7d59dcaaf8e1" />

# SectorTimerClock V1.21

**SectorTimerClock** is a desktop analog clock that stays on your screen at all times. It features a built-in timer that displays the remaining time visually as a sector (pie slice) on the clock face.

🔗 [Latest Release](https://github.com/adEGeD3Lf/SectorTimerClock/releases)

---

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation & Launch](#installation--launch)
- [Basic Controls](#basic-controls)
- [Timer](#timer)
- [Right-Click Menu](#right-click-menu)
- [Settings](#settings)
- [Settings File](#settings-file)

---

## System Requirements

- Windows 11

---

## Installation & Launch

1. Extract the ZIP file to any folder
2. Double-click `SectorTimerClock.exe` to launch

To uninstall, simply delete the folder. No registry entries are created.

---

## Basic Controls

| Action | Result |
|--------|--------|
| Left drag | Move the clock anywhere on screen |
| Left double-click | Reset the timer |
| Left click (when flashing) | Stop flashing and reset |
| Right-click | Open the menu |

The window position is saved automatically and restored on next launch (can be disabled in Settings).

---

## Timer

Open the timer from the right-click menu → **Timer Settings**.

### Set by Duration

Specify how much time is left until the end.

Examples:
- `1:30:00` → 1 hour 30 minutes from now
- `45:00` → 45 minutes from now
- `10` → 10 minutes from now

### Set by Time

Set a specific end time. If the specified time has already passed today, it will be set for the same time tomorrow.

Example: `17:30:00` → counts down to 5:30 PM

### Display Modes

The sector scale switches automatically based on how much time remains.

| Mode | Condition | Full circle = |
|------|-----------|---------------|
| **H Mode** | More than 1 hour left | 12 hours |
| **M Mode** | 1–60 minutes left | 60 minutes |
| **S Mode** | 60 seconds or less | 60 seconds |

The sector spans from the current clock position to the end time, shrinking as time passes. A ring around the dial is also shown while the timer is active.

### When the Timer Ends

The entire clock face flashes in the configured color. Left-click or double-click to reset.

### History & Favorites

Frequently used durations and times can be saved with the **Save** button (up to 20 entries, auto-sorted). Items added to **Favorites** appear in the right-click menu for one-click launch. Favorites can be reordered by drag & drop and deleted.

**Default favorites:**
- 5 minutes remaining
- 25 minutes remaining
- Time: 12:00:00

---

## Right-Click Menu

| Item | Description |
|------|-------------|
| Reset Timer | Immediately reset the active timer |
| Timer Settings | Open the timer settings dialog |
| (Favorites list) | Launch a saved favorite with one click |
| Toggle Date Position | Flip the date display between top and bottom |
| Language | Switch between 日本語 and English |
| Settings | Open the detailed settings dialog |
| Quit | Exit the application |

> **Note:** Language changes are saved immediately, but the UI will reflect the new language the next time a dialog is opened.

---

## Settings

Open via right-click → **Settings**. The dialog opens automatically in a position that does not overlap the clock.

### General

| Option | Description |
|--------|-------------|
| Always on Top | Keep the clock above all other windows |
| Smooth Second Hand | Move the second hand smoothly instead of ticking |
| Remember Window Position | Restore the clock position on next launch |
| Opacity | Overall transparency of the clock (10–100%) |
| Diameter | Clock size in pixels (50–600px) |

### Dial Settings

**Numbers:** Customize color, font, and distance from the center.

**Tick Marks:** Set color, width, and length separately for 5-minute and 1-minute marks.

**Date Display:**

| Option | Description |
|--------|-------------|
| Show | Toggle date display on/off |
| Opacity | Transparency of the date text |
| Distance (up/down) | Vertical offset from center (negative = up, positive = down) |
| Format | Choose from 4 formats below |

Date format options (Japanese mode):

| # | Example |
|---|---------|
| 0 | 4/20 |
| 1 | 4/20(月) |
| 2 | 4月20日月曜日 |
| 3 | 2026/4/20 |

Date format options (English mode):

| # | Example |
|---|---------|
| 0 | 4/20 |
| 1 | Mon 4/20 |
| 2 | Mon, Apr 20 |
| 3 | 4/20/2026 |

### Hand Settings

Customize color, length, and width for the hour, minute, and second hands. The hour hand is automatically prevented from being longer than the minute hand.

### Timer Display

**H Mode / M Mode / S Mode:** Set the color and radius (as a percentage of the dial) for each mode's sector.

**Ring:** Set the color and width of the ring shown around the dial while the timer is active.

**Finish Flash:** Set the flash color and flash interval (in seconds).

---

## Settings File

All settings are saved automatically to `settings.json` in the same folder as `SectorTimerClock.exe`. The file can be edited manually, but using the Settings dialog is recommended.

To reset all settings to defaults, delete `settings.json` and relaunch the app.

---

*SectorTimerClock V1.21 — https://github.com/adEGeD3Lf/SectorTimerClock/releases*
