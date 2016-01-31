var app = angular.module('Example', ['ngRoute'])

//routing configuration
.config(['$routeProvider', '$httpProvider', function($routeProvider){
	$routeProvider
  	.when('/',{
  		templateUrl: '/templates/login.html',
  		controller: 'LoginControl',
  		controllerAs: 'Ctrl',
  	}).
  	when('/profile',{
  		templateUrl:'/templates/profile.html',
  		controller:'ProfileControl',
  		controllerAs:'Ctrl'
  	}).
   otherwise({
      redirectTo: '/'
   });
}]);

//controller for the login page
app.controller('LoginControl', ['$scope', '$http', '$location', function($scope, $http, $location){
    
    $scope.sign_in = function(){
       
       var request = $http({
         url: "/scripts/user.php",
         method: "POST",
         data:{
           username: $scope.username,
           password: $scope.password       
         },
         headers: {
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Access-Control-Allow-Methods':'GET, POST, OPTIONS',
           'Access-Control-Allow-Origin':'*'
         }
      });
      
      request.success(function(data){
         console.log(data);
      });
      request.error(function(data){
         console.log("Script error.");
      });
      
      //$location.path('/profile');
   }
}]);

//controller for the profile page
app.controller('ProfileControl', ['$scope', '$location', function($scope, $location){
   
   $scope.posts = [{content:"Hello World"}];
   
   $scope.sign_out = function(){
      $location.path('/');
   }

}]);

//navbar directive
app.directive('navbar', function(){
	return{
		templateUrl:'/templates/navbar.html'
	};
});


//used to create a new service for a specific controller
/*app.service('checkUser', ['$scope', '$http', function($scope, $http){
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
    
   var sign_in = function(){
    
       var request = $http({
       method: "post",
       url: "http://sae.magnusb.net/scripts/user.php",
       data: {
           username: $scope.username,
           password: $scope.password
       },
       headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      request.success(function(data){
         console.log(data);
      });
      request.failure(function(data){
         console.log("Script error.");
      });
   }
});
/*
//used to create a set of new services that is shared among controllers
app.factory("");1\
*/
