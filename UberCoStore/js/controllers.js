function InventoryController($scope, $http) {
    $scope.apiAddress = 'http://localhost:5051';

    $scope.requiredKeys = []
    $scope.currentBarcode = [];

    $scope.showingInventory = true;
    
    $(document).keypress(function(e) {
        if ($scope.selectedTeam) {
            var cardId;
            if (e.which != 13) {
                $scope.currentBarcode.push(e.which-48);
            } else if ($scope.currentBarcode.length != 0) {
                console.log("Enter Pressed");
                for (var i = 0; i < $scope.currentBarcode.length; i++) {
                    if (i == 0) {
                        cardId = $scope.currentBarcode[i].toString();
                    } else {    
                        cardId += $scope.currentBarcode[i].toString();
                    }
                }
                $scope.currentBarcode = []
                $http.get($scope.apiAddress+'/'+$scope.selectedTeam.id+'/cards/redeem/'+cardId).success(function(data) {
                    $scope.addItemWithPopup(data);
                }).error(function (data) {
                        $scope.displayError(data);
                    });
            }
        }
    });

    $scope.getTeamInventory = function(){
        $http.get($scope.apiAddress+'/'+$scope.selectedTeam.id+'/items').success(function(data) {
            $scope.inventory = data.sort($scope.sortById);
            $scope.setSelectedItem($scope.inventory[0]);
        }).error(function(data) {
                $scope.displayError(data);
            });
    };

    $scope.getTeamRewards = function(){
        $http.get($scope.apiAddress+'/'+$scope.selectedTeam.id+'/rewards').success(function(data) {
            $scope.rewards = data.sort($scope.sortById);
            $scope.setSelectedReward($scope.rewards[0]);
        }).error(function(data) {
                $scope.displayError(data);
            });
    };

    $scope.redeemChest = function (chestId) {
        $http.get($scope.apiAddress+'/'+$scope.selectedTeam.id+'/chests/redeem/'+chestId).success(function(data) {
            $scope.reward = data;

        }).error(function(data) {
                $scope.displayError(data);
            });
    }

    $("#item-to-add").keyup(function(event){
        if(event.keyCode == 13 && $("#item-to-add")[0].value != ""){
            var cardId = $("#item-to-add")[0].value;
            $http.get($scope.apiAddress+'/'+$scope.selectedTeam.id+'/cards/redeem/'+cardId).success(function(data) {
                $scope.addItemWithPopup(data);
            }).error(function (data) {
                    $scope.displayError(data);
                });
        }
    });

    $("#open-chest").click(function(event) {
        if ($scope.canOpenChest) {
            $http.get($scope.apiAddress+'/'+$scope.selectedTeam.id+'/chests/redeem/'+$scope.selectedItem.id).success(function(data) {
                $scope.getTeamInventory();
                $scope.showReward(data);
                $scope.getTeamRewards();
            }).error(function (data) {
                    $scope.displayError(data);
                })
        }
    });

    $scope.sortById = function(a,b) {
        if (a.id < b.id)
            return -1;
        if (a.id > b.id)
            return 1;
        return 0;
    };

    $scope.sortByType = function(a,b) {
        if (a.is_chest < b.is_chest)
            return -1;
        if (a.is_chest > b.is_chest)
            return 1;
        return 0;
    };

    $scope.sortByRarity = function(a,b) {
        if (a.rarity < b.rarity)
            return -1;
        if (a.rarity > b.rarity)
            return 1;
        return 0;
    };

    $scope.getFormattedName = function(name, maxLength) {
        if (name.length > maxLength) {
            return name.slice(0,maxLength-3) + "...";
        } else {
            return name;
        }
    }

    $scope.addItemWithPopup = function (item) {
        $scope.getTeamInventory();
        $scope.addedItem = item;
        $( "#item-message" ).dialog({
            modal: true,
            title: item.name + " has been added to your inventory!",
            width: 530,
            show: {
                effect: "fade",
                duration: 300
            },
            hide: {
                effect: "fade",
                duration: 300
            }
        });
        setTimeout(function(){ $("#item-message").dialog("close"); }, 3000);
        $("#item-to-add")[0].value = ""
    };

    $scope.showReward = function (reward) {
        $scope.reward = reward;
        $( "#reward-message" ).dialog({
            modal: true,
            width: 530,
            show: {
                effect: "fade",
                duration: 300
            },
            hide: {
                effect: "fade",
                duration: 300
            }
        });
        setTimeout(function(){ $("#error-message").dialog("close"); }, 3000);
    }

    $scope.displayError = function (data) {
        $scope.errorMessage = data.error;
        $( "#error-message" ).dialog({
            modal: true,
            show: {
                effect: "fade",
                duration: 300
            },
            hide: {
                effect: "fade",
                duration: 300
            }
        });
        setTimeout(function(){ $("#error-message").dialog("close"); }, 3000);
        $("#item-to-add")[0].value = ""
    };

    $scope.setSelectedItem = function (item) {
        $scope.selectedItem = item;
        if (item.is_chest) {
            $scope.requiredKeys = $scope.getListOfRequiredKeys(item.id);
        }
    };

    $scope.setSelectedReward = function (item) {
        $scope.selectedReward = item;
    };

    $scope.getRarityString = function (rarity) {
        switch(rarity){
            case 1:
                return "Very Common";
            case 2:
                return "Common";
            case 3:
                return "Uncommon";
            case 4:
                return "Rare";
            case 5:
                return "Very Rare";
        }
    };

    $scope.getImageString = function (imageName) {
        return "img/" + imageName
    };

    $scope.getRequiredKeys = function (chestId) {
        for (var i = 0; i < $scope.chest_keys.length; i++) {
            if ($scope.chest_keys[i].chest == chestId) {
                return $scope.chest_keys[i].keys;
            }
        }
    };

    $scope.getItemName = function(itemId) {
        var items = $scope.allItems;
        for (var i = 0; i < items.length; i++) {
            if (items[i].id == itemId) {
                return items[i].name;
            }
        }
    };

    $scope.selectTeam = function(team) {
        $scope.selectedTeam = team;
        $scope.getTeamInventory();
        $scope.getTeamRewards();
        $("#selection-overlay").css("top", 200)
        $("#team-selector").hide('slide', {'duration': 300, 'direction': 'left'}, function(){
            $("#main-container").show('slide',{'duration': 300, 'direction': 'right'});
            $("#selection-overlay").css("top", 230)
        });
        //$("#item-to-add").focus();
    };

    $scope.getListOfRequiredKeys = function(chestId) {
        var requiredKeys = $scope.getRequiredKeys(chestId);
        var inventoryItemIds = [];

        var itemList = [];

        for (var i = 0; i < $scope.inventory.length; i++) {
            inventoryItemIds.push($scope.inventory[i].id);
        }

        for (var i = 0; i < requiredKeys.length; i++) {
            if (inventoryItemIds.indexOf(requiredKeys[i]) != -1) {
                inventoryItemIds.splice(inventoryItemIds.indexOf(requiredKeys[i]), 1);
                itemList.push({"id": requiredKeys[i], "owned": true});
            } else {
                itemList.push({"id": requiredKeys[i], "owned": false});
            }
        }
        return itemList;
    }

    $scope.canOpenChest = function(chestId, isChest) {
        if (isChest) {
            console.log("Checking Chest ID: "+chestId);
            var items = $scope.inventory.slice();
            var requiredKeys = $scope.getRequiredKeys(chestId);
            var ownedKeys = [];
            for (var i = 0; i < requiredKeys.length; i++) {
                for (var j = 0; j < items.length; j++) {
                    if (items[j].id == requiredKeys[i]) {
                        ownedKeys.push(requiredKeys[i]);
                        items.splice(j,1);
                        break;
                    }
                }
            }
            return requiredKeys.length == ownedKeys.length;
        } else {
            return false;
        }
    }

    $("#inventory-button").click(function() {
        if (!$scope.showingInventory) {
            $("#rewards").hide('card');
            $("#inventory").show('card');
            $(this).toggleClass('selected');
            $("#reward-button").toggleClass('selected');
            $scope.showingInventory = true;
        }
    });

    $("#reward-button").click(function() {
        if ($scope.showingInventory) {
            $("#inventory").hide('card');
            $("#rewards").show('card');
            $(this).toggleClass('selected');
            $("#inventory-button").toggleClass('selected');
            $scope.showingInventory = false;
        }
    });

    $scope.logout = function () {
        $("#selection-overlay").css("top", 200)
        $("#main-container").hide('slide', {'duration': 300, 'direction': 'right'}, function(){
            $("#team-selector").show('slide',{'duration': 300, 'direction': 'left'}, function() {
                $("#selection-overlay").css("top", 230)
            });

        });
        $scope.selectedTeam = undefined;
    }

    $http.get($scope.apiAddress+'/teams/list').success(function(data) {
        $scope.teams = data.sort($scope.sortById);
    }).error(function(data) {
            $scope.displayError(data);
        });

    $http.get($scope.apiAddress+'/chests').success(function(data) {
        $scope.chest_keys = data;
    }).error(function(data) {
            $scope.displayError(data);
        });

    $http.get($scope.apiAddress+'/items/list').success(function(data) {
        $scope.allItems = data;
    }).error(function(data) {
            $scope.displayError(data)
        });
}