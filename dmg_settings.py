# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import plistlib
import os.path

# Use like this: dmgbuild -s settings.py "Test Volume" test.dmg

application = defines.get('app', './dist/webp-converter.app')
appname = os.path.basename(application)

def icon_from_app(app_path):
    plist_path = os.path.join(app_path, 'Contents', 'Info.plist')
    with open(plist_path, 'rb') as fp:
        plist = plistlib.load(fp)
    icon_name = plist['CFBundleIconFile']
    icon_root,icon_ext = os.path.splitext(icon_name)
    if not icon_ext:
        icon_ext = '.icns'
    icon_name = icon_root + icon_ext
    return os.path.join(app_path, 'Contents', 'Resources', icon_name)

# Volume format (see hdiutil create -help)
format = defines.get('format', 'UDBZ')

# Volume size
size = defines.get('size', None)

# Files to include
files = [ application ]

# Symlinks to create
symlinks = { 'Applications': '/Applications' }

# Volume icon
badge_icon = icon_from_app(application)

# Where to put the icons
icon_locations = {
    appname:        (140, 120),
    'Applications': (500, 120)
    }

# Background
background = 'builtin-arrow'

show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 180

# Window position in ((x, y), (w, h)) format
window_rect = ((100, 100), (640, 280))

# Select the default view; must be one of
#
#    'icon-view'
#    'list-view'
#    'column-view'
#    'coverflow'
#
default_view = 'icon-view'

# General view configuration
show_icon_preview = False

# Set these to True to force inclusion of icon/list view settings (otherwise
# we only include settings for the default view)
include_icon_view_settings = 'auto'
include_list_view_settings = 'auto'

# Icon view configuration
arrange_by = None
grid_offset = (0, 0)
grid_spacing = 100
scroll_position = (0, 0)
label_pos = 'bottom'
text_size = 16
icon_size = 128