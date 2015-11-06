#!/usr/bin/python

# -*- encoding: utf-8 -*-
# Server management
#
# --list
# --move=[all] --from=[service] --to=[service]
# --move=[ip] --to=[service]

import ovh
import urllib3
import click
#import requests
#requests.packages.urllib3.disable_warnings()
import sys
from tabulate import tabulate

def listallip():
    print('IP Failover List:')
    params = {}
    params['type'] = 'failover'

    client = ovh.Client()
    tableIpList = []

    ipList=(client.get('/ip/', **params))
    for ip in ipList:
        IP=ip.split('/')
        ipProperties=client.get('/ip/'+IP[0])
        tableIpList.append([ipProperties['ip'],ipProperties['routedTo']['serviceName'],ipProperties['description']])
    print tabulate(tableIpList, headers=['ip','routedTo','description'])

def movesingleip(ip,service):
    client = ovh.Client()
    print "client.post('/ip/"+ip+"/move', to="+service+")"
    # client.post('/ip/'+ip+'/move', to=service)

def moveallip(srcservice,dstservice):
    client = ovh.Client()
    params = {}
    failover_ips = []

    params['type'] = 'failover'
    params['routedTo.serviceName'] = srcservice
    failover_ips += client.get('/ip', **params)
    for failover_ip in failover_ips:
        print "client.post('/ip/"+failover_ip+"/move', to="+dstservice+")"
        # client.post('/ip/'+failover_ip+'/move', to=dstservice)

def helpmsg():
    print "Use -h/--help."


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
@click.option('--list', help='List all ips', required=False, is_flag=True)
@click.option('--src', help='source SERVICENAME', required=False)
@click.option('--dst', help='destination SERVICENAME', required=False)
@click.option('--ip', help='IP address', required=False)
@click.option('--move', help='all IPs (require "--src" and "--dst" option / single IP (require "--ip" and --dst option)', required=False, type=click.Choice(['all', 'ip']))
def ovhip(list,src,dst,move,ip):
    if list:
        listallip()

    if move == 'ip':
        if ip and dst:
            movesingleip(ip,dst)
        else:
            helpmsg()
    elif move == 'all':
        if src and dst:
            moveallip(src,dst)
        else:
            helpmsg()
    else:
        helpmsg()
if __name__ == '__main__':
    ovhip()

