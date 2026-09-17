# Nicole's VS Code themes

Four themes in two families, all generated from one template so they stay
consistent with each other.

| Theme | Mode | Base | Story |
| --- | --- | --- | --- |
| **Smiski Dark** | dark | `#1e2023` | neutral graphite, sage and olive syntax |
| **Smiski Dark Pine** | dark | `#17211e` | clean blue-shifted pine green |
| **Parisian Blush** | light | `#faf1ef` | blush paper, rose and copper syntax |
| **Parisian Blush Noir** | dark | `#221a1c` | deep cocoa plum, macaron pink and champagne |

Switch with **Preferences: Color Theme**. Side-by-side shots are in
`images/variant-comparison.png` and `images/blush-comparison.png`.

## The two palettes

Smiski, drawn from the figures themselves:

| Role | Hex |
| --- | --- |
| Keywords, storage, tags | `#c5cf8f` |
| Strings | `#a8c48a` |
| Functions | `#e9ecc0` |
| Types and classes | `#d7b99a` |
| Numbers and constants | `#c79a72` |

Parisian Blush, sampled from the two reference collages. Light values first,
dark second:

| Role | Light | Noir |
| --- | --- | --- |
| Keywords | `#b0476b` rose | `#e79ab0` macaron pink |
| Strings | `#96603a` copper | `#e0b48c` champagne |
| Functions | `#7d4f7a` plum | `#f2dcd8` pearl |
| Types and classes | `#8a6157` mocha | `#d8b3ae` rosy beige |
| Numbers | `#b2512e` terracotta | `#e59b78` copper |
| The cool note | `#5f6b8a` silver lilac | `#a9a8bd` silver lilac |

## Editing the themes

Do not edit the files in `themes/` by hand. They are generated:

```
python3 build-themes.py
```

`themes/_template.json` is the structure, and every hex in it is a named slot
(see `SLOTS`). Slot names describe the role, such as `kw` or `bg_editor`, not
the colour, because a variant may use an entirely different hue family. Each
entry in `VARIANTS` layers its own values over the defaults:

```
ACCENTS  <-  variant["accents"]  <-  variant["neutrals"]
```

So a variant can override just the background ramp, as the two Smiski themes do,
or the whole palette, as the two Blush themes do. The build also rewrites
`contributes.themes` in `package.json`, so adding a variant to `VARIANTS` is the
only step needed to ship it.

Every build runs 22 contrast checks per theme and fails if any falls below its
floor. Body text needs 4.5:1 and UI chrome needs 3.0:1. Adding a light variant
also needs an `ansi` block, because a light terminal wants its neutral ramp
flipped.

Reload the VS Code window after building so it re-reads the files. A new or
renamed variant does not appear in the theme picker until you do.

## Install

The folder is symlinked into `~/.vscode/extensions/`, so VS Code picks it up on
launch.

## Corner Smiski

VS Code color themes cannot include images, so the Smiski in the bottom-right of
the editor is drawn by the
[Background](https://marketplace.visualstudio.com/items?itemName=shalldie.background)
extension. Its config lives in the user `settings.json` under `background.editor`
and points at `images/corner-smiski.png`.

That config is global, not per-theme, so the Smiski also shows up behind the
Blush themes. Set `background.enabled` to false to turn it off.

## Sidebar cats

`background.sidebar` puts `images/sidebar-cats.png` in the bottom-right of the
file tree. The sidebar is a better home for a picture than the editor is, since
the tree is mostly empty space and short filenames, so nothing has to stay
readable through it.

Two traps in the extension are worth knowing before you touch this config:

- **Opacity above 0.6 is silently reset to 0.1.** The extension clamps the
  top-level `opacity`, so a higher value makes the image nearly vanish rather
  than getting brighter. The per-image `styles` block is applied after the base
  rule and is not clamped, which is where the real value of 0.8 lives.
- **The default blend mode is `screen` on dark themes,** which washes artwork
  out into a pale ghost. The `styles` block sets `mix-blend-mode: normal` so the
  cats look the same whichever theme is active.

The image sits above the tree at a high z-index but ignores clicks, so it never
blocks anything. Raise or lower the `opacity` inside `styles` to taste.

After changing the config, run **Background: Enable and apply the background.**
from the Command Palette and click Reload. The extension patches VS Code's own
files, so nothing takes effect until you do.

Settings worth knowing:

- `background-size` controls how big it is. Currently `175px auto`.
- `useFront: true` draws it over the code instead of behind it, which keeps it
  from being dimmed by the editor background.
- `mix-blend-mode: normal` overrides the extension's default `screen` blend,
  which washes images out on dark themes.

Swap the path for any other cutout in `images/` to change the pose: thinking,
pointing, idea, briefcase or trio.

Because Background patches VS Code, it shows a one-time "installation appears to
be corrupt" notice. Click the gear on it and choose "Don't Show Again".

Smiski figures © Dreams Inc. Personal use only.

## Restoring the setup on a new machine

The themes live in this repo, but the background images are driven by VS Code
settings that do not. `setup/` holds a copy of both.

1. Clone this repo and symlink it into `~/.vscode/extensions/`.
2. Install the Background extension:
   `code --install-extension shalldie.background`
3. Merge `setup/settings.snippet.json` into your user `settings.json`, fixing
   the absolute image paths if the repo lives somewhere else.
4. Copy `setup/keybindings.json` into your user keybindings, which binds
   Cmd+Alt+B to the apply command.
5. **Trust the folder.** This is the step that wastes an afternoon if you miss
   it. The Background extension does not declare support for untrusted
   workspaces, so VS Code disables it completely in Restricted Mode, and its
   command silently does not exist. There is no error message. If the banner
   at the top of the window offers Restricted Mode, click Manage and then Trust.
6. Press Cmd+Alt+B and click Reload.

Repeat step 6 after any change to a `background.*` setting. Nothing takes
effect until the extension re-patches VS Code.

### Turning the corner image on and off

`background.editor.images` holds the corner image and `background.sidebar.images`
holds the cats. Emptying a list switches that one off while leaving the other
alone. The config is global rather than per-theme, so the corner Smiski would
otherwise follow you onto the Blush themes, where it does not belong.
