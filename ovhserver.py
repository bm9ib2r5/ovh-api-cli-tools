#!/usr/bin/python

# -*- encoding: utf-8 -*-
# Server management

import ovh
import urllib3
import click
#import requests
#requests.packages.urllib3.disable_warnings()
import json
import sys
from tabulate import tabulate

@click.group()
@click.version_option(version='0.0.1')
def ovhserver():
    pass

@ovhserver.command()
def list():
    print('Server list')
    number =0
    tableServerList = []
    client = ovh.Client()
    serverlist=client.get('/dedicated/server/')
    for server in serverlist:
        number = number+1
        serverrev=client.get('/dedicated/server/'+server)
        tableServerList.append([number,server,serverrev['reverse']])
    print tabulate(tableServerList, headers=['NUM','ServerName', 'RevDNS'])

@ovhserver.command()
@click.argument('servername')
def properties(**kwargs):
    print('Server properties'.format(kwargs['servername']))
    client = ovh.Client()
    tableServerProperties = []
    serverProperties=client.get('/dedicated/server/'+format(kwargs['servername']))
    tableServerProperties.append([serverProperties['name'],serverProperties['reverse'],serverProperties['ip'],serverProperties['datacenter'],serverProperties['rack'],serverProperties['serverId'],serverProperties['state'],serverProperties['monitoring'],serverProperties['os']])
    print tabulate(tableServerProperties, headers=['ServerName', 'Reverse','IP','datacenter','rack','serverId','state','monitoring','os'])

@ovhserver.command()
@click.argument('servername')  # add the name argument
def tasks(**kwargs):
    print('Server ip(s)'.format(kwargs['servername']))
    client = ovh.Client()
    tableServerTasks = []
    serverTasks=client.get('/dedicated/server/'+format(kwargs['servername'])+'/task')
    print serverTasks
    for tasksid in serverTasks:
            serverTasksDetails=client.get('/dedicated/server/'+format(kwargs['servername'])+'/task/'+format(tasksid))
            tableServerTasks.append([format(kwargs['servername']),serverTasksDetails['taskId'],serverTasksDetails['function'],serverTasksDetails['startDate'],serverTasksDetails['lastUpdate'],serverTasksDetails['doneDate'],serverTasksDetails['status'],serverTasksDetails['comment']])

    print tabulate(tableServerTasks, headers=['taskId', 'function', 'startDate', 'lastUpdate', 'doneDate', 'status', 'comment'])

@ovhserver.command()
@click.argument('servername')  # add the name argument
def reboot(**kwargs):

    client = ovh.Client()
    serverProperties=client.get('/dedicated/server/'+format(kwargs['servername']))
    print('Server reboot: '+format(kwargs['servername'])+' ( '+serverProperties['reverse']+' )')

    if click.confirm('Do you want to continue?'):
        print 'Rebooting server: '+format(kwargs['servername'])
        # client = ovh.Client()
        # server=client.get('/dedicated/server/'+format(kwargs['servername'])+'/reboot')

if __name__ == '__main__':
    ovhserver()
