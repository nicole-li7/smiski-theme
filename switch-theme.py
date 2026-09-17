#!/usr/bin/env python3
"""Switch the colour theme and its matching background art in one step.

VS Code's `background.*` settings are global rather than per-theme, so the
corner image does not follow the theme on its own. This sets both together.

    python3 switch-theme.py smiski     # Smiski Dark   + corner Smiski
    python3 switch-theme.py pine       # Smiski Pine   + corner Smiski
    python3 switch-theme.py blush      # Parisian Blush, no corner image
    python3 switch-theme.py noir       # Blush Noir,     no corner image

Then press Cmd+Alt+B in VS Code. The Background extension patches VS Code's
own files, so nothing takes effect until it re-patches and reloads.

The sidebar cats are left alone; they suit every theme. Add `--dry-run` to
see what would change without writing.
"""
import json, os, sys

IMAGES = "/Users/nicole/Projects/smiski-theme/images"
SETTINGS = os.path.expanduser("~/Library/Application Support/Code/User/settings.json")

# theme key -> (theme label, corner image filename or None)
THEMES = {
    "smiski": ("Smiski Dark", "corner-smiski.png"),
    "pine":   ("Smiski Dark Pine", "corner-smiski.png"),
    "blush":  ("Parisian Blush", None),
    "noir":   ("Parisian Blush Noir", None),
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    dry = "--dry-run" in sys.argv
    if len(args) != 1 or args[0] not in THEMES:
        print(__doc__)
        print("choices: " + ", ".join(THEMES))
        raise SystemExit(1)

    label, corner = THEMES[args[0]]
    s = json.load(open(SETTINGS))
    s["workbench.colorTheme"] = label
    s.setdefault("background.editor", {})["images"] = (
        [f"file://{IMAGES}/{corner}"] if corner else []
    )

    print(f"theme  : {label}")
    print(f"corner : {corner or 'none'}")
    print(f"sidebar: {os.path.basename(s.get('background.sidebar', {}).get('images', ['none'])[0])}")
    if dry:
        print("\n--dry-run, nothing written")
        return

    with open(SETTINGS, "w") as fh:
        json.dump(s, fh, indent=4)
        fh.write("\n")
    print("\nsettings updated. Press Cmd+Alt+B in VS Code to apply and reload.")


if __name__ == "__main__":
    main()
