# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Standard Enigma2 gettext hookup so _("...") works for translations.
# Real plugins keep .po/.mo files under locale/<lang>/LC_MESSAGES/ and load
# them here; this stub just falls back to the identity function.
def _(text):
    return text
