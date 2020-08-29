import sys
import requests
import common_bits


def gen_network_urls():
    """Return full URL path for each service type."""
    base_url = common_bits.base_url
    all_base_service_urls = []
    network_urls = [
            'aaa', 'any', 'availability_group', 'dns_host',
            'group', 'host', 'interface_address', 'interface_broadcast',
            'interface_network', 'multicast', 'network', 'range'
            ]
    for item in network_urls:
        base_network_url = '{}/network/{}'.format(base_url,item)
        all_base_service_urls.append(base_network_url)

    return all_base_service_urls


def network_any(network):
    """Return data from /network/any object."""
    network_type = network['type']
    network = '{}/{}'.format(network['data']['address'], network['data']['netmask'])
    data = {
            "type":network_type,
            "network":network
    }
    return data


def network_group(ng):
    """Return data from /network/group object."""
    network_type = ng['type']
    members = ng['data']['members']
    network_urls = gen_network_urls()
    network_data = []
    for member in members:
        for url in network_urls:
            network_url = '{}/{}'.format(url,member)
            result = common_bits.get_request(network_url, common_bits.headers, common_bits.payload)
            if result.status_code == 200:
                network = result.json()
                network_type = network['_type']
                data = {
                        "type":network_type,
                        "data":network
                }
                network_data.append(data)
    result = parser(network_data)
    return result


def network_host(host):
    """Return data from /network/host object."""
    network_type = host['type']
    address = host['data']['address']
    data = {
            "type":network_type,
            "address":address
    }
    return data


def network_interface_address(int_address):
    """Return data from /network/interface_address object."""
    network_type = int_address['type']
    address = int_address['data']['address']
    data = {
            "type":network_type,
            "address":address
    }
    return data


def network_network(network):
    """Return data from /network/network object."""
    network_type = network['type']
    address = network['data']['address']
    data = {
            "type":network_type,
            "address":address
    }
    return data


def parser(ref_object):
    """Return object specific data by type""" 
    ref_object_data = []
    for i in ref_object:
        if i['type'] == 'network/any':
            result = network_any(i)
            ref_object_data.append(result)
        elif i['type'] == 'network/group':
            result = network_group(i)
            ref_object_data.append(result)
        elif i['type'] == 'network/host':
            result = network_host(i)
            ref_object_data.append(result)
        elif i['type'] == 'network/interface_address':
            result = network_interface_address(i)
            ref_object_data.append(result)
        elif i['type'] == 'network/network':
            result = network_network(i)
            ref_object_data.append(result)
        else:
            ref_object_data.append(ref_object)

    return ref_object_data


def get_request_network(value):
    """Return parsed data from API of object type 'service'"""
    network_data = []
    base_urls = gen_network_urls()
    
    for url in base_urls:
        network_url = '{}/{}'.format(url, value)
        result = common_bits.get_request(network_url, common_bits.headers, common_bits.payload)

        if result.status_code == 200:
            network = result.json()
            network_type = network['_type']

            data = {
                    "type":network_type,
                    "data":network
            }
            network_data.append(data)
            break

    result = parser(network_data)

    final_result = []
    common_bits.removeNestedLists(result, final_result)

    return final_result
    
