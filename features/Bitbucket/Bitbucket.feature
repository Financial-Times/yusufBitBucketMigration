 Feature: Bitbucket API for extracting commits information from git

    Scenario: Should return specified project and repo commit information
        Given a config class
        Given I set the headers with API key as headers
        Given I set the section as "bitbucket"
        When I set the url in the format "https://bitbucket-api.in.ft.com/v2/commits/%s/%s"
        When I make api get request with projectId and roleId in the url
        Then the status code should be 200
        Then verify author and email of the project committer exist in the response
