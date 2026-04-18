
# PomoSectorChrono

A simple desktop timer app that combines an analog clock with a countdown timer.  
Remaining time is visualized intuitively as a sector (wedge) overlaid on the clock face.

---

## Features

- Remaining time displayed as a **wedge sector** overlaid on the analog clock
- Two timer modes: **countdown duration** and **target time**
- Display scale **switches automatically** based on remaining time (hours / minutes / seconds mode)
- **Flashing animation** when the timer finishes
- Register frequently used timers as **favorites** for one-click start
- Highly customizable appearance — clock face, hands, colors, size, and more
- Frameless window with always-on-top support for a **clean desktop presence**

---

## How to Use

You'll figure most of it out just by playing around. But just in case…

## Basic Controls

| Action | Behavior |
|--------|----------|
| Left drag | Move the clock |
| Left double-click | Reset timer |
| Left click after timer ends | Reset timer |
| Right-click | Open context menu |

---

## Right-Click Menu

| Item | Description |
|------|-------------|
| Reset Timer | Stop and reset the running timer |
| Timer Settings | Open the timer settings dialog |
| 　Remaining XX:XX:XX / Time XX:XX:XX | Start a saved favorite timer instantly |
| Flip Date Position | Toggle the date display between top and bottom |
| Advanced Settings | Open the appearance/advanced settings dialog |
| Quit | Exit the app |

Favorites are listed in the order set in Timer Settings. They won't appear if none are registered.

---

## Timer Settings

Open via right-click → **Timer Settings**.

### Set by Duration

Specify a countdown duration. The input format is flexible:

| Input | Meaning |
|-------|---------|
| `25` | 25 minutes |
| `45:00` | 45 minutes |
| `1:30:00` | 1 hour 30 minutes |

- **Save** button: saves the current value to history
- **Delete** button: removes the selected history entry
- **Add to Favorites** button: registers the current value as a favorite (e.g. `Remaining 01:30:00`)
- **Start** button: starts the timer

### Set by Target Time

Specify the time you want the timer to end (e.g. `17:30:00`).  
If the specified time has already passed today, it will be treated as the same time tomorrow.

- **Add to Favorites** button: saves the entry with a name like `Time 17:30:00`

### Favorites Management

A list is shown at the bottom of the Timer Settings dialog.

- **↑ Up / ↓ Down** buttons: reorder how favorites appear in the right-click menu
- **Delete** button: remove the selected favorite

---

## Timer Display Modes

The wedge scale switches automatically based on remaining time:

| Remaining Time | Mode | Scale |
|----------------|------|-------|
| Over 1 hour | H Mode | 12-hour scale |
| 1–60 minutes | M Mode | 60-minute scale |
| 60 seconds or less | S Mode | 60-second scale |

When the timer ends, the clock face flashes in the configured color.  
Click or double-click to reset.

---

## Advanced Settings

Open via right-click → **Advanced Settings**.

### General

- **Always on Top**: keeps the clock in front of all other windows
- **Smooth Second Hand**: enables smooth second hand motion (slightly increases CPU usage)
- **Opacity**: adjusts the overall transparency of the clock
- **Diameter**: changes the size of the clock

### Clock Face

- Customize the color and font of the hour numbers
- Adjust the radial position of the numbers
- Set the color, thickness, and length of 5-minute and 1-minute tick marks
- Configure the date display: color, font, format, opacity, and vertical position

### Hands

Set the color, length, and thickness of the hour, minute, and second hands individually.

### Timer Display

- Set the wedge color and radius for H / M / S modes
- Customize the ring color and thickness
- Configure the flash color and interval shown when the timer ends

---

## Data Storage

All settings, history, and favorites are automatically saved to `settings.json`  
in the same directory as the executable.

---

