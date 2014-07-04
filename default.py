# -*- coding: utf-8 -*-

import xbmcplugin
import xbmcgui
import xbmcaddon

import os

import pydevd
pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)

from bromixbmc import Bromixbmc
bromixbmc = Bromixbmc("plugin.video.vox_now", sys.argv)

import rtlinteractive

__now_client__ = rtlinteractive.now.Client(rtlinteractive.now.__CONFIG_VOX_NOW__)

__FANART__ = os.path.join(bromixbmc.Addon.Path, "fanart.jpg")
__ICON_HIGHLIGHTS__ = os.path.join(bromixbmc.Addon.Path, "resources/media/highlight.png")
__ICON_LIBRARY__ = os.path.join(bromixbmc.Addon.Path, "resources/media/library.png")
__ICON_FAVOURITES__ = os.path.join(bromixbmc.Addon.Path, "resources/media/pin.png")

__ACTION_SHOW_LIBRARY__ = 'showLibrary'
__ACTION_SHOW_EPISODES__ = 'showEpisodes'

__SETTING_SHOW_FANART__ = bromixbmc.Addon.getSetting('showFanart')=="true"

def showIndex():
    # add 'Sendungen A-Z'
    params = {'action': __ACTION_SHOW_LIBRARY__}
    bromixbmc.addDir(bromixbmc.Addon.localize(30000), params = params, thumbnailImage=__ICON_LIBRARY__, fanart=__FANART__)
    
    xbmcplugin.endOfDirectory(bromixbmc.Addon.Handle)
    return True

def showLibrary():
    def _sort_key(d):
        return d[1].get('formatlong', '').lower()
     
    shows = __now_client__.getShows()
    shows = shows.get('content', {})
    shows = shows.get('formatlist', {})
    
    sorted_shows = sorted(shows.items(), key=_sort_key, reverse=False)
    
    for item in sorted_shows:
        if len(item)>=2:
            show = item[1]
            title = show.get('formatlong', None)
            id = show.get('formatid', None)
            free_episodes = int(show.get('free_episodes', '0'))
            fanart = None
            if __SETTING_SHOW_FANART__:
                fanart = show.get('bigaufmacherimg', '')
                fanart = fanart.replace('/640x360/', '/768x432/')
                
            thumbnailImage = show.get('biggalerieimg', '')
            
            if free_episodes>=1 and title!=None and id!=None:
                params = {'action': __ACTION_SHOW_EPISODES__,
                          'id': id}
                bromixbmc.addDir(title, params=params, thumbnailImage=thumbnailImage, fanart=fanart)
    
    xbmcplugin.endOfDirectory(bromixbmc.Addon.Handle)
    return True

def showEpisodes(id):
    episodes = __now_client__.getEpisodes(id)
    episodes = episodes.get('content', {})
    page = episodes.get('page', '1')
    maxpage = episodes.get('maxpage', '1')
    episodes = episodes.get('filmlist', {})
    
    for key in episodes:
        episode = episodes.get(key, None)
        if episode!=None:
            title = episode.get('headlinelong', None)
            id = episode.get('id', None)
            if title!=None and id!=None:
                params = {'action': '',
                          'id': id}
                bromixbmc.addVideoLink(title, params = params)
    xbmcplugin.endOfDirectory(bromixbmc.Addon.Handle)
    return True

action = bromixbmc.getParam('action')
id = bromixbmc.getParam('id')

if action == __ACTION_SHOW_LIBRARY__:
    showLibrary()
elif action == __ACTION_SHOW_EPISODES__ and id!=None:
    showEpisodes(id)
else:
    showIndex()