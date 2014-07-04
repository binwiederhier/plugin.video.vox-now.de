# -*- coding: utf-8 -*-

import xbmcplugin
import xbmcgui
import xbmcaddon

import os
import re

#import pydevd
#pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)

from bromixbmc import Bromixbmc
bromixbmc = Bromixbmc("plugin.video.vox_now", sys.argv)

import rtlinteractive

__now_client__ = rtlinteractive.now.Client(rtlinteractive.now.__CONFIG_VOX_NOW__)

__FANART__ = os.path.join(bromixbmc.Addon.Path, "fanart.jpg")
__ICON_HIGHLIGHTS__ = os.path.join(bromixbmc.Addon.Path, "resources/media/highlight.png")
__ICON_LIBRARY__ = os.path.join(bromixbmc.Addon.Path, "resources/media/library.png")
__ICON_FAVOURITES__ = os.path.join(bromixbmc.Addon.Path, "resources/media/pin.png")

__ACTION_SHOW_LIBRARY__ = 'showLibrary'
__ACTION_SHOW_TIPS__ = 'showTips'
__ACTION_SHOW_NEWEST__ = 'showNewest'
__ACTION_SHOW_TOP10__ = 'showTop10'
__ACTION_SHOW_EPISODES__ = 'showEpisodes'

__SETTING_SHOW_FANART__ = bromixbmc.Addon.getSetting('showFanart')=="true"
__SETTING_SHOW_PUCLICATION_DATE__ = bromixbmc.Addon.getSetting('showPublicationDate')=="true"

def showIndex():
    # add 'Sendungen A-Z'
    params = {'action': __ACTION_SHOW_LIBRARY__}
    bromixbmc.addDir(bromixbmc.Addon.localize(30000), params = params, thumbnailImage=__ICON_LIBRARY__, fanart=__FANART__)
    
    params = {'action': __ACTION_SHOW_TIPS__}
    bromixbmc.addDir(bromixbmc.Addon.localize(30001), params = params, thumbnailImage=__ICON_HIGHLIGHTS__, fanart=__FANART__)
    
    params = {'action': __ACTION_SHOW_NEWEST__}
    bromixbmc.addDir(bromixbmc.Addon.localize(30002), params = params, thumbnailImage=__ICON_HIGHLIGHTS__, fanart=__FANART__)
    
    params = {'action': __ACTION_SHOW_TOP10__}
    bromixbmc.addDir(bromixbmc.Addon.localize(30003), params = params, thumbnailImage=__ICON_HIGHLIGHTS__, fanart=__FANART__)
    
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

def _listEpisodes(episodes, func={}):
    xbmcplugin.setContent(bromixbmc.Addon.Handle, 'episodes')
    
    episodes = episodes.get('content', {})
    page = episodes.get('page', '1')
    maxpage = episodes.get('maxpage', '1')
    episodes = episodes.get('filmlist', {})
        
    sorted_episodes = sorted(episodes.items(), key=func.get('sort_func', None), reverse=func.get('sort_reverse', True))
    
    for item in sorted_episodes:
        if len(item)>=2:
            episode = item[1]
            title = func.get('title_func', None)(episode)
            id = episode.get('id', None)
            free = episode.get('free', '0')
            duration = episode.get('duration', '00:00:00')
            match = re.compile('(\d*)\:(\d*)\:(\d*)', re.DOTALL).findall(duration)
            if match!=None and len(match[0])>=3:
                hours = int(match[0][0])
                minutes = hours*60 + int(match[0][1]) 
                duration = str(minutes)

            year = ''
            aired = ''
            match = re.compile('(\d*)\-(\d*)\-(\d*) (\d*)\:(\d*)\:(\d*)', re.DOTALL).findall(episode.get('sendestart', '0000-00-00'))
            if match!=None and len(match[0])>=3:
                year = match[0][0]
                aired = match[0][0]+"-"+match[0][1]+"-"+match[0][2]
                if __SETTING_SHOW_PUCLICATION_DATE__:
                    date_format = xbmc.getRegion('dateshort')
                    
                    date_format = date_format.replace('%d', match[0][0])
                    date_format = date_format.replace('%m', match[0][1])
                    date_format = date_format.replace('%Y', match[0][2])
                    title = date_format+" - "+title
                
            fanart = None
            if __SETTING_SHOW_FANART__:
                fanart = episode.get('bigaufmacherimg', '')
                fanart = fanart.replace('/640x360/', '/768x432/')
                
            thumbnailImage = __now_client__.getEpisodeThumbnailImage(episode)

            additionalInfoLabels = {'duration': duration,
                                    'plot': episode.get('articleshort', ''),
                                    'episode': episode.get('episode', ''),
                                    'season': episode.get('season', ''),
                                    'year': year,
                                    'aired': aired}
                
            if free=='1' and title!=None and id!=None:
                params = {'action': '',
                          'id': id}
                bromixbmc.addVideoLink(title, params=params, thumbnailImage=thumbnailImage, fanart=fanart, additionalInfoLabels=additionalInfoLabels)
    xbmcplugin.endOfDirectory(bromixbmc.Addon.Handle)
    return True

def showTips():
    def _sort_key(d):
        return d[0]
    
    def _get_title(d):
        return d.get('formatlong', '')+" - "+d.get('headlinelong', '')
    
    episodes = __now_client__.getTips()
    _listEpisodes(episodes, func={'sort_func': _sort_key,
                                  'sort_reverse': False,
                                  'title_func': _get_title}
                  )
    
def showNewest():
    def _sort_key(d):
        return d[0]
    
    def _get_title(d):
        return d.get('formatlong', '')+" - "+d.get('headlinelong', '')
    
    episodes = __now_client__.getNewest()
    _listEpisodes(episodes, func={'sort_func': _sort_key,
                                  'sort_reverse': False,
                                  'title_func': _get_title}
                  )
    
def showTop10():
    def _sort_key(d):
        return d[0]
    
    def _get_title(d):
        return d.get('formatlong', '')+" - "+d.get('headlinelong', '')
    
    episodes = __now_client__.getTop10()
    _listEpisodes(episodes, func={'sort_func': _sort_key,
                                  'sort_reverse': False,
                                  'title_func': _get_title}
                  )

def showEpisodes(id):
    def _sort_key(d):
        return d[1].get('sendestart', '').lower()
    
    def _get_title(d):
        return d.get('headlinelong', '')
    
    episodes = __now_client__.getEpisodes(id)
    _listEpisodes(episodes, func={'sort_func': _sort_key,
                                  'sort_reverse': True,
                                  'title_func': _get_title}
                  )

action = bromixbmc.getParam('action')
id = bromixbmc.getParam('id')

if action == __ACTION_SHOW_LIBRARY__:
    showLibrary()
elif action == __ACTION_SHOW_TIPS__:
    showTips()
elif action == __ACTION_SHOW_NEWEST__:
    showNewest()
elif action == __ACTION_SHOW_TOP10__:
    showTop10()
elif action == __ACTION_SHOW_EPISODES__ and id!=None:
    showEpisodes(id)
else:
    showIndex()