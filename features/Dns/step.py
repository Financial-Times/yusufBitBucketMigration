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


@step(u'Given I set the headers with api key as headers')
def given_i_set_the_headers_with_api_key_as_headers(step):
    header = set_param()
    world.headers = header['headers']


@step(u'Given I set the url as url')
def given_i_set_the_url_as_url(step):
    uri = set_param()
    world.url = uri['dns_url']['zones']


@step(u'Given I set the create endpoint url as url')
def given_i_set_the_create_endpoint_url_as_url(step):
    uri = set_param()
    world.createUrl = uri['dns_url']['create']


@step(u'Given I set the delete endpoint url as url')
def given_i_set_the_delete_endpoint_url_as_url(step):
    uri = set_param()
    world.delUrl = uri['dns_url']['create']


@step(u'Given I set the data as "([^"]*)"')
def given_i_set_the_data_as_group1(step, data_section):
    dat = set_param()
    world.createData = dat[data_section]


@step(u'Then check the dns entry is not available')
def then_check_the_dns_entry_is_not_available(step):
    check_request()


@step(u'Given I make get zone request to the api with url "([^"]*)"')
def given_i_make_get_zone_request_to_the_api_with_url_group1(step, group1):
    world.res = get_zones(world.url, world.headers)


@step(u'Given I make create dns entry request to the api with url "([^"]*)"')
def given_i_make_create_dns_entry_request_to_the_api_with_url_group1(step, group1):
    world.res = make_an_api_request(world.createUrl, world.createData, world.headers)


@step(u'Given I make a call to the api with url "([^"]*)"')
def given_i_make_a_call_to_the_api_with_url_group1(step, group1):
    world.res = api_delete_request(world.delUrl, world.zone_name_data, world.headers)


@step(u'Given I set the section as "([^"]*)"')
def given_i_set_the_section_as_group1(step, section):
    world.section = section


@step(u'When I set the url in the format "([^"]*)"')
def when_i_set_the_url_in_the_format_group1(step, setUrl):
    name = get_name()
    zone = get_zone()
    world.zoneNameUrl = setUrl % (zone, name)


@step(u'When I make api get name and zone request')
def when_i_make_api_get_name_and_zone_request(step):
    world.res = get_zones(world.zoneNameUrl, world.headers)


@step(u'Then verify zone and name exist in dns entry in format "([^"]*)"')
def then_verify_zone_and_name_exist_in_dns_entry_in_format_group1(step, fqdn):
    data = convert_to_json()
    world.fqdn = data[fqdn]
    fqdnResponse = world.fqdn.encode('ascii')
    assert get_name() in fqdnResponse, "Name of dns entry not exist"
    assert get_zone() in fqdnResponse, "Zone not present in dns entry"


@step(u'Then the status code should be 200')
def then_the_status_code_should_be_200(step):
    assert_equal(world.res.status_code, 200)


@step(u'Then verify that dns get zone endpoint retrieves an existing zone "([^"]*)"')
def then_verify_that_dns_get_zone_endpoint_retrieves_an_existing_zone_group1(step, expected):
    data = convert_to_json()
    key = data.keys()
    zonekey = key[0]
    zones = data[zonekey]
    for index in range(len(zones)):
        zones[index] = zones[index].encode('ascii')
    assert expected in zones, 'Zone %s not in the zone list' % expected


@step(u'Then verify new dns entry response is "([^"]*)"')
def then_verify_new_dns_entry_in_format_group1(step, response):
    data = convert_to_json()
    assert data['response'] == response, "Create DNS not working properly"


@step(u'Then verify dns record "([^"]*)" is "([^"]*)"')
def then_verify_dns_record_group1_is_group2(step, typeExpected, recordType):

    if recordType == 'A':
        responseType = world.resDict[typeExpected].encode('ascii')
        assert recordType == responseType,  "DNS record type not A record"
    elif recordType == 'CNAME':
        responseType = world.resDict[typeExpected].encode('ascii')
        assert recordType == responseType, "DNS record type not CNAME record"
    else:
        assert False, "DNS Record type unknown "


@step(u'When I set the dns name and zone data')
def when_i_set_the_dns_name_and_zone_data(step):
    world.zone_name_data = get_data_dict()


@step(u'Then verify that delete response is "([^"]*)"')
def then_verify_that_delete_response_is_group1(step, response):
    del_response = convert_to_json()
    assert del_response['response'] == response, "Delete DNS not working properly"


def set_param():
    return world.config_obj.dataload(filename)


def get_zones(url, headers):
    world.response = requests.get(url=url, headers=headers)
    return world.response


def convert_to_json():
    return json.loads(world.response.text)


def make_an_api_request(url,data,headers):
    world.response = requests.post(url=url, data=json.dumps(data), headers=headers)
    return world.response


def api_delete_request(url, data,headers):
    world.response = requests.delete(url=url, data=json.dumps(data), headers=headers)
    return world.response


def get_fqdn():
    data = set_param()
    name = data[world.section]['name']
    zone = data[world.section]['zone']
    s = "."
    seq = (name, zone)
    new_str = s.join(seq)
    return s.join(seq)


def get_name():
    data = set_param()
    world.name = data[world.section]['name']
    return world.name


def get_zone():
    data = set_param()
    world.zone = data[world.section]['zone']
    return world.zone


def get_data_dict():
    data = set_param()
    data_dict = {}
    data_dict['name'] = data[world.section]['name']
    data_dict['zone'] = data[world.section]['zone']
    return data_dict


def send_request():
    name = get_name()
    zone = get_zone()
    world.checkUrl = "https://dns-api.in.ft.com/v2/name/%s/%s" % (zone, name)
    return world.checkUrl


def check_request():
    world.del_data = get_data_dict()
    url = send_request()
    world.resp = requests.get(url=url, headers=world.headers)
    response_text = json.loads(world.resp.text)
    resp_keys = response_text.keys()
    world.new_res = ""
    world.new_text = {}
    uri = set_param()
    world.delUri = uri['dns_url']['create']
    if len(response_text) == 4 and 'stackTrace' in resp_keys:
        print "DNS entry does not ", resp_keys
    elif len(response_text) == 4 and 'fqdn' in resp_keys:
        print "DNS entry already exist", resp_keys
        del_req = api_delete_request(world.delUri, world.del_data, world.headers)
        del_req_response = json.loads(del_req.text)
        assert  del_req_response['response'] == 'OK', "Delete operation not working"
    else:
        pass

