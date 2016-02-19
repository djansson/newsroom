(function() {
    'use strict';

    var app = angular.module('superdesk.feedparser.clickatell', [
        'superdesk.ingest'
    ]);

    app.run(['feedParsers', function(feedParsers) {
        feedParsers.push({
            value: 'clickatell',
            name: 'Clickatell SMS',
        });
    }]);

    return app;

})();
