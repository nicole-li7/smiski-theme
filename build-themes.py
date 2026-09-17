#!/usr/bin/env python3
"""Generate every theme variant from themes/_template.json.

The template is a working VS Code theme; each hex in it is a named slot (SLOTS).
A variant supplies a colour for every slot by layering:

    ACCENTS  <-  variant["accents"]  <-  variant["neutrals"]

so a variant can override as little as the background ramp or as much as the
whole palette. build() also rewrites contributes.themes in package.json and
prints contrast ratios, so adding a variant here is the only step needed.

Run:  python3 build-themes.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

# template hex -> semantic slot. Slot names describe the ROLE, not the colour,
# because variants are free to use a completely different hue family.
SLOTS = {
    # --- neutrals: backgrounds, chrome, greys ---
    "#12140d": "bg_deep",        # title bar, status bar, section headers
    "#161910": "bg_sunk",        # sidebar, panels, widgets, terminal
    "#1b1e17": "bg_editor",      # editor surface
    "#1f2319": "bg_row_hover",
    "#22261b": "bg_raised",      # current line, hover, chrome borders
    "#262b1e": "bg_sel_idle",    # inactive list selection
    "#2a2e22": "border",
    "#2f3527": "sel_idle",       # inactive editor selection
    "#353b2b": "whitespace",
    "#363b2c": "btn_sec_hover",
    "#3a4030": "border_strong",
    "#3e4632": "sel_active",
    "#4c5640": "sel_strong",
    "#4f5642": "gutter_dim",     # line numbers, indent guides
    "#5f6650": "fg_faint",       # ghost text, ignored files
    "#737b64": "fg_comment",
    "#8a9276": "fg_inlay",
    "#98a08a": "fg_muted",
    "#9ea58c": "fg_operator",    # operators, punctuation
    "#c3c9b0": "fg_soft",        # sidebar text, icons
    "#d8dbc9": "fg_main",
    # --- syntax and UI accents ---
    "#c5cf8f": "kw",             # keywords, storage, tags
    "#d8dfa0": "accent",         # links, badges, headings, active borders
    "#dde3ab": "accent_soft",    # cursor
    "#a8c48a": "str",            # strings, focus border
    "#8ea86e": "fill",           # button fill, peek border
    "#bdd3a3": "str_alt",        # escapes, untracked files
    "#e9ecc0": "fn",             # functions, selected row text
    "#9fc9b4": "type",           # types, classes, interfaces
    "#e6b894": "num",            # numbers, constants, decorators, self
    "#c6cfb0": "prop",           # properties, fields
    "#d4d2ad": "param",
    "#e39a9a": "err",
    "#e0cf92": "warn",
    "#98b8c2": "cool",           # ansi blue, deep brackets, charts
    "#c9aacb": "violet",         # ansi magenta
    "#ecb5b5": "err_light",
    "#b3ccd3": "cool_light",
    "#d9c3da": "violet_light",
    "#b8d8c9": "teal_light",
    "#eef0e4": "fg_bright",
    # --- fixed tints ---
    "#3a2222": "bg_error",
    "#3a3320": "bg_warn",
    "#223a33": "bg_info",
    "#000000": "shadow",
    "#ffffff": "overlay",        # status bar hover wash; black on light themes
}

# Defaults. A variant overrides whatever it needs.
ACCENTS = {
    "kw": "#c5cf8f", "accent": "#d8dfa0", "accent_soft": "#dde3ab",
    "str": "#a8c48a", "fill": "#8ea86e", "str_alt": "#bdd3a3",
    "fn": "#e9ecc0", "type": "#d7b99a", "num": "#c79a72",
    "prop": "#c6cfb0", "param": "#d4d2ad",
    "err": "#e39a9a", "warn": "#e0cf92", "cool": "#98b8c2", "violet": "#c9aacb",
    "err_light": "#ecb5b5", "cool_light": "#b3ccd3", "violet_light": "#d9c3da",
    "teal_light": "#b8d8c9", "fg_bright": "#eef0e4",
    "cyan": "#9fc9b4",           # terminal ANSI cyan slot
    "info": "#a9c7bb",           # info diagnostics, kept off the type/warn pair
    "bg_error": "#3a2222", "bg_warn": "#3a3320", "bg_info": "#223a33",
    "shadow": "#000000", "overlay": "#ffffff",
}

SMISKI_ACCENTS = {}  # the default ACCENTS already are the Smiski palette

# Sampled from the two Dior/Paris reference collages: blush cream, rosy beige,
# taupe, mocha, copper, and one whisper of silver-lilac.
BLUSH_LIGHT_ACCENTS = {
    "kw": "#b0476b",             # rose
    "accent": "#ab4a64",         # deep rose, also badge and button-adjacent fills
    "accent_soft": "#c05d7a",
    "str": "#96603a",            # muted copper
    "fill": "#9c4a61",
    "str_alt": "#a86c3e",
    "fn": "#7d4f7a",             # plum, the one cool-leaning warm
    "type": "#8a6157",           # mocha taupe
    "num": "#b2512e",            # terracotta
    "prop": "#7b5c5c",
    "param": "#886666",
    "err": "#b1362c",
    "warn": "#8a6413",
    "cool": "#5f6b8a",           # silver lilac, darkened
    "violet": "#8a5580",
    "err_light": "#c25248",
    "cool_light": "#76819c",
    "violet_light": "#9d6d94",
    "teal_light": "#4f7d78",
    "fg_bright": "#2f2422",
    "cyan": "#3f6f69",
    "info": "#5c6382",
    "bg_error": "#f7dedb", "bg_warn": "#f6ead2", "bg_info": "#dfe2ef",
    "shadow": "#000000", "overlay": "#000000",
}

BLUSH_DARK_ACCENTS = {
    "kw": "#e79ab0",             # macaron pink
    "accent": "#f0b3c2",
    "accent_soft": "#f6c8d3",
    "str": "#e0b48c",            # champagne
    "fill": "#c4788e",
    "str_alt": "#ecc9a6",
    "fn": "#f2dcd8",             # pearl cream
    "type": "#d8b3ae",           # rosy beige
    "num": "#e59b78",            # copper
    "prop": "#d5bcbf",
    "param": "#c9a9ae",
    "err": "#e8828a",
    "warn": "#e0b56a",
    "cool": "#a9a8bd",           # silver lilac
    "violet": "#c9a3c6",
    "err_light": "#f0a0a6",
    "cool_light": "#c2c1d2",
    "violet_light": "#dcbdd9",
    "teal_light": "#b4d2cc",
    "fg_bright": "#faf0f0",
    "cyan": "#9ec4bd",
    "info": "#b6b2c6",
    "bg_error": "#3d2124", "bg_warn": "#3a2f1d", "bg_info": "#26243a",
    "shadow": "#000000", "overlay": "#ffffff",
}

VARIANTS = {
    "smiski-dark": {
        "label": "Smiski Dark", "file": "smiski-dark-color-theme.json",
        "type": "dark", "ui": "vs-dark", "accents": SMISKI_ACCENTS,
        "neutrals": {  # neutral graphite, no green cast in the chrome
            "bg_deep": "#141517", "bg_sunk": "#191a1d", "bg_editor": "#1e2023",
            "bg_row_hover": "#212327", "bg_raised": "#25272b", "bg_sel_idle": "#2a2c31",
            "border": "#2c2e33", "sel_idle": "#32353b", "whitespace": "#3a3d44",
            "btn_sec_hover": "#383b41", "border_strong": "#3d4046", "sel_active": "#3b3f46",
            "sel_strong": "#484d55", "gutter_dim": "#666c76", "fg_faint": "#666b73",
            "fg_comment": "#838a7b", "fg_inlay": "#8b9184", "fg_muted": "#9aa096",
            "fg_operator": "#a3a99f", "fg_soft": "#c5c9c0", "fg_main": "#dcdfd6",
        },
    },
    "smiski-pine": {
        "label": "Smiski Dark Pine", "file": "smiski-pine-color-theme.json",
        "type": "dark", "ui": "vs-dark", "accents": SMISKI_ACCENTS,
        "neutrals": {  # clean blue-shifted green, not the yellow-green that read as swamp
            "bg_deep": "#0e1613", "bg_sunk": "#121c19", "bg_editor": "#17211e",
            "bg_row_hover": "#1a2522", "bg_raised": "#1e2a26", "bg_sel_idle": "#22302b",
            "border": "#24322d", "sel_idle": "#2a3a34", "whitespace": "#31433c",
            "btn_sec_hover": "#2c3c36", "border_strong": "#35473f", "sel_active": "#2f423a",
            "sel_strong": "#3b5049", "gutter_dim": "#577065", "fg_faint": "#5e736a",
            "fg_comment": "#799085", "fg_inlay": "#84998f", "fg_muted": "#93a89e",
            "fg_operator": "#9db0a6", "fg_soft": "#c0cbc4", "fg_main": "#d7ded7",
        },
    },
    "blush": {
        "label": "Parisian Blush", "file": "blush-color-theme.json",
        "type": "light", "ui": "vs", "accents": BLUSH_LIGHT_ACCENTS,
        "neutrals": {  # blush cream paper
            "bg_deep": "#e7d7d5", "bg_sunk": "#f1e4e2", "bg_editor": "#faf1ef",
            "bg_row_hover": "#f4e7e4", "bg_raised": "#f3e5e3", "bg_sel_idle": "#e9dad8",
            "border": "#e4d2d0", "sel_idle": "#eddcdc", "whitespace": "#d8c4c2",
            "btn_sec_hover": "#e6d5d3", "border_strong": "#d7c3c1", "sel_active": "#e9d5d6",
            "sel_strong": "#dfc6c8", "gutter_dim": "#9f8583", "fg_faint": "#97807e",
            "fg_comment": "#7f6968", "fg_inlay": "#8e7674", "fg_muted": "#7d6664",
            "fg_operator": "#705957", "fg_soft": "#5a4846", "fg_main": "#453634",
        },
        # a light terminal needs its neutral ramp flipped
        "ansi": {"terminal.ansiBlack": "#453634", "terminal.ansiBrightBlack": "#7d6664",
                 "terminal.ansiWhite": "#d8c4c2", "terminal.ansiBrightWhite": "#fcf5f3"},
    },
    "blush-noir": {
        "label": "Parisian Blush Noir", "file": "blush-noir-color-theme.json",
        "type": "dark", "ui": "vs-dark", "accents": BLUSH_DARK_ACCENTS,
        "neutrals": {  # deep cocoa plum
            "bg_deep": "#171113", "bg_sunk": "#1c1517", "bg_editor": "#221a1c",
            "bg_row_hover": "#251d1f", "bg_raised": "#2a2124", "bg_sel_idle": "#2f2528",
            "border": "#332629", "sel_idle": "#3a2c30", "whitespace": "#4a393d",
            "btn_sec_hover": "#3d2f32", "border_strong": "#46353a", "sel_active": "#45333a",
            "sel_strong": "#573f47", "gutter_dim": "#7f6168", "fg_faint": "#7d6169",
            "fg_comment": "#a2868d", "fg_inlay": "#a98d94", "fg_muted": "#b89aa1",
            "fg_operator": "#c2a8ae", "fg_soft": "#ddc9cd", "fg_main": "#f0e2e3",
        },
    },
}


def post_fix(theme, palette, ansi):
    """Colours that must be set from named slots rather than substituted."""
    c = theme["colors"]
    ramp = [palette[n] for n in ("accent", "type", "str", "num", "violet", "cool")]
    for i, col in enumerate(ramp, start=1):
        c[f"editorBracketHighlight.foreground{i}"] = col
    for i, col in enumerate(ramp[:3], start=1):
        c[f"editorBracketPairGuide.activeBackground{i}"] = col + "66"
    # terminals need a real cyan slot or ANSI output reads wrong
    c["terminal.ansiCyan"] = palette["cyan"]
    c["charts.blue"] = palette["cool"]
    # info diagnostics: a distinct slot so info != warning != type
    for k in ["inputValidation.infoBorder", "editorInfo.foreground",
              "editorOverviewRuler.infoForeground", "notificationsInfoIcon.foreground",
              "problemsInfoIcon.foreground", "debugConsole.infoForeground",
              "editorMarkerNavigationInfo.background"]:
        if k in c:
            c[k] = palette["info"]
    c.update(ansi)
    return theme


def luminance(hex_):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(fg, bg):
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


# (foreground slot, background slot, minimum). Body text wants 4.5, UI chrome 3.0.
CHECKS = [(n, "bg_editor", 4.5) for n in
          ("fg_main", "fg_comment", "kw", "str", "fn", "type", "num", "prop",
           "param", "err", "warn", "cool", "violet")] + [
    ("fg_soft", "bg_sunk", 4.5),
    ("fg_main", "bg_sunk", 4.5),
    ("fg_soft", "bg_deep", 4.5),
    ("bg_deep", "fill", 3.0),        # button label on button fill
    ("bg_deep", "accent", 3.0),      # badge label on badge
    ("bg_deep", "err", 3.0),         # status bar error item
    ("bg_deep", "warn", 3.0),        # status bar warning item
    ("fn", "sel_active", 3.0),       # selected list row label
    ("gutter_dim", "bg_editor", 3.0),
]


def build():
    template = open(os.path.join(HERE, "themes", "_template.json")).read()
    unknown = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}", template)} - set(SLOTS)
    if unknown:
        raise SystemExit(f"template has hexes with no slot: {sorted(unknown)}")

    contributes, failures = [], []
    for var in VARIANTS.values():
        palette = {**ACCENTS, **var.get("accents", {}), **var["neutrals"]}
        out = re.sub(r"#[0-9a-fA-F]{6}",
                     lambda m: palette[SLOTS[m.group(0).lower()]], template)
        theme = post_fix(json.loads(out), palette, var.get("ansi", {}))
        theme["name"] = var["label"]
        theme["type"] = var["type"]
        with open(os.path.join(HERE, "themes", var["file"]), "w") as fh:
            json.dump(theme, fh, indent=2)
            fh.write("\n")
        contributes.append({"label": var["label"], "uiTheme": var["ui"],
                            "path": "./themes/" + var["file"]})

        print(f"\n{var['label']}  ({var['type']}, base {palette['bg_editor']})")
        for fg, bg, floor in CHECKS:
            r = contrast(palette[fg], palette[bg])
            if r < floor:
                failures.append((var["label"], fg, bg, r, floor))
                print(f"    {fg:>12} on {bg:<12} {r:5.2f}:1   BELOW {floor}")
        if not any(f[0] == var["label"] for f in failures):
            worst = min((contrast(palette[f], palette[b]), f, b) for f, b, _ in CHECKS)
            print(f"    all {len(CHECKS)} checks pass, tightest {worst[0]:.2f}:1"
                  f" ({worst[1]} on {worst[2]})")

    pkg_path = os.path.join(HERE, "package.json")
    pkg = json.load(open(pkg_path))
    pkg["contributes"]["themes"] = contributes
    with open(pkg_path, "w") as fh:
        json.dump(pkg, fh, indent=2)
        fh.write("\n")

    print(f"\nwrote {len(contributes)} themes and updated package.json")
    if failures:
        raise SystemExit(f"\n{len(failures)} contrast check(s) failed")


if __name__ == "__main__":
    build()
