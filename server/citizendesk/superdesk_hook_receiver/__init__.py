# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""HookReceiver module"""
import logging
import superdesk
from superdesk.errors import SuperdeskApiError
from superdesk import get_resource_service
from flask import request, current_app as app
from superdesk.io.commands.update_ingest import ingest_items, LAST_ITEM_UPDATE
from superdesk.stats import stats
from superdesk.io import registered_feeding_services
from superdesk.utc import utcnow
from superdesk.metadata.utils import generate_guid
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, GUID_TAG
from superdesk.notification import push_notification

from . import feeding_provider  # NOQA


def set_item_defaults(item):
    item['urgency'] = 5
    item['pubstatus'] = 'usable'
    item['anpa_category'] = [{'qcode': 'e'}]
    item['subject'] = [{'qcode': '01000000',
                        'name': 'arts, culture and entertainment'}]


bp = superdesk.Blueprint('hook_receiver_raw', __name__)
superdesk.blueprint(bp)
logger = logging.getLogger(__name__)


@bp.route('/hook_receiver/<path:hook_id>', methods=['GET', 'POST'])
def get_hook_receiver_as_data_uri(hook_id):
    data = request.json
    if not data:
        data = list(request.form.items())

    # logger.critical(dir(request))
    logger.critical(hook_id)
    logger.critical(data)
    """
    logger.critical([
        (item["_id"], item["source"]) for item in
        get_resource_service("ingest_providers").get(req=None, lookup={})
    ])
    logger.critical(list(
        get_resource_service("ingest_providers").get(req=None, lookup={})
    ))
    """

    ingest_provider_service = superdesk.get_resource_service(
        'ingest_providers')
    ingest_provider = get_resource_service("ingest_providers").find_one(
        req=None, _id=hook_id, feeding_service='webhook'
    )
    if not ingest_provider:
        raise SuperdeskApiError.notFoundError('Hook is not registered.')

    update = {}
    update[LAST_ITEM_UPDATE] = utcnow()

    # @TODO:
    item = {}
    set_item_defaults(item)
    item['guid'] = generate_guid(type=GUID_TAG)
    item['versioncreated'] = update[LAST_ITEM_UPDATE]
    item['original_source'] = 'from_field_placeholder'
    # item['firstcreated'] = message['timestamp']
    item[ITEM_TYPE] = CONTENT_TYPE.TEXT
    item['headline'] = str(data)
    item['body_html'] = str(data)

    feeding_service = registered_feeding_services[
        ingest_provider['feeding_service']
    ].__class__()
    ingest_items(
        [item], ingest_provider, feeding_service,
        ingest_provider.get('rule_set', None), ingest_provider.get(
            'routing_scheme', None)
    )
    stats.incr('ingest.ingested_items', 1)
    ingest_provider_service.system_update(
        ingest_provider[superdesk.config.ID_FIELD], update, ingest_provider
    )
    push_notification('ingest:update', provider_id=str(
        ingest_provider[superdesk.config.ID_FIELD])
    )

    response = app.response_class(
        '{"_status": "OK"}',
        direct_passthrough=True
    )
    response.make_conditional(request)
    return response
