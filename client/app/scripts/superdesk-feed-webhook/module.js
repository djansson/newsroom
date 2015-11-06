(function() {
    'use strict';

    var modulePath = 'scripts/superdesk-feed-webhook';

    var app = angular.module('superdesk.feed.webhook', [
        'superdesk.ingest'
    ]);

    app.run(['feedingServices', function(providerTypes) {
        providerTypes.push({
            value: 'webhook',
            label: 'WebHook',
            templateUrl: modulePath + '/views/webhookConfig.html'
        });
    }]);

    app.directive('sdWebhookConfig', [
    function() {
        return {
            scope: {
                provider: '='
            },
            templateUrl: modulePath + '/views/webhookRealConfig.html',
            link: function($scope) {
                $scope.prefix = config.server.url + '/hook_receiver/';
            }
        };
    }]);

    return app;

})();
