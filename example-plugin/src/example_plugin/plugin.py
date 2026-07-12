# -*- coding: utf-8 -*-
"""
Enigma2 plugin entry point - the minimum shape every plugin in this feed
follows. Copy this whole example-plugin/ directory out into your own new
repo and start replacing pieces from here.

Enigma2 discovers a plugin by importing this module and calling Plugins().
Everything else (screens, services, config) is normal Python; there is no
special build step beyond what the Makefile does (staging files + tar/ar
into an .ipk).
"""
from __future__ import absolute_import

from Components.ActionMap import ActionMap
from Components.config import ConfigText, ConfigSubsection, config
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen

from . import _

# ---------------------------------------------------------------------------
# Config - persisted in /etc/enigma2/settings as config.plugins.example.*
# ---------------------------------------------------------------------------

if not hasattr(config.plugins, "example"):
    config.plugins.example = ConfigSubsection()

config.plugins.example.greeting = ConfigText(default="Hello from your plugin!", fixed_size=False)


# ---------------------------------------------------------------------------
# Screen - swap this for whatever your plugin actually shows.
# ---------------------------------------------------------------------------

class ExampleScreen(Screen):
    skin = """
    <screen name="ExampleScreen" position="center,center" size="600,150" title="Example Plugin">
        <widget name="message" position="20,20" size="560,110" font="Regular;24" halign="center" valign="center" />
    </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        self["message"] = Label(config.plugins.example.greeting.value)
        self["actions"] = ActionMap(
            ["OkCancelActions"],
            {"ok": self.close, "cancel": self.close},
        )


def main(session, **kwargs):
    session.open(ExampleScreen)


def autostart(reason, **kwargs):
    """reason 0 = Enigma2 startup, 1 = shutdown. Wire up background
    services/timers here if your plugin needs any - this template doesn't."""
    pass


def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="Example Plugin",
            description=_("Template plugin - shows how this feed's plugins are structured"),
            where=PluginDescriptor.WHERE_PLUGINMENU,
            # icon="plugin.png",  # drop a 56x38 PNG next to this file and uncomment
            fnc=main,
        ),
        PluginDescriptor(
            where=PluginDescriptor.WHERE_AUTOSTART,
            fnc=autostart,
        ),
    ]
