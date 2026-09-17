#!/usr/bin/env python3
"""Generate the Smiski theme variants from themes/_template.json.

The template is a working VS Code theme; every hex in it is treated as a
semantic slot (see SLOTS). Each variant supplies a colour per slot.
Run:  python3 build-themes.py
"""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))

# template hex -> semantic slot name
SLOTS = {
    # --- neutrals: backgrounds, chrome, greys (differ per variant) ---
    "#12140d": "bg_deep",        # title bar, status bar, section headers
    "#161910": "bg_sunk",        # sidebar, panels, widgets, terminal
    "#1b1e17": "bg_editor",      # editor surface
    "#1f2319": "bg_row_hover",   # settings row hover
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
    # --- accents (shared across variants) ---
    "#c5cf8f": "olive",          # keywords, storage, tags
    "#d8dfa0": "olive_bright",   # links, badges, headings, active borders
    "#dde3ab": "olive_pale",     # cursor
    "#a8c48a": "sage",           # strings, focus border, buttons
    "#8ea86e": "sage_deep",      # button fill, peek border
    "#bdd3a3": "sage_light",     # escapes, untracked files
    "#e9ecc0": "cream",          # functions, selected row text
    "#9fc9b4": "tan",            # types, classes, interfaces (was mint)
    "#e6b894": "caramel",        # numbers, constants, decorators, self (was peach)
    "#c6cfb0": "prop",           # properties, fields
    "#d4d2ad": "param",          # parameters
    "#e39a9a": "rose",           # errors
    "#e0cf92": "amber",          # warnings, modified
    "#98b8c2": "slate",          # ansi blue, deep brackets
    "#c9aacb": "mauve",          # ansi magenta
    "#ecb5b5": "rose_light",
    "#b3ccd3": "slate_light",
    "#d9c3da": "mauve_light",
    "#b8d8c9": "teal_light",
    "#eef0e4": "white_soft",
    # --- fixed tints, identical in both variants ---
    "#3a2222": "bg_error",
    "#3a3320": "bg_warn",
    "#223a33": "bg_info",
    "#000000": "black",
    "#ffffff": "white",
}

ACCENTS = {
    "olive": "#c5cf8f", "olive_bright": "#d8dfa0", "olive_pale": "#dde3ab",
    "sage": "#a8c48a", "sage_deep": "#8ea86e", "sage_light": "#bdd3a3",
    "cream": "#e9ecc0", "tan": "#d7b99a", "caramel": "#c79a72",
    "prop": "#c6cfb0", "param": "#d4d2ad",
    "rose": "#e39a9a", "amber": "#e0cf92", "slate": "#98b8c2", "mauve": "#c9aacb",
    "rose_light": "#ecb5b5", "slate_light": "#b3ccd3", "mauve_light": "#d9c3da",
    "teal_light": "#b8d8c9", "white_soft": "#eef0e4",
    "bg_error": "#3a2222", "bg_warn": "#3a3320", "bg_info": "#223a33",
    "black": "#000000", "white": "#ffffff",
}

VARIANTS = {
    # Neutral graphite. No green cast in the chrome; the greens live in the syntax.
    "gray": {
        "label": "Smiski Dark",
        "file": "smiski-dark-color-theme.json",
        "neutrals": {
            "bg_deep": "#141517", "bg_sunk": "#191a1d", "bg_editor": "#1e2023",
            "bg_row_hover": "#212327", "bg_raised": "#25272b", "bg_sel_idle": "#2a2c31",
            "border": "#2c2e33", "sel_idle": "#32353b", "whitespace": "#3a3d44",
            "btn_sec_hover": "#383b41", "border_strong": "#3d4046", "sel_active": "#3b3f46",
            "sel_strong": "#484d55", "gutter_dim": "#555a62", "fg_faint": "#666b73",
            "fg_comment": "#838a7b", "fg_inlay": "#8b9184", "fg_muted": "#9aa096",
            "fg_operator": "#a3a99f", "fg_soft": "#c5c9c0", "fg_main": "#dcdfd6",
        },
    },
    # Clean pine. Blue-shifted green rather than the yellow-green that read as swamp.
    "pine": {
        "label": "Smiski Dark Pine",
        "file": "smiski-pine-color-theme.json",
        "neutrals": {
            "bg_deep": "#0e1613", "bg_sunk": "#121c19", "bg_editor": "#17211e",
            "bg_row_hover": "#1a2522", "bg_raised": "#1e2a26", "bg_sel_idle": "#22302b",
            "border": "#24322d", "sel_idle": "#2a3a34", "whitespace": "#31433c",
            "btn_sec_hover": "#2c3c36", "border_strong": "#35473f", "sel_active": "#2f423a",
            "sel_strong": "#3b5049", "gutter_dim": "#4d635a", "fg_faint": "#5e736a",
            "fg_comment": "#799085", "fg_inlay": "#84998f", "fg_muted": "#93a89e",
            "fg_operator": "#9db0a6", "fg_soft": "#c0cbc4", "fg_main": "#d7ded7",
        },
    },
}

# Applied after substitution so these stay distinguishable from the tan/caramel pair.
def post_fix(theme):
    c = theme["colors"]
    ramp = ["#d8dfa0", "#d7b99a", "#a8c48a", "#c79a72", "#c9aacb", "#98b8c2"]
    for i, col in enumerate(ramp, start=1):
        c[f"editorBracketHighlight.foreground{i}"] = col
    for i, col in enumerate(ramp[:3], start=1):
        c[f"editorBracketPairGuide.activeBackground{i}"] = col + "66"
    # terminals need a real cyan slot or ANSI output reads wrong
    c["terminal.ansiCyan"] = "#9fc9b4"
    c["charts.blue"] = "#98b8c2"
    # info diagnostics: keep a cool-ish slot so info != warning != type
    info = "#a9c7bb"
    for k in ["inputValidation.infoBorder", "editorInfo.foreground",
              "editorOverviewRuler.infoForeground", "notificationsInfoIcon.foreground",
              "problemsInfoIcon.foreground", "debugConsole.infoForeground",
              "editorMarkerNavigation.infoBackground", "editorMarkerNavigationInfo.background"]:
        if k in c:
            c[k] = info
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


def build():
    template = open(os.path.join(HERE, "themes", "_template.json")).read()
    unknown = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}", template)} - set(SLOTS)
    if unknown:
        raise SystemExit(f"template has hexes with no slot: {sorted(unknown)}")

    for key, var in VARIANTS.items():
        palette = {**ACCENTS, **var["neutrals"]}
        out = re.sub(
            r"#[0-9a-fA-F]{6}",
            lambda m: palette[SLOTS[m.group(0).lower()]],
            template,
        )
        theme = post_fix(json.loads(out))
        theme["name"] = var["label"]
        path = os.path.join(HERE, "themes", var["file"])
        with open(path, "w") as fh:
            json.dump(theme, fh, indent=2)
            fh.write("\n")

        bg = palette["bg_editor"]
        checks = ["fg_main", "fg_comment", "olive", "sage", "cream", "tan",
                  "caramel", "prop", "param", "rose", "amber"]
        worst = min((contrast(palette[n], bg), n) for n in checks)
        print(f"{var['label']:<18} bg {bg}  lowest contrast {worst[0]:.2f}:1 ({worst[1]})")
        for n in checks:
            r = contrast(palette[n], bg)
            flag = "  <-- under 4.5" if r < 4.5 else ""
            print(f"    {n:<12} {palette[n]}  {r:5.2f}:1{flag}")


if __name__ == "__main__":
    build()
