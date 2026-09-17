# Smiski Dark

Dark VS Code themes in Smiski colours: sage and olive greens for the syntax,
warm tan and caramel for types and numbers.

Two variants ship in the extension, identical except for the background ramp:

| Variant | Base | Editor background |
| --- | --- | --- |
| **Smiski Dark** | neutral graphite, no green cast in the chrome | `#1e2023` |
| **Smiski Dark Pine** | clean blue-shifted pine green | `#17211e` |

Switch with **Preferences: Color Theme**. See `images/variant-comparison.png`
for the two side by side.

## Accent palette

Shared by both variants.

| Role | Hex |
| --- | --- |
| Keywords, storage, tags | `#c5cf8f` |
| Links, badges, headings, active borders | `#d8dfa0` |
| Strings, focus border | `#a8c48a` |
| Button fill, peek border | `#8ea86e` |
| Functions and methods | `#e9ecc0` |
| Types, classes, interfaces | `#d7b99a` |
| Numbers, constants, decorators, `this` | `#c79a72` |
| Properties and fields | `#c6cfb0` |
| Parameters | `#d4d2ad` |
| Errors | `#e39a9a` |
| Warnings, modified files | `#e0cf92` |

Every accent clears 4.5:1 contrast against both backgrounds. `build-themes.py`
prints the ratios each time it runs.

## Editing the themes

Do not edit the files in `themes/` by hand. They are generated:

```
python3 build-themes.py
```

`themes/_template.json` is the structure, and every hex in it is a named slot
(see `SLOTS` in the build script). `ACCENTS` holds the colours shared by both
variants, and each entry in `VARIANTS` supplies its own background ramp. Change
a colour in one place and both themes stay in sync.

Reload the VS Code window after building so it re-reads the files.

## Install

The folder is symlinked into `~/.vscode/extensions/`, so VS Code picks it up on
launch. Adding or renaming a variant needs a window reload before it shows up in
the theme picker.

## Corner Smiski

VS Code color themes cannot include images, so the Smiski in the bottom-right of
the editor is drawn by the
[Background](https://marketplace.visualstudio.com/items?itemName=shalldie.background)
extension. Its config lives in the user `settings.json` under `background.editor`
and points at `images/corner-smiski.png`.

After changing that config, run **Background: Enable and apply the background.**
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
