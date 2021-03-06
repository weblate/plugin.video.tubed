# -*- coding: utf-8 -*-
"""
    Copyright (C) 2020 Tubed (plugin.video.tubed)

    This file is part of plugin.video.tubed

    SPDX-License-Identifier: GPL-2.0-only
    See LICENSES/GPL-2.0-only.txt for more information.
"""

import xbmcplugin  # pylint: disable=import-error

from ..constants import MODES
from ..generators.comments import thread_generator
from ..items.next_page import NextPage
from ..lib.url_utils import create_addon_path
from .utils import get_sort_order

DEFAULT_ORDER = 'relevance'


def invoke(context, video_id, page_token='', order=DEFAULT_ORDER):
    if order == 'prompt':
        order = get_sort_order(context)
        order = order or DEFAULT_ORDER
        if order != DEFAULT_ORDER:
            page_token = ''

    payload = context.api.comment_threads(video_id, order=order, page_token=page_token)
    list_items = list(thread_generator(context, payload.get('items', [])))

    page_token = payload.get('nextPageToken')
    if page_token:
        query = {
            'mode': str(MODES.COMMENTS_THREADS),
            'video_id': video_id,
            'page_token': page_token
        }
        if order != DEFAULT_ORDER:
            query['order'] = order

        directory = NextPage(
            label=context.i18n('Next Page'),
            path=create_addon_path(query)
        )
        list_items.append(tuple(directory))

    xbmcplugin.addDirectoryItems(context.handle, list_items, len(list_items))

    xbmcplugin.endOfDirectory(context.handle, True)
