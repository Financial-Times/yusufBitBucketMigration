import json
from nose.tools import *
from lettuce import *
import requests
import os
import sys
import inspect
import re

cmd_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"kontest")))
if cmd_folder not in sys.path:
    sys.path.insert(0,cmd_folder)

from config import *

filename = "parameters.ini"


@step(u'Given a config class')
def select_config(step):
    world.config_obj = DataLoader()


@step(u'Given I set the headers with api key as headers')
def given_i_set_the_headers_with_api_key_as_headers(step):
    header = set_param()
    world.headers = header['headers']
    print "WORLD HEADERS", world.headers


@step(u'Given I set the data version as "([^"]*)"')
def given_i_set_the_data_as_data_group1(step, expected):
    dat = set_param()
    if dat['version_major']['action'] == expected:
        world.data = dat['version_major']
    else:
        world.data = dat['version_minor']


@step(u'Given I set the url as url')
def given_i_set_the_url_as_url(step):
    uri = set_param()
    world.url = uri['version_url']['ver_url']


@step(u'Given I make a call to the api with url "([^"]*)"')
def given_i_make_a_call_to_the_api_with_url_group1(step, group1):
    world.res = make_an_api_request(world.url, world.data, world.headers)


@step(u'Then the status code should be 200')
def then_the_status_code_should_be_200(step):
    assert_equal(world.res.status_code, 200)


@step(u'Then verify that lambda service is versioning and contain "([^"]*)"')
def then_verify_that_lambda_service_is_versioning_and_contain_group1(step, expected):
    key_list = encode_response_keys_to_ascii()
    assert expected in key_list, 'The versioning api failed'
    print 'KEY LIST', key_list


@step(u'Then verify if "([^"]*)" version')
def then_verify_if_expected_version(step, expected):
    version_num = version_numbers()
    if expected == 'major':
        assert version_num[0] > version_num[1], 'major version number is wrong'
    else:
        assert version_num[1] > version_num[0], 'minor version number is wrong'



def set_param():
    return world.config_obj.dataload(filename)


def make_an_api_request(url,data,headers):
    world.response = requests.post(url=url, data=json.dumps(data), headers=headers)
    return world.response


def convert_to_json():
    return json.loads(world.response.text)


def encode_response_keys_to_ascii():
    data = convert_to_json()
    resp_key = data.keys()
    for i in range(len(resp_key)):
        resp_key[i] = resp_key[i].encode('ascii')
    return resp_key


def encode_response_value_ascii():
    data = convert_to_json()
    world.resp_val = data.values()
    for i in range(len(world.resp_val)):
        world.resp_val[i] = world.resp_val[i].encode('ascii')
    print "world.resp_val", world.resp_val
    return world.resp_val


def version_numbers():
    old_val = encode_response_value_ascii()
    ver_num = re.sub(r'-.*$',"", old_val[1]).split('.')
    for i in range(len(ver_num)):
        ver_num[i] = int(ver_num[i])
    return ver_num