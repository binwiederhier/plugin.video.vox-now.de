__author__ = 'bromix'

from .. import constants


class ViewManager(object):
    SKIN_DATA = {
        'skin.confluence': [
            {'name': 'List', 'id': 50},
            {'name': 'Big List', 'id': 51},
            {'name': 'Thumbnail', 'id': 500},
            {'name': 'Media info', 'id': 504},
            {'name': 'Media info 2', 'id': 503}
        ]
    }

    def __init__(self, context):
        self._context = context
        pass

    def update_view_mode(self, title, view='default'):
        view_id = -1
        settings = self._context.get_settings()

        skin_data = self.SKIN_DATA.get(self._context.get_ui().get_skin_id(), [])
        if skin_data:
            items = []
            for view_data in skin_data:
                items.append((view_data['name'], view_data['id']))
                pass
            view_id = self._context.get_ui().on_select(title, items)
            pass

        if view_id == -1:
            old_value = settings.get_string(constants.setting.VIEW_X % view, '')
            if old_value:
                result, view_id = self._context.get_ui().on_numeric_input(title, old_value)
                if not result:
                    view_id = -1
                    pass
                pass
            pass

        if view_id > -1:
            settings.set_int(constants.setting.VIEW_X % view, view_id)
            return True

        return False

    pass
