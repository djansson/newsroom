# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


from datetime import datetime
from urllib.parse import unquote_plus

from superdesk.errors import ParserError
from superdesk.io import register_feed_parser
from superdesk.io.feed_parsers import FileFeedParser
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, GUID_FIELD, GUID_TAG
from superdesk.metadata.utils import generate_guid
from superdesk.utc import utcnow, utc


def set_item_defaults(item):
    item['urgency'] = 5
    item['pubstatus'] = 'usable'
    item['anpa_category'] = [{'qcode': 'e'}]
    item['subject'] = [{'qcode': '01000000',
                        'name': 'arts, culture and entertainment'}]


class ClickatellFeedParser(FileFeedParser):
    """
    Feed Parser which can parse if the feed is in ANPA 1312 format.
    """

    NAME = 'clickatell'

    def can_parse(self, data):
        return isinstance(data, dict)

    def parse(self, raw_data, provider=None):
        try:
            data = raw_data['data']
            item = {ITEM_TYPE: CONTENT_TYPE.TEXT, GUID_FIELD: generate_guid(type=GUID_TAG)}
            item['original_source'] = data.get('from', None)
            raw_timestamp = data.get('timestamp', None)
            item['firstcreated'] = datetime.strptime(
                raw_timestamp, '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=utc)
            item['body_html'] = unquote_plus(data.get('text', ''))
            item['headline'] = item['body_html']
            set_item_defaults(item)
            item['versioncreated'] = utcnow()
            return item
        except Exception as ex:
            raise ParserError.parseMessageError(ex, provider)


register_feed_parser(ClickatellFeedParser.NAME, ClickatellFeedParser())
