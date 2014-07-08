angular.module('hz').factory
    ('SatelliteErrata', ['$resource', 'Base64',
        function ($resource, Base64) {

             var getAuthToken = function(username, password) {
                        var tokenize = username + ':' + password;
                        tokenize = Base64.encode(tokenize);
                        return "Basic " + tokenize;
                    };

             var SatelliteErrata = $resource('https://sat-perf-05.idm.lab.bos.redhat.com/katello/api/v2/systems/:id/errata', {id: '@uuid'}, {
                     get: {
                         method: 'GET',
                         isArray: false,
                         headers: { 'Authorization': getAuthToken('admin', 'changeme') }
                     }
                 }
             );

             return SatelliteErrata;

        }]);

angular.module('hz').factory('Base64', function() {
        var keyStr = 'ABCDEFGHIJKLMNOP' +
            'QRSTUVWXYZabcdef' +
            'ghijklmnopqrstuv' +
            'wxyz0123456789+/' +
            '=';
        return {
            encode: function (input) {
                var output = "";
                var chr1, chr2, chr3 = "";
                var enc1, enc2, enc3, enc4 = "";
                var i = 0;

                do {
                    chr1 = input.charCodeAt(i++);
                    chr2 = input.charCodeAt(i++);
                    chr3 = input.charCodeAt(i++);

                    enc1 = chr1 >> 2;
                    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
                    enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
                    enc4 = chr3 & 63;

                    if (isNaN(chr2)) {
                        enc3 = enc4 = 64;
                    } else if (isNaN(chr3)) {
                        enc4 = 64;
                    }

                    output = output +
                        keyStr.charAt(enc1) +
                        keyStr.charAt(enc2) +
                        keyStr.charAt(enc3) +
                        keyStr.charAt(enc4);
                    chr1 = chr2 = chr3 = "";
                    enc1 = enc2 = enc3 = enc4 = "";
                } while (i < input.length);

                return output;
            },

            decode: function (input) {
                var output = "";
                var chr1, chr2, chr3 = "";
                var enc1, enc2, enc3, enc4 = "";
                var i = 0;

                // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
                var base64test = /[^A-Za-z0-9\+\/\=]/g;
                if (base64test.exec(input)) {
                    alert("There were invalid base64 characters in the input text.\n" +
                        "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
                        "Expect errors in decoding.");
                }
                input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

                do {
                    enc1 = keyStr.indexOf(input.charAt(i++));
                    enc2 = keyStr.indexOf(input.charAt(i++));
                    enc3 = keyStr.indexOf(input.charAt(i++));
                    enc4 = keyStr.indexOf(input.charAt(i++));

                    chr1 = (enc1 << 2) | (enc2 >> 4);
                    chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                    chr3 = ((enc3 & 3) << 6) | enc4;

                    output = output + String.fromCharCode(chr1);

                    if (enc3 != 64) {
                        output = output + String.fromCharCode(chr2);
                    }
                    if (enc4 != 64) {
                        output = output + String.fromCharCode(chr3);
                    }

                    chr1 = chr2 = chr3 = "";
                    enc1 = enc2 = enc3 = enc4 = "";

                } while (i < input.length);

                return output;
            }
        };
    });

angular.module('hz').directive({
    satelliteErrata: [ function () {

        return {
            restrict: 'A',
           // require: '^file',
            transclude: true,
            scope: {
                uuid: '='
            },
            controller: ['$scope', 'SatelliteErrata', '$http', 'Base64', 'ngTableParams', '$filter',
                function ($scope, SatelliteErrata, $http, Base64, ngTableParams, $filter) {

                    var baseUrl = 'https://sat-perf-05.idm.lab.bos.redhat.com';

                    var defaultParams = function (data) {
                        var params = new ngTableParams({
                            page: 1,            // show first page
                            count: 10           // count per page

                        }, {
                             total: data.length, // length of data
                             getData: function($defer, params) {
                                 var filteredData = params.filter() ?
                                     $filter('filter')(data, params.filter()) :
                                     data;
                                 var orderedData = params.sorting() ?
                                     $filter('orderBy')(filteredData, params.orderBy()) :
                                     data;
                                $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                             }
                        });

                        return params;
                    };

                    $scope.errataLink = function (errata) {
                        return baseUrl + '/content_hosts/' + $scope.uuid + '/errata/' + errata.errata_id;
                    };

                    var payload = SatelliteErrata.get({id: $scope.uuid});
                    payload.$promise.then(
                        function() {
                            $scope.errata = payload.results
                            $scope.errataParams = defaultParams($scope.errata);
                        });


            }],
            template:
               '<table ng-table="errataParams" class="table">\n' +
                    '<tr ng-repeat="e in $data">\n' +
                        '<td data-title="\'Title\'" sortable="\'title\'">\n' +
                            '<a ng-href="{$errataLink(e)$}">{{e.title}}</a>\n' +
                        '</td>\n' +
                        '<td data-title="\'Type\'" sortable="\'type\'">{{ e.type }}</td>\n' +
                        '<td data-title="\'Errata ID\'" sortable="\'type\'">{{ e.errata_id }}</td>\n' +
                        '<td data-title="\'Date Issued\'" sortable="\'issued\'">{{ e.issued }}</td>\n' +
                    '</tr>\n'+
               '</table>\n',
            link: function (scope, element, attrs, modelCtrl, transclude)    {
                scope.modelCtrl = modelCtrl;
                scope.$transcludeFn = transclude;
            }
        };
    }]
});

angular.module('hz').controller({
    ErrataController: ['$scope',
        function ($scope ) {

        }]});
