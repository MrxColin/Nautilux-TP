var app = angular.module('Nautilux', ['ngRoute']);


//* ROUTES *//
app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/tickets', {
            templateUrl: "views/tickets.html",
            controller: "listeTicketsController"
        })
        .when('/form', {
            templateUrl: "views/form.html",
            controller: "ticketController"
        })
        .otherwise({
            redirectTo: '/tickets'
        });
}]);

app.service("serveurService", ['$http', function ($http) {
    this.getTickets = function () { return $http({ method: 'GET', url: 'http://127.0.0.1:5000/api/ressources/tickets' }) };
}]);


//* CONTROLLERS *//

/* Controller vue tableau contenant les interventions*/
app.controller('listeTicketsController', ['$scope', '$http', 'ticketService', function ($scope, $http, ticketService) {
    $http({ method: 'GET', url: 'http://127.0.0.1:5000/api/ressources/tickets' }).then(
        function (response) {
             $scope.tickets = response.data; 
             for (ticket of $scope.tickets){
                 ticket.date_inter=new Date(ticket.date_inter);
             }
            },
        function (error) { alert(error); }
    );

    $scope.delete = function (ticket) { //Lorqu'on clique sur le bouton supprimer
        $http({

            method: 'DELETE',
            url: 'http://127.0.0.1:5000/api/ressources/deleteTicket/' + ticket.libel   //on supprime l'élément, (pour des raisons pratique, le libellé fait office d'id, on estime qu'il est unique)

        }).then(function successCallback(response) {
            alert("Le ticket a été supprimé");
            $scope.updateListeTicket()
        }, function errorCallback(response) {
            alert("Erreur lors de la supression!");
        });


    };

    $scope.updateListeTicket = function () {  //Lorsqu'on clique sur le bouton modifier
        $http({ method: 'GET', url: 'http://127.0.0.1:5000/api/ressources/tickets' }).then(    //On remet à jour la liste des interventions
            function (response) { $scope.tickets = response.data; },
            function (error) { alert(error); }
        );
    };
    $scope.update = function (ticket) {  //Lorsqu'on clique sur le bouton modifier
        ticketService.updateInter(ticket);
    };

    $scope.reset = function (ticket) {  //Si l'on quitte la modification via la navbar
        ticketService.modif = false;
        ticketService.intervention = {
            libel: "",
            desc: "",
            nom_inter: "",
            lieu: "",
            statut: "",
            date_inter: new Date()
        };
    };
}

]);
/* Controller vue formulaire*/

app.controller('ticketController', ['$scope', '$http', 'ticketService', function ($scope, $http, ticketService) {
    $scope.intervention = ticketService.intervention;
    $scope.modif = ticketService.modif;
    $scope.modify = function (ticket) {  // Lorsqu'on valide la modification
        $http.post('http://127.0.0.1:5000/api/ressources/modifyTicket', JSON.stringify(ticket)).then(function successCallback(response) {
            alert("Le ticket a été modifié");
            ticketService.modif = false;
            ticketService.intervention = {
                libel: "",
                desc: "",
                nom_inter: "",
                lieu: "",
                statut: "",
                date_inter: new Date()
            };

        }, function errorCallback(response) {
            alert("Erreur lors de la modification!");
        });

    };
    $scope.add = function (intervention) {
        $http.put('http://127.0.0.1:5000/api/ressources/putTickets', JSON.stringify(intervention)).then(function successCallback(response) {
            alert("Le ticket a été ajouté");
            ticketService.modif = false;
            $scope.intervention = {
                libel: "",
                desc: "",
                nom_inter: "",
                lieu: "",
                statut: "",
                date_inter: new Date()
            };
        }, function errorCallback(response) {
            alert("Erreur lors de la modification!");
        });

    };

}])



//** Directives **//

app.directive("ticketsDirective", function () {
    return {
        template: "<td>{{ticket.libel}}</td> <td>{{ticket.nom_inter}}</td> <td>{{ticket.desc}}</td> <td>{{ticket.date_inter | date : 'dd/MM' }}</td> <td>{{ticket.lieu}}</td> <td> <a href='#!form' class='btn btn-secondary' ng-click='update(ticket)'><i class='fa fa-folder'></i></a><button class='btn btn-danger' ng-click='delete(ticket)'><i class='fa fa-close'></i></button></td>"
    };
})


//** Services **//

app.service("ticketService", [function () {
    this.intervention = {
        libel: "",
        desc: "",
        nom_inter: "",
        lieu: "",
        statut: "",
        date_inter: new Date()
    };
    this.modif = false;

    this.updateInter = function (ticket) {
        this.intervention = ticket;
        this.modif = true;
    }
}]);


