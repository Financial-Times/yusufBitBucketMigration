Feature: Change Request API for change management via Salesforce

    Scenario: Should automatically raise change request
        Given I set up release log envrionment with data as "release_log_data"  and url as "releaselog_url"
        Then a change request api call is made
        Then the status code should be 200

    Scenario: Should raise a normal CR and close the request
        Given I set up normal change request environment data as "normal_cr_data" and url as "normal_cr_url"
        Then I set the "scheduledStartDate" and "scheduledEndDate"
        Then a change request api call is made
        Then the status code should be 200

    Scenario Outline: Should create normal change with different text matrix [0-8]
        Given I set up normal change request environment data as "normal_cr_data" and url as "normal_cr_url"
        Given I set riskProfile "<riskProfile>" and changeCategory "<changeCategory>"
        Given I set repeatableProcess "<repeatableProcess>" and outage "<willThereBeAnOutage>"
        Given I set previouslyConducted "<previouslyConducted>"
        Then I set the "scheduledStartDate" and "scheduledEndDate"
        Then a change request api call is made
        Then the status code should be 200

    Examples:
        | riskProfile | changeCategory | repeatableProcess | willThereBeAnOutage | previouslyConducted |
        | Low         |  Major         |   No              |       Yes           |     No              |
        | Medium      |  Minor         |   Yes             |        No           |     Yes             |
        | High        |  Significant   |   No              |        No           |     Yes             |
        | Medium      |  Major         |   No              |        Yes          |     No              |
        | High        |  Minor         |   No              |        Yes          |     Yes             |
        | Low         |  Significant   |   Yes             |        No           |     No              |
        | High        |  Major         |   Yes             |        Yes          |     Yes             |
        | Low         |  Minor         |   Yes             |        Yes          |     No              |
        | Medium      |  Significant   |   No              |        No           |     No              |


    Scenario: Should return the list of CR created when from and to dates specified
        Given I set up test configuration and url as "cr_list_url"
        Then I get list of CR by calling the api
        Then status code must be 200

    Scenario: Should return the list of CR created using systemcode
        Given I set up test configuration systemcode as "/koncrapi" and url as "cr_list_url"
        Then I get list of CR by calling the api
        Then status code must be 200

    Scenario: Should not be successful with an invalid systemcode
        Given I set up test configuration systemcode as "/koncrap" and url as "cr_list_url"
        Then I get list of CR by calling the api
        Then status code must be 400

    Scenario: Should not be successful with invalid dates from
<<<<<<< HEAD
        Given I set up test configuration and url as "cr_list_url"
        Then I get list of CR by calling the api
        Then status code must be 400
=======
        Given I set up configuration and url as "cr_list_url"
        Then I get list of CR by calling the api
        Then status code must be 200
>>>>>>> 6bdd56cc9912ee349e5abbbe081bdda5df29ec71
