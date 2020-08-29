import sys
import requests
import common_bits


def gen_service_urls():
    """Return full URL path for each service type."""
    base_url = common_bits.base_url
    all_base_service_urls = []
    service_urls = ['ah', 'any', 'esp', 'group', 'icmp', 'icmpv6', 'ip', 'tcp', 'tcpudp', 'udp']
    for item in service_urls:
        base_service_url = '{}/service/{}'.format(base_url,item)
        all_base_service_urls.append(base_service_url)

    return all_base_service_urls


def service_any(service):
    """Return data from /service/any object."""
    service_type = service['type']
    service_port = service['data']['name']
    data = {
            "type":service_type,
            "dst":service_port
    }
    return data


def service_group(sg):
    """Return data from /service/group object."""
    service_type = sg['type']
    members = sg['data']['members']
    service_urls = gen_service_urls()
    service_data = []
    for member in members:
        for url in service_urls:
            service_url = '{}/{}'.format(url,member)
            result = common_bits.get_request(service_url, common_bits.headers, common_bits.payload)
            if result.status_code == 200:
                service = result.json()
                service_type = service['_type']
                data = {
                        "type":service_type,
                        "data":service
                }
                service_data.append(data)
    result = parser(service_data)
    return result


def service_ip(service):
    """Return data from /service/ip object."""
    service_type = service['type']
    service_protocol = service['data']['proto']
    data = {
            "type":service_type,
            "protocol":service_protocol
    }
    return data


def service_tcp_udp(service):
    """Return data from /service/tcpudp object."""
    service_type = service['type']
    src_port = '{}:{}'.format(service['data']['src_low'],service['data']['src_high'])
    if service['data']['dst_high'] == service['data']['dst_low']:
        dest_port = service['data']['dst_low']
    else:
        dest_port = '{}:{}'.format(service['data']['dst_low'],service['data']['dst_high'])
    data = {
            "type":service_type,
            "src":src_port,
            "dst":dest_port
    }
    return data


def parser(ref_object):
    """Return object specific data by type""" 
    ref_object_data = []
    for i in ref_object:
        if i['type'] == 'service/any':
            result = service_any(i)
            ref_object_data.append(result)
        elif i['type'] == 'service/group':
            result = service_group(i)
            ref_object_data.append(result)
        elif i['type'] == 'service/ip':
            result = service_ip(i)
            ref_object_data.append(result)
        elif (i['type'] == 'service/tcp' or
              i['type'] == 'service/udp' or
              i['type'] == 'service/tcpudp'):
            result = service_tcp_udp(i)
            ref_object_data.append(result)
        else:
            ref_object_data.append(ref_object)

    return ref_object_data


def get_request_service(value):
    """Return parsed data from API of object type 'service'"""
    service_data = []
    base_urls = gen_service_urls()
    
    for url in base_urls:
        service_url = '{}/{}'.format(url, value)
        result = common_bits.get_request(service_url, common_bits.headers, common_bits.payload)

        if result.status_code == 200:
            service = result.json()
            service_type = service['_type']

            data = {
                    "type":service_type,
                    "data":service
            }
            service_data.append(data)
            break

    result = parser(service_data)

    final_result = []
    common_bits.removeNestedLists(result, final_result)

    return final_result

