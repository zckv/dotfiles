#!/usr/bin/python

from libqtile import bar, layout, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget 
from qtile_extras.widget.decorations import RectDecoration, PowerLineDecoration
import os
import subprocess

mod = "mod4"
terminal = "kitty"

theme_argonaut = [ 
    '#23232300',    # Black (Host)
    '#FF000F',    # Red (Syntax string)
    '#8CE10B',    # Green (Command)
    '#FFB900',    # Yellow (Command second)
    '#008DF8',    # Blue (Path)
    '#6D43A6',    # Magenta (Syntax var)
    '#00D8EB',    # Cyan (Prompt)
    '#FFFFFF',    # White
    '#444444',    # Bright Black
    '#FF2740',    # Bright Red (Command error)
    '#ABE15B',    # Bright Green (Exec)
    '#FFD242',    # Bright Yellow
    '#0092FF',    # Bright Blue (Folder)
    '#9A5FEB',    # Bright Magenta
    '#67FFF0',    # Bright Cyan
    '#FFFFFF',    # Bright White
]

colors = {
    "black": theme_argonaut[0], 
    "red": theme_argonaut[1], 
    "green": theme_argonaut[2], 
    "yellow": theme_argonaut[3], 
    "blue": theme_argonaut[4], 
    "magenta": theme_argonaut[5], 
    "cyan": theme_argonaut[6], 
    "white": theme_argonaut[7], 
    "bblack": theme_argonaut[8], 
    "bred": theme_argonaut[9], 
    "bgreen": theme_argonaut[10], 
    "byellow": theme_argonaut[11], 
    "bblue": theme_argonaut[12], 
    "bmagenta": theme_argonaut[13], 
    "bcyan": theme_argonaut[14], 
    "bwhite": theme_argonaut[15], 
}

#[
#        ["#00000000", "#00000000", "#00000000"],     # color 0
#        ["#2e3440", "#2e3440", "#2e3440"], # color 1
#        # ["#32333C", "#32333C", "#32333C"], # color 1
#        ["#65bdd8", "#65bdd8", "#65bdd8"], # color 2
#        ["#bc7cf7", "#a269cf", "#bc7cf7"], # color 3
#        ["#aed1dc", "#98B7C0", "#aed1dc"], # color 4
#        ["#f3f4f5", "#f3f4f5", "#f3f4f5"], # color 5
#        ["#bb94cc", "#AB87BB", "#bb94cc"], # color 6
#        ["#9859B3", "#8455A8", "#9859B3"], # color 7
#        ["#744B94", "#694486", "#744B94"], # color 8
#        ["#0ee9af", "#0ee9af", "#0ee9af"] # color 9
#]

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
        ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5")),
]

groups = [Group(i) for i in "123456789"]
azerty_keys_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "minus", "egrave", "underscore", "ccedilla"]
for group, key in zip(groups, azerty_keys_names):
    name = group.name
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                key,
                lazy.group[name].toscreen(),
                desc="Switch to group {}".format(name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                key,
                #azerty_numbers[int(i.name)],
                lazy.window.togroup(name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

decor = {
    "decorations": [
#        RectDecoration(colour=colors["blue"], radius=5, filled=False, padding_y=10)
        PowerLineDecoration(path='forward_slash'),
    ],
}

widget_defaults = dict(
    background=colors["black"],
    foreground=colors["white"],
    font="sans",
    fontsize=12,
    padding=5,
    decorations = [
        PowerLineDecoration(path='forward_slash'),
    ],
)
extension_defaults = widget_defaults.copy()

wsep = widget.Sep(
    decorations=[],
    padding=10,
    linewidth=0,
)


modded_widgets = [
    wsep,
    widget.CPU(
        background=colors["blue"],
        format='{load_percent}%',
        fontsize=16,
    ),
    widget.Memory(
        background=colors["bblue"],
        fontsize=16,
        measure_mem='G',
        format='{MemUsed: .2f} GB',
    ),
    widget.CurrentLayout(
        background=colors["blue"],
        fontsize=15,
    ),
    widget.Prompt(),
    # widget.CurrentLayoutIcon(
    #     scale=0.6,
    # ),
    wsep,
    widget.Spacer(
        decorations=[],
    ),
    widget.GroupBox(
        active=colors["bblue"],
        background=colors["black"],
        block_highlight_text_color=colors["blue"],
        disable_drag=True,
        fontsize=14,
        inactive=colors["bblack"],
        rounded=True,
        highlight_color=colors["white"],
        # highlight_method="line",
        this_current_screen_border=colors["white"],

        blockwidth=2,
        margin_y=5,
        decorations=[],
    ),
    widget.Spacer(
        decorations=[],
    ),
    widget.Systray(
        icon_size=30,
        padding=5,
    ),
    widget.PulseVolume(
        background=colors["blue"],
        fontsize=16,
        mouse_callbacks={'Button3': lambda: qtile.cmd_spawn("pavucontrol")},
    ),
#    widget.PulseVolume(
#        background=colors["cyan"],
#        emoji=True,
#        foreground=colors["white"],
#        fontsize=16,
#        mouse_callbacks={'Button3': lambda: qtile.cmd_spawn("pavucontrol")},
#    ),
    widget.Clock(
        decorations=[],
        background=colors["blue"],
        foreground=colors["white"],
        fontsize=16,
        format='%H:%M %d/%m/%y',
    ),
]

screens = [
    Screen(
        top=bar.Bar(
            modded_widgets,
            30,
            background=["#00000000"],
            opacity=1,
            # background=colors[0],
        ),
        wallpaper="/usr/local/wallpapers/black_lp_planet.jpg",
        wallpaper_mode="fill",
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# Run bash on startup
@hook.subscribe.startup_once
def startup_once():
    subprocess.run('/usr/local/config/autostart_once.sh')

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
# wmname = "LG3D"
wmname = "QTile"
