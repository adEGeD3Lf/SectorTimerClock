<img width="143" height="142" alt="Image6" src="https://github.com/user-attachments/assets/ad205872-c1a2-407d-b6e4-9e290c457c39" /><img width="167" height="157" alt="Image2" src="https://github.com/user-attachments/assets/17800824-1f6f-4440-a681-b73ace2a86e2" /><img width="142" height="147" alt="Image3" src="https://github.com/user-attachments/assets/4d45158e-5698-462f-a815-f68602196bbd" /><img width="137" height="144" alt="Image4" src="https://github.com/user-attachments/assets/41cd841e-a4d6-4bf8-a3ba-7d59dcaaf8e1" />

# SectorTimerClock User Manual

**Version: 1.22**

---

## Overview

SectorTimerClock is a desktop analog clock that stays on your screen at all times. It visually displays the remaining time of a timer as a sector (pie slice) on the clock face. In addition to standard timers, it supports a "Sequence Timer" feature that runs multiple timers one after another automatically.

---

## Basic Operations

### Moving the Clock

Left-click and drag the clock face to move it anywhere on the screen.

### Resetting (Stopping) the Timer

Select "Stop Timer" from the right-click menu, click the clock while it is flashing at the end of a timer, or double-click the clock to reset the timer.

---

## Right-Click Menu

Right-clicking the clock opens a context menu.

| Item | Description |
|------|-------------|
| Stop Timer | Resets the running timer |
| Timer Settings | Opens the timer settings dialog |
| Favorites | Instantly starts a registered timer or sequence |
| Toggle Date Position | Switches the date display between top and bottom |
| Language | Switches the display language between 日本語 and English |
| Settings | Opens the detailed settings dialog |
| Quit | Exits the application |

---

## Timer Settings

Selecting "Timer Settings" from the right-click menu opens a dialog with the following sections.

### Set by Duration

Starts a timer for a specified remaining time.

- Input format: `H:MM:SS`, `MM:SS`, or minutes only (e.g. `1:30:00`, `45:00`, `10`)
- Full-width numbers and colons are also accepted
- **Save**: Saves the current value to history
- **Delete**: Removes the selected history entry
- **Add to Favorites**: Registers the current value as a favorite
- **Add to Sequence**: Adds the current value as a step in the sequence
- **Start**: Starts the timer

### Set by Time

Sets a timer that ends at a specified time of day.

- Input format: `HH:MM:SS` (e.g. `15:00:00`)
- If the specified time is in the past, the timer is set for the same time the next day
- Buttons are the same as in "Set by Duration"

### Manage Favorites

Manages timers registered as favorites. Favorites can be started directly from the right-click menu.

- **↑ Up / ↓ Down**: Reorders the selected item
- **Delete**: Removes the selected item from favorites
- Items can also be reordered by drag and drop

### Sequence Timer

Runs multiple timers consecutively.

#### Loading a Saved Sequence

1. Select a sequence from the "Saved Sequences:" dropdown
2. Click **Load** to load it into the step list
3. Click **Delete Saved** to delete a saved sequence (a confirmation dialog appears if the sequence is also registered as a favorite)

#### Editing a Sequence

- Enter a sequence name
- Enter a value in the "Set by Duration" or "Set by Time" input field, then click **Add to Sequence** to add a step
- Select a step in the list and use the following buttons to manage it:

| Button | Description |
|--------|-------------|
| ↑ Up | Moves the selected step up |
| ↓ Down | Moves the selected step down |
| Delete Step | Deletes the selected step |
| Clear All Steps | Clears all steps from the list |
| Add to Favorites | Registers the saved sequence as a favorite |

- Steps can also be reordered by drag and drop

#### Saving

- Enter a sequence name and click **Save** to save the sequence
- The **Save** button is grayed out if the name already exists (overwriting is not allowed)
- The **Add to Favorites** button becomes active only when the current steps exactly match a saved sequence

#### Running a Sequence

| Button | Description |
|--------|-------------|
| Start Sequence | Starts from the first step (grayed out when no steps exist) |
| Start Sequence From Here | Starts from the selected step (active when the 2nd step or later is selected) |

---

## Sequence Timer Behavior

### Moving Between Steps

When a step's timer reaches zero, the next step's timer starts automatically in the background, and the clock flashes to indicate the step has ended.

- Clicking the clock while it is flashing stops the flash and switches the display to the next timer
- The next timer continues running in the background even while the clock is flashing

### Sequence End

When all steps are complete, the clock flashes in the same way as a normal timer ending. Click the clock to reset.

### Interrupting a Running Sequence

If you try to start a new timer while a sequence is running, a confirmation dialog appears: "A sequence timer is running. Do you want to interrupt it?" Select "Interrupt" to stop the sequence and start the new timer, or "Cancel" to keep the sequence running.

### Handling Time-Based Steps

If a step uses a specific time of day and appears in the middle of a sequence, it starts as a timer that ends at the specified time, beginning from when the previous step finishes. If the specified time has already passed, it is treated as the same time the next day.

---

## Timer Display

While a timer is running, the mode switches automatically based on the remaining time, displaying the remaining time as a sector (pie slice) in a color and size that corresponds to the current mode.

### Mode Switching

| Mode | Condition | Reference Scale |
|------|-----------|----------------|
| H Mode | More than 1 hour remaining | 12-hour clock face |
| M Mode | 1 minute to 60 minutes remaining | 60-minute clock face |
| S Mode | 1 second to 60 seconds remaining | 60-second clock face |

### Finish Flash

When the timer reaches zero, the entire clock face flashes in the configured color. The flash interval can be adjusted in Settings.

---

## Settings

Selecting "Settings" from the right-click menu opens the settings dialog.

### General

| Item | Description |
|------|-------------|
| Always on Top | Keeps the clock in front of all other windows |
| Smooth Second Hand | Makes the second hand move smoothly (default is 1-second steps) |
| Remember Window Position | Restores the window position from the previous session on startup |
| Opacity | Sets the overall transparency of the clock (10–100%) |
| Diameter | Sets the size of the clock (50–600px) |

### Dial Settings

- **Numbers**: Color, font, and distance from the center
- **5-min Marks**: Color, width, and length
- **1-min Marks**: Color, width, and length
- **Date**: Color, font, show/hide, opacity, vertical position, and display format

### Hand Settings

Color, length, and width for the hour, minute, and second hands.

### Timer Display

| Item | Description |
|------|-------------|
| H/M/S Mode Color Settings | Opens the color stage settings for each mode |
| H/M/S Mode Radius | Sets the size of the sector |
| Ring | Color and width of the outer ring displayed while the timer is running |
| Finish Flash | Color and interval of the finish flash |

#### Color Stage Settings

Clicking the "Color Settings" button for each mode (H/M/S) opens a dialog for configuring how the sector color changes based on remaining time.

- Set a threshold (remaining time) and the color to apply when the time falls below that threshold
- **Add Stage**: Adds a new stage
- **Delete Stage**: Deletes stages checked with the checkboxes (at least one stage is required)
- Thresholds are automatically sorted in descending order

---

## Installation

No installation process is required. Simply extract the downloaded ZIP file to any folder you like.

## Uninstallation

Simply delete the folder you extracted the files to. No registry entries or files are written anywhere else on your system.

---

## System Requirements

- Windows (confirmed working on Windows 11)

---

*SectorTimerClock V1.22*
*https://github.com/adEGeD3Lf/SectorTimerClock/releases*
