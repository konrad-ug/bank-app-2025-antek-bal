Feature: Account registry

Scenario: User is able to create 2 accounts
  Given Account registry is empty
  When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
  And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
  Then Number of accounts in registry equals: "2"
  And Account with pesel "89092909246" exists in registry
  And Account with pesel "79101011234" exists in registry

Scenario: User is able to update last name of already created account
  Given Account registry is empty
  And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
  When I update "last_name" of account with pesel: "95092909876" to "filatov"
  Then Account with pesel "95092909876" has "last_name" equal to "filatov"

Scenario: User is able to update name of already created account
  Given Account registry is empty
  And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
  When I update "first_name" of account with pesel: "90010112345" to "adam"
  Then Account with pesel "90010112345" has "first_name" equal to "adam"

Scenario: Created account has all fields correctly set
  Given Account registry is empty
  When I create an account using name: "anna", last name: "nowak", pesel: "85050512345"
  Then Account with pesel "85050512345" has "first_name" equal to "anna"
  And Account with pesel "85050512345" has "last_name" equal to "nowak"
  And Account with pesel "85050512345" has "pesel" equal to "85050512345"

Scenario: User is able to delete created account
  Given Account registry is empty
  And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
  When I delete account with pesel: "01092909876"
  Then Account with pesel "01092909876" does not exist in registry
  And Number of accounts in registry equals: "0"