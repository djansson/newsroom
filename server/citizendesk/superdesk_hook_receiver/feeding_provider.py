# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""WebHook io service."""

from superdesk.io import register_feeding_service
from superdesk.io.feeding_services import FeedingService
from superdesk.errors import IngestApiError


class WebHookFeedingService(FeedingService):
    """WebHook ingest service."""

    NAME = 'webhook'

    ERRORS = [IngestApiError.apiTimeoutError().get_error_description(),
              IngestApiError.apiRedirectError().get_error_description(),
              IngestApiError.apiRequestError().get_error_description(),
              IngestApiError.apiUnicodeError().get_error_description(),
              IngestApiError.apiParseError().get_error_description(),
              IngestApiError.apiGeneralError().get_error_description()]

    DATE_FORMAT = '%Y.%m.%d.%H.%M'

    def __init__(self):
        super().__init__()

    def prepare_href(self, href):
        return href

    def _update(self, provider):
        """Service update call."""

        pass

register_feeding_service(
    WebHookFeedingService.NAME,
    WebHookFeedingService(),
    WebHookFeedingService.ERRORS
)
