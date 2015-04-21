(function () {

  'use strict';

  angular.module('WordcountApp', [])

  .controller('WordcountController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {

    $scope.getResults = function() {

      // get the URL from the input
      var userInput = $scope.input_url;
      // fire the API request
      $log.log(userInput);
      $http.post('/', {"url": userInput}).
        success(function(results) {
          $log.log(results);
          getWordCount();

        }).
        error(function(error) {
          $log.log(error);
        });

    };

    function getWordCount() {

      var timeout = "";

      var poller = function() {
        // fire another request
        $http.get('/').
          success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200){
              $log.log(data);
              $scope.results = data;
              $timeout.cancel(timeout);
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 2000);
          });
      };
      poller();
    }

  }

  ]);

}());