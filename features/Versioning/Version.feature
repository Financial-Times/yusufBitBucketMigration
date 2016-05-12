Feature: Lambda Versioning API Major and Minor

     Scenario: Should increase the Major version number
        Given a config class
        Given I set the headers with api key as headers
        Given I set the data version as "major"
        Given I set the url as url
        Given I make a call to the api with url "https://version-api.in.ft.com/v2/version"
        Then the status code should be 200
        Then verify that lambda service is versioning and contain "version"
        Then verify if "major" version


     Scenario: Should increase the Minor version number
        Given a config class
        Given I set the headers with api key as headers
        Given I set the data version as "minor"
        Given I set the url as url
        Given I make a call to the api with url "https://version-api.in.ft.com/v2/version"
        Then the status code should be 200
        Then verify that lambda service is versioning and contain "version"
        Then verify if "minor" version
