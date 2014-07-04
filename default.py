# -*- coding: utf-8 -*-

import xbmcplugin
import xbmcgui
import xbmcaddon

import os

import pydevd
pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)

from bromixbmc import Bromixbmc
bromixbmc = Bromixbmc("plugin.video.vox_now", sys.argv)

__FANART__ = os.path.join(bromixbmc.Addon.Path, "fanart.jpg")
__ICON_HIGHLIGHTS__ = os.path.join(bromixbmc.Addon.Path, "resources/media/highlight.png")
__ICON_LIBRARY__ = os.path.join(bromixbmc.Addon.Path, "resources/media/library.png")
__ICON_FAVOURITES__ = os.path.join(bromixbmc.Addon.Path, "resources/media/pin.png")

__ACTION_SHOW_LIBRARY__ = 'showLibrary'

def showIndex():
    # add 'Sendungen A-Z'
    params = {'action': __ACTION_SHOW_LIBRARY__}
    bromixbmc.addDir(bromixbmc.Addon.localize(30000), params = params, thumbnailImage=__ICON_LIBRARY__, fanart=__FANART__)
    
    xbmcplugin.endOfDirectory(bromixbmc.Addon.Handle)
    return True

def showLibrary():
    xbmcplugin.endOfDirectory(bromixbmc.Addon.Handle)
    return True

action = bromixbmc.getParam('action')

if action == __ACTION_SHOW_LIBRARY__:
    showLibrary()
else:
    showIndex()