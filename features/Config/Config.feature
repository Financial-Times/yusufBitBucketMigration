Feature: Lambda config service API

    Scenario: Should retrieve configuration using api key
        Given a config class
        Given I set the headers with api key as headers
        Given I set the data as data
        Given I set the url as url
        Given I make a call to the api with url "https://config-api.in.ft.com/v1"
        Then the status code should be 200
        Then verify is the config service api
        Then output should contain the text "test"
        Then returned value should contain the value "passed"


Examples:
    | test | passed