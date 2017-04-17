#! /Users/anil/anaconda2/bin/python
# -*- coding: utf-8 -*-
# <bitbar.title>EC2 SSH</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>syllogismos</bitbar.author>
# <bitbar.author.github>syllogismos</bitbar.author.github>
# <bitbar.desc>Lists all EC2 instances by Name, IP, and allow you to copy the ssh command</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/syllogismos/dotfiles/master/bitbar_plugins.symlink/ec2.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/syllogismos/dotfiles/bitbar.symlink</bitbar.abouturl>

import boto3
try:
    client = boto3.client('ec2')
    response = client.describe_instances()
    reservations = response['Reservations']
except:
    reservations = []

ec2_instances = []

print "©"
print "---"

for reservation in reservations:
    for instance in reservation['Instances']:
        # if instance['State']['Name'] != 'running':
        #     continue
        if 'Tags' in instance.keys():
            for tag in instance['Tags']:
                if tag['Key'] == "Name":
                    key_name = instance['KeyName']
                    if 'PublicIpAddress' not in instance:
                        ip = 'terminated'
                    else:
                        ip = instance['PublicIpAddress']
                    name = tag['Value']
                    ec2_instances.append({'name': name, 'ip': ip, 'key': key_name})


sorted_by_name = sorted(ec2_instances, key=lambda k: k['name'])

for item in sorted_by_name:
    copy_command = "ssh\ -i\ ~/.ssh/%s.pem\ ubuntu@%s\ |\ pbcopy" % (item['key'], item['ip'])
    # param2 = "\'import pyperclip; pyperclip.copy(%s)\'" % copy_command
    # python_command = """python param1=-c param2=%s""" % param2
    bash_command = "echo param1=%s" % copy_command
    print "%s | bash=%s terminal=false" % (item['name'], bash_command)
    print item['ip']
    print "---"
