import json
from nose.tools import *
from lettuce import *
import requests
import os
import sys
import inspect
import re

from config import *

filename = 'parameters.ini'


@step(u'Given a config class')
def given_a_config_class(step):
    world.config_obj = DataLoader()


@step(u'Given I set the headers with API key as headers')
def given_i_set_the_headers_with_api_key_as_headers(step):
    header = set_param()
    world.headers = header['headers']


@step(u'Given I set the section as "([^"]*)"')
def given_i_set_the_section_as_group1(step, section):
    world.section = section


@step(u'When I set the url in the format "([^"]*)"')
def when_i_set_the_url_in_the_format_group1(step, setUrl):
    projectId = get_project_id()
    repoId = get_repo_id()
    world.bitBucketUrl = setUrl % (projectId, repoId)


@step(u'When I make api get request with projectId and roleId in the url')
def when_i_make_api_get_request_with_projectid_and_roleid_in_the_url(step):
    world.res = get_bitbucket_info(world.bitBucketUrl, world.headers)


@step(u'Then the status code should be 200')
def then_the_status_code_should_be_200(step):
    assert_equal(world.res.status_code, 200)


@step(u'Then verify author and email of the project committer exist in the response')
def then_verify_author_and_email_of_the_project_committer_exist_in_the_response(step):
    data = convert_to_json()
    bitBucketResponse = data['commits'][0]
    commitKeys = bitBucketResponse.keys()
    commitValues = bitBucketResponse.values()
    assert "author" in commitKeys, "Bitbucket API cannot retrieve author's info correctly"
    if any("@ft.com" in value for value in commitValues):
        assert True, "Committer Email present in retrieved information"
    else:
        assert False, "Email not present Bitbucket API not working correctly"


def set_param():
    return world.config_obj.dataload(filename)


def get_project_id():
    data = set_param()
    world.projectId = data[world.section]['projectId']
    return world.projectId


def get_repo_id():
    data = set_param()
    world.repoId= data[world.section]['repoId']
    return world.repoId


def get_bitbucket_info(url, headers):
    world.response = requests.get(url=url, headers=headers)
    return world.response


def convert_to_json():
    return json.loads(world.response.text)