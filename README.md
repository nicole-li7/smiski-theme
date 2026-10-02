# Nicole's VS Code Themes

Four VS Code color themes, all generated from one template so they stay
consistent: Smiski greens in graphite or pine, and Parisian Blush in light or
noir.

## Features

- **Smiski Dark** (dark, base `#1e2023`): neutral graphite with sage and olive
  syntax, colors drawn from the Smiski figures.
- **Smiski Dark Pine** (dark, base `#17211e`): clean blue-shifted pine green,
  same Smiski syntax colors.
- **Parisian Blush** (light, base `#faf1ef`): blush paper with rose and copper
  syntax.
- **Parisian Blush Noir** (dark, base `#221a1c`): deep cocoa plum with macaron
  pink and champagne.
- **One template, four outputs.** `build-themes.py` generates every theme file
  from `themes/_template.json` and rewrites `contributes.themes` in
  `package.json`, so adding a variant is one entry in a table.
- **Contrast checks on every build.** 22 checks per theme fail the build if
  body text drops below 4.5:1 or UI chrome below 3.0:1.
- **Light variant support.** Blush has an `ansi` block that flips the terminal's
  neutral ramp for a light background.
- **Background art.** A corner Smiski in the editor and cats in the sidebar,
  drawn by the Background extension (themes cannot include images).
- **`switch-theme.py`** sets the theme and its matching corner art together,
  since `background.*` settings are global.
- **`setup/`** keeps a copy of the VS Code settings and keybindings behind all
  of this, for rebuilding on a new machine.

Side-by-side screenshots: `images/variant-comparison.png` and
`images/blush-comparison.png`.

## Install

There is no .vsix. Clone the repo and symlink the folder into VS Code's
extensions directory:

```
ln -s ~/Projects/smiski-theme ~/.vscode/extensions/nicole-li7.smiski-dark-theme-1.0.0
```

Restart VS Code, then pick a theme with **Preferences: Color Theme**.

### Background art (optional)

1. Install the extension: `code --install-extension shalldie.background`
2. Merge `setup/settings.snippet.json` into your user `settings.json`, fixing
   the absolute image paths if the repo lives somewhere else.
3. Copy `setup/keybindings.json` into your user keybindings. It binds Cmd+Alt+B
   to `extension.background.install`.
4. Trust the folder. The Background extension does not support untrusted
   workspaces, so in Restricted Mode it is disabled and its command silently
   does not exist. Click Manage, then Trust, on the banner.
5. Press Cmd+Alt+B and click Reload. Repeat after any `background.*` change,
   because the extension patches VS Code's own files.

The extension may show a one-time "installation appears to be corrupt" notice.
Choose "Don't Show Again" from its gear menu.

Background notes:

- `background.editor` holds the corner Smiski (`images/corner-smiski.png`) and
  `background.sidebar` holds the cats (`images/sidebar-cats.png`). Emptying
  either `images` list turns that one off. `background.enabled: false` turns
  both off.
- The extension silently resets a top-level `opacity` above 0.6 to 0.1. The
  per-image `styles` block is not clamped, so the sidebar's real opacity (0.8)
  lives there.
- The default blend mode is `screen`, which washes art out on dark themes. The
  config sets `mix-blend-mode: normal`.
- For a different pose, point the corner path at another cutout in `images/`
  (thinking, pointing, idea, briefcase, trio).

### Switching theme and art together

```
python3 switch-theme.py smiski     # Smiski Dark + corner Smiski
python3 switch-theme.py pine       # Smiski Dark Pine + corner Smiski
python3 switch-theme.py blush      # Parisian Blush, no corner image
python3 switch-theme.py noir       # Parisian Blush Noir, no corner image
```

The theme changes right away. Press Cmd+Alt+B to apply the corner image. Pass
`--dry-run` to preview. The sidebar cats are left alone. To give a theme its own
corner art, edit its entry in the `THEMES` table in `switch-theme.py`.

## Making changes

Do not edit the files in `themes/` by hand; they are generated.

1. Edit `themes/_template.json` for structure. Every hex in it is a named slot
   (see `SLOTS` in `build-themes.py`), named for its role (`kw`, `bg_editor`),
   not its color.
2. Edit the `SLOTS`, `ACCENTS` and `VARIANTS` tables in `build-themes.py` for
   colors. Each variant layers its own values over the defaults:
   `ACCENTS <- variant["accents"] <- variant["neutrals"]`.
3. Run `python3 build-themes.py`. It rewrites the theme files and
   `package.json`, prints contrast results, and exits with an error if any
   check fails.
4. Reload the VS Code window. A new or renamed variant will not show in the
   picker until you do.

A new light variant also needs an `ansi` block.

## How it's built

```
build-themes.py        generator: slot tables, variants, contrast checks
switch-theme.py        sets theme + corner art in user settings
package.json           theme list (rewritten by the build)
themes/
  _template.json       the one hand-edited theme
  *-color-theme.json   generated output, four files
setup/
  settings.snippet.json  Background extension config
  keybindings.json       Cmd+Alt+B binding
images/                corner Smiski, sidebar cats, cutouts, screenshots
```

Smiski figures are (c) Dreams Inc. Personal use only.
