# Fillets Python

Python port of the game Fish Fillets NG.

## Origin

This project is a reimplementation/port of the original game:

Fish Fillets NG

https://github.com/FishFilletsNG

https://fillets.sourceforge.net/

All original copyrights belong to their respective authors.

## License

This project is distributed under the terms of the GNU General Public License

as published by the Free Software Foundation; either version 2 of the License,

or (at your option) any later version.

See the LICENSE file for details.

## Disclaimer

This is an unofficial port written in Python.

It is not the original project.

## Current Status

The project currently contains the main game entry point and the translated
engine, menu, level, state, effect, widget, and scripting packages. It is not a
finished standalone release yet: it still expects the original game data files
to be available.

Implemented or partially implemented areas:

- `effect/`: visual effects, pictures, fonts, surface helpers, pixel helpers.
- `gengine/`: engine agents, messages, resource packs, Lua scripting, paths,
  logging, input primitives, and utility types.
- `game/`: application startup and top-level game agent.
- `level/`: level model, room, physics/rules, loading, input, view, scripts.
- `menu/`: world map, level descriptions, nodes, pedometer, menu input.
- `option/`: options/help/language menu states.
- `plan/`: state management, planner, dialogs, subtitles, script commands.
- `state/`: game/demo/movie/poster states.
- `widget/`: basic UI widgets used by the menus.

The active sound implementation is `gengine.agent.pygame_sound_agent`, with
`gengine.agent.dummy_sound_agent` used when sound is disabled or unavailable.

## Requirements

- Python 3.12 has been used during development.
- Pygame for display, input, and audio.
- Lupa for Lua script execution.
- NumPy/SciPy for translated gameplay helpers.
- PyAV for movie/audio decoding.

Install dependencies:

```bash
pip install -r requirements.txt
```

If you clone the repository from scratch, include submodules so the original
game data is checked out into `data/`:

```bash
git clone --recurse-submodules <repo-url>
```

For an existing checkout:

```bash
git submodule update --init --recursive
```

## Game Data

The original Fish Fillets NG data is tracked as a git submodule:

```text
data/ -> https://github.com/FishFilletsNG/fillets-data
```

By default, the application looks for game data in:

```text
data/
```

That is the submodule checkout path. You can still provide an explicit external
data path with the `systemdir` command-line option:

```bash
python main.py systemdir=/path/to/fillets-ng-data
```

`userdir` defaults to `user_data/` inside this repository.

## Running

From the repository root:

```bash
python main.py
```

If `data/` is missing, initialize the submodule first:

```bash
git submodule update --init --recursive
```

Useful options:

- `sound=false`: use the dummy sound agent.
- `systemdir=/path/to/data`: override the default `data/` submodule path.
- `userdir=/path/to/user_data`: set the writable user data directory.
- `lang=en`: set text language.
- `speech=en`: set speech language.
- `fullscreen=false`: start windowed.
- `show_steps=1`: show the step counter in levels.
- `strict_rules=1`: keep strict movement rules enabled.

## Game Controls

- Arrow keys: Move the current fish
- Space: Switch fish
- Backspace: Restart level
- `-` / `+`: Undo / redo
- F1: Help
- F2 / F3: Save / load game
- F5: Show or hide the move counter
- F6: Show or hide subtitles
- F10: Game menu
- F11: Toggle fullscreen
- Option+Enter: Toggle fullscreen, recommended on macOS
- Ctrl+Cmd+F: Toggle fullscreen on macOS
- Shift: Faster game

Fullscreen keeps the logical game resolution and scales it proportionally to the largest size that fits the desktop. The scaled game area is centered, with black bars when the desktop aspect ratio differs.

## Repository Layout

```text
effect/        Visual effects and drawing helpers
game/          Application and top-level game agent
gengine/       Engine agents, resources, scripting, messages, utilities
level/         Level runtime, models, rules, loading, scripts, view/input
menu/          World map and menu flow
option/        Options, help, and language menu states
plan/          State manager, planner, dialogs, subtitles, commands
state/         Game/demo/movie/poster states
user_data/     Writable user data used by the port
widget/        Menu widgets
main.py        Application entry point
```

## Notes

- The scripting layer uses Lua through `lupa`, not Python scripts.
- SDL-specific audio code has been removed; sound uses Pygame's mixer.
- Several translated classes still mirror the original C++ structure closely,
  so some APIs are intentionally thin or placeholder-like while the port
  continues.
- The `data/` directory is versioned as a submodule pointer, not as regular
  files in this repository.
