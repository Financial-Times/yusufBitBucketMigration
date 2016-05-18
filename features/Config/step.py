import sys
import json
import  os
from nose.tools import *
from lettuce import *
import requests
import inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"kontest")))
if cmd_folder not in sys.path:
    sys.path.insert(0,cmd_folder)
    print "FOLDER",cmd_folder

from config import *

filename = 'parameters.ini'


@step(u'Given a config class')
def select_config(step):
    world.config_obj = DataLoader()


@step(u'Given I set the headers with api key as headers')
def given_i_set_the_headers_with_api_key_as_headers(step):
    header = set_param()
    world.headers =  header['headers']


@step(u'Given I set the data as data')
def given_i_set_the_data_as_data(step):
    dat = set_param()
    world.data = dat['config_service']


@step(u'Given I set the url as url')
def given_i_set_the_url(step):
    uri = set_param()
    world.url = uri['config_service_url']['config_url']


@step(u'Given I make a call to the api with url "([^"]*)"')
def given_i_make_a_call_to_the_api_with_url_group1(step, group1):
    world.res = make_an_api_request(world.url,world.data,world.headers)


@step(u'Then the status code should be 200')
def then_the_status_code_should_be_200(step):
    assert_equal(world.res.status_code, 200)


@step(u'Then verify is the config service api')
def then_verify_is_the_config_service_api(step):
    conf_serv = encode_unicode_list_ascii()
    assert 'config.service'in conf_serv[0], 'Test Failed'


@step(u'Then output should contain the text "([^"]*)"')
def then_the_output_should_contain_the_text_group1(step, expected):
    conf_serv = encode_unicode_list_ascii()
    world.key_value = json.loads(conf_serv[1])
    kon_key = world.key_value.keys()
    assert_equal(kon_key[0].encode('ascii'),expected ), 'Test Failed'


@step(u'Then returned value should contain the value "([^"]*)"')
def then_returned_value_should_contain_the_value_group1(step, expected):
    kon_val = world.key_value.values()
    assert_equal(kon_val[0].encode('ascii'), expected), 'Test Failed'


def set_param():
     return world.config_obj.dataload(filename)


def make_an_api_request(url,data,headers):
    world.response = requests.post(url=url, data=json.dumps(data), headers=headers)
    return world.response


def convert_to_json():
    return json.loads(world.response.text)


def encode_unicode_list_ascii():
    data = convert_to_json()
    data_value = data.values()
    for i in range(len(data_value)):
        data_value[i] = data_value[i].encode('ascii')
    return data_value



