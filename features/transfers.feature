Feature: Money transfers

  Scenario: User creates an account and deposits money
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "80010112345"
    When I make an incoming transfer of "100" to account with pesel "80010112345"
    Then Account with pesel "80010112345" has balance "100"

  Scenario: User sends money to another account
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "90010112345"
    And I create an account using name: "Anna", last name: "Nowak", pesel: "92010154321"
    And I make an incoming transfer of "200" to account with pesel "90010112345"
    When I transfer "100" from account with pesel "90010112345" to account with pesel "92010154321"
    Then Account with pesel "90010112345" has balance "100"
    And Account with pesel "92010154321" has balance "100"

  Scenario: Transfer fails when funds are insufficient
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "95010112345"
    And I create an account using name: "Anna", last name: "Nowak", pesel: "96010154321"
    And I make an incoming transfer of "50" to account with pesel "95010112345"
    When I try to transfer "100" from account with pesel "95010112345" to account with pesel "96010154321"
    Then The transfer should fail with status code 422
    And Account with pesel "95010112345" has balance "50"

  Scenario: Express transfer charges extra fee
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "88010112345"
    And I create an account using name: "Anna", last name: "Nowak", pesel: "99010154321"
    And I make an incoming transfer of "100" to account with pesel "88010112345"
    When I make an express transfer of "50" from account with pesel "88010112345" to account with pesel "99010154321"
    Then Account with pesel "88010112345" has balance "49"
    And Account with pesel "99010154321" has balance "50"