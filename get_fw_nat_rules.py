import sys
import csv
import json
import requests
import pyfiglet
import common_bits
import nat_network
import nat_service
from pprint import pprint
from collections import ChainMap


def Banner():
    """Print fancy banner for all to see."""
    main_banner = pyfiglet.figlet_format("  UTM     NAT", font = "slant")
    sub_banner1 = pyfiglet.figlet_format("tool", font = "isometric1")
    sub_banner2 = "      -Generate a CSV file of Sophos UTM NAT statements-"
    sub_banner3 = "           via REST API using the power of Python"

    print()
    print('=' * 62)
    print(main_banner)
    print(sub_banner1)
    print()
    print(sub_banner2)
    print(sub_banner3)
    print()
    print('=' * 62)
    print() 


def get_nat_rules():
    """Returns list object of all nat rules via REST API."""
    url = '{}/packetfilter/nat'.format(common_bits.base_url)
    result = common_bits.get_request(url, common_bits.headers, common_bits.payload)

    return result.json()


def get_request_url(rule):
    """Return parsed data from API of interesting objects in rule."""
    rule_result = []
    for key, value in rule.items():
        if (key == 'destination' or
           key == 'destination_nat_address' or
           key == 'source' or
           key == 'source_nat_address') and value:
            result = nat_network.get_request_network(value)
            data = {
                    key:result
            }
            rule_result.append(data)
        elif (key == 'service' or
             key == 'destination_nat_service') and value:
            result = nat_service.get_request_service(value)
            data = {
                    key:result
            }
            rule_result.append(data)
        else:
            data = {
                    key:value
            }
            rule_result.append(data)
    
    final_result = []
    final_result.append(dict(ChainMap(*rule_result)))
    
    return final_result


def main():

    Banner()

    print('[+] Retrieving all NAT objects from {}/packetfilter/nat'.format(common_bits.base_url))
    rules = get_nat_rules()
    rule_list = []

    print('[+] Parsing each statement endpoint values... Please wait')
    for nat in rules:
        r = get_request_url(nat)
        rule_list.append(r)

    final_rule_list = []
    common_bits.removeNestedLists(rule_list, final_rule_list)

    keys = ['_locked', '_ref', '_type', 'auto_pf_in', 'auto_pfrule',
            'comment', 'destination', 'destination_nat_address',
            'destination_nat_service', 'group', 'ipsec', 'log',
            'mode', 'name', 'service', 'source', 'source_nat_address',
            'source_nat_service', 'status']

    output_file_name = "fw_nat_rules.csv"
    print('[+] Writing result to file "{}"'.format(output_file_name))
    with open('{}'.format(output_file_name), 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(final_rule_list)

    print('[+] Complete!')

if __name__ == '__main__':
    main()
