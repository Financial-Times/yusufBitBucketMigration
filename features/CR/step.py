import json
from nose.tools import *
from lettuce import *
import requests
import os
import sys
import inspect
import re
from datetime import datetime,timedelta, date

from config import *

filename = 'parameters.ini'


@step(u'Given I set up release log envrionment with data as "([^"]*)"  and url as "([^"]*)"')
def given_i_set_up_release_log_envrionment_with_data_as_group1_and_url_as_group2(step, data_section, url_section):
    world.url_section = url_section
    world.data_section = data_section
    set_change_request_data(world.data_section)


@step(u'Given I set up test configuration and url as "([^"]*)"')
def given_i_set_up_test_configuration_and_url_as_group1(step, url_section):
    world.url_section = url_section
    set_change_request_get()


@step(u'Given I set up test configuration with invalid dates and url as "([^"]*)"')
def given_i_set_up_configuration_and_url_as_group1(step, url_section):
    world.url_section = url_section
    set_invalid_dates_get_request()


@step(u'Given I set up test configuration systemcode as "([^"]*)" and url as "([^"]*)"')
def given_i_set_up_test_configuration_systemcode_as_group1_and_url_as_group2(step, system_code, url_section):
    world.url_section = url_section
    world.system_code = system_code
    set_change_request_param_system_code()


@step(u'Given I set up normal change request environment data as "([^"]*)" and url as "([^"]*)"')
def given_i_set_up_normal_change_request_environment_data_as_group1_and_url_as_group2(step,data_section,url_section):
    world.url_section = url_section
    world.data_section = data_section
    set_change_request_data(world.data_section)


@step(u'Given I set up fyi change request environment data as "([^"]*)" and url as "([^"]*)"')
def given_i_set_up_fyi_change_request_environment_data_as_group1_and_url_as_group2(step, data_section , url_section):
    world.url_section = url_section
    world.data_section = data_section
    set_change_request_data(world.data_section)


@step(u'Then I set the "([^"]*)" and "([^"]*)"')
def then_i_set_the_group1_and_group2(step, start_time, end_time):
    set_request_time(start_time, end_time)


@step(u'Then I set an invalid "([^"]*)" and "([^"]*)"')
def then_i_set_an_invalid_group1_and_group2(step, start_time, end_time):
    set_invalid_time_fyi_normal_cr(start_time, end_time)


@step(u'Then a change request api call is made')
def then_a_change_request_api_call_is_made(step):
    world.change_request_response = make_an_api_request(world.url,world.requestData,world.headers)


@step(u'Then I get list of CR by calling the api')
def then_i_get_list_of_cr_by_calling_the_api_with_from_and_to_dates(step):
    world.cr_list_by_date_response = make_cr_get_list_api_call(world.url,world.headers)


@step(u'Then the status code should be 200')
def then_the_status_code_should_be_200(step):
    assert_equal(world.change_request_response.status_code, 200)


@step(u'Then status code must be 200')
def then_status_code_must_be_200(step):
    assert_equal(world.cr_list_by_date_response.status_code, 200)


@step(u'Then status code must be 400')
def then_status_code_must_be_400(step):
    assert_equal(world.cr_list_by_date_response.status_code, 400)


@step(u'Then status code should be 400')
def then_status_code_should_be_400(step):
    assert_equal(world.change_request_response.status_code, 400)


@step('Given I set riskProfile "([^"]*)" and changeCategory "([^"]*)"')
def given_i_set_riskprofile_riskprofile_and_changecategory_changecategroy(step, riskProfile, changeCategory):

    world.requestData['riskProfile']= riskProfile
    world.requestData['changeCategory'] = changeCategory


@step(u'Given I set repeatableProcess "([^"]*)" and outage "([^"]*)"')
def given_i_set_repeatableprocess_repeatableprocess_outages_willThereBeAnOutage(step, repeatableProcess, willThereBeAnOutage):
    world.requestData['repeatableProcess'] = repeatableProcess
    world.requestData['willThereBeAnOutage'] = willThereBeAnOutage


@step(u'Given I set previouslyConducted "([^"]*)"')
def given_i_set_previouslyconducted_group1(step, previouslyConducted):
    world.requestData['previouslyConducted'] = previouslyConducted


@step(u'Given I set the field willThereBeAnOutage "([^"]*)"')
def given_i_set_the_field_willtherebeanoutage_group1(step, willThereBeAnOutage):
    world.requestData['willThereBeAnOutage'] = willThereBeAnOutage


def set_param():
    world.config_obj = DataLoader()
    load_obj = world.config_obj.dataload(filename)
    return load_obj


def set_change_request_data(data_section):
    world.load_obj = set_param()
    world.requestData = world.load_obj[data_section]
    world.url = set_endpoint_url(world.url_section)
    world.headers = set_headers()


def set_change_request_get():
    world.load_obj = set_param()
    url = set_endpoint_url(world.url_section)
    world.url = url % (set_from_date(), set_to_date())
    world.headers = set_headers()


def set_invalid_dates_get_request():
    world.load_obj = set_param()
    url = set_endpoint_url(world.url_section)
    world.url = url % (set_to_date(), set_from_date())
    world.headers = set_headers()


def set_change_request_param_system_code():
    world.load_obj = set_param()
    old_url = set_endpoint_url(world.url_section)
    new_url = old_url % (set_from_date(), set_to_date())
    world.url = new_url + world.system_code
    world.headers = set_headers()

def set_request_time(start_time, end_time):
    world.requestData[start_time] = set_scheduled_start_date_time()
    world.requestData[end_time] = set_scheduled_end_date_time()

def set_invalid_time_fyi_normal_cr(start_time, end_time):
    world.requestData[start_time] = set_scheduled_end_date_time()
    world.requestData[end_time] = set_scheduled_start_date_time()


def set_endpoint_url(url_section):
    world.url = world.load_obj['cr_section'][url_section]
    return world.url


def set_headers():
    headers = world.load_obj['headers']
    return headers


def make_an_api_request(url,data,headers):
    world.response = requests.post(url=url, data=json.dumps(data), headers=headers)
    return world.response


def make_cr_get_list_api_call(url,headers):
    world.response = requests.get(url=url, headers=headers)
    return world.response


def convert_response_to_json():
    return world.response.text


def set_scheduled_start_date_time():
    five_mins_from_now = datetime.now() + timedelta(hours=2)
    scheduled_start_date = format(five_mins_from_now, '%Y-%m-%d %H:%M')
    return scheduled_start_date


def set_scheduled_end_date_time():
    eight_mins_from_now = datetime.now() + timedelta(hours=3)
    scheduled_end_date = format(eight_mins_from_now, '%Y-%m-%d %H:%M')
    return scheduled_end_date


def set_from_date():
    from_time = date.today() - timedelta(1)
    from_date = format(from_time, '%Y-%m-%d')
    return from_date


def set_to_date():
    to_time = date.today()
    to_date = format(to_time, '%Y-%m-%d')
    return to_date