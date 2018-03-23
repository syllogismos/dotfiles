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
import random
import datetime
try:
    client = boto3.client('ec2')
    response = client.describe_instances()
    reservations = response['Reservations']
except:
    reservations = []

ec2_instances = []

print "©"
# print "ec2"
print "---"

e = datetime.datetime.now()
s = e - datetime.timedelta(hours=1)
instance_types_tups = [
                       ('t2.micro', '1, 1, 0.011'),
                       ('c4.large', '2, 3.75, 0.1'),
                       ('c4.xlarge', '4, 7.5, 0.2'),
                       ('c4.2xlarge', '8, 15, 0.39'),
                       ('c4.4xlarge', '16, 30, 0.79'),
                       ('c4.8xlarge', '36, 60, 1.59'),
                       ('c3.large', '2, 3.75, 0.1'),
                       ('c3.xlarge', '4, 7.5, 0.21'),
                       ('c3.2xlarge', '8, 15, 0.42'),
                       ('c3.4xlarge', '16, 30, 0.84'),
                       ('c3.8xlarge', '32, 60, 1.68'),
                       ('m4.large', '2, 8, 0.1'),
                       ('m4.xlarge', '4, 16, 0.2'),
                       ('m4.2xlarge', '8, 32, 0.4'),
                       ('m4.4xlarge', '16, 64, 0.8'),
                       ]
instance_types = dict(instance_types_tups)
av_zones = ['us-east-1b', 'us-east-1c', 'us-east-1d']
spot = client.describe_spot_price_history(StartTime=s, EndTime=e,
                                          InstanceTypes=instance_types.keys(),
                                          ProductDescriptions=['Linux/UNIX (Amazon VPC)'])
"""
spot['SpotPriceHistory'][0] = {u'AvailabilityZone': 'us-east-1a',
  u'InstanceType': 'c4.4xlarge',
  u'ProductDescription': 'Linux/UNIX (Amazon VPC)',
  u'SpotPrice': '9.280000',
  u'Timestamp': datetime.datetime(2017, 6, 21, 11, 10, 35, tzinfo=tzutc())}
"""

spot_modified = {}
for instance in instance_types.keys():
    spot_modified[instance] = {}
    for zone in av_zones:
        relevant_spots = filter(lambda x: (x['InstanceType'] == instance) and
                                          (x['AvailabilityZone'] == zone),
                                spot['SpotPriceHistory'])
        sorted_spots = sorted(relevant_spots, cmp=lambda a, b: cmp(a['Timestamp'], b['Timestamp']))
        spot_modified[instance][zone] = sorted_spots[-1]
amis = client.describe_images(Owners=['self'])['Images']
"""
amis[0] = {u'Architecture': 'x86_64',
  u'BlockDeviceMappings': [{u'DeviceName': '/dev/sda1',
    u'Ebs': {u'DeleteOnTermination': False,
     u'Encrypted': False,
     u'SnapshotId': 'snap-0c937ae0e4a9dcd90',
     u'VolumeSize': 30,
     u'VolumeType': 'gp2'}}],
  u'CreationDate': '2017-06-21T15:28:36.000Z',
  u'Description': 'runenv image',
  u'Hypervisor': 'xen',
  u'ImageId': 'ami-ce133ad8',
  u'ImageLocation': '051029754231/runenv 21st June',
  u'ImageType': 'machine',
  u'Name': 'runenv 21st June',
  u'OwnerId': '051029754231',
  u'Public': False,
  u'RootDeviceName': '/dev/sda1',
  u'RootDeviceType': 'ebs',
  u'State': 'available',
  u'VirtualizationType': 'hvm'}
"""


def format_date_string(d):
    return datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.000Z')

sorted_amis = sorted(amis,
                     cmp=lambda a, b: cmp(format_date_string(a['CreationDate']),
                                          format_date_string(b['CreationDate'])),
                     reverse=True)


def copy_to_clipboard(show_string, copy_string):
    """
    show_string is what you see in the menu
    copy_string is what gets copied
    """
    copy_command = "echo %s | pbcopy" % (copy_string)
    print "%s | bash='/bin/bash' param1='-c' param2='%s' terminal=false" \
        % (show_string, copy_command)

# def random_str():
#     return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for x in range(7)])
# sorted_by_name = [{'key': random_str(), 'ip': random_str(), 'name': random_str()}
#                   ,{'key': random_str(), 'ip': random_str(), 'name': random_str()}]

for reservation in reservations:
    for instance in reservation['Instances']:
        # if instance['State']['Name'] != 'running':
        #     continue
        name = None
        prod = None
        tags = {}
        if 'Tags' in instance.keys():
            for tag in instance['Tags']:
                if tag['Key'] == "Name":
                    name = tag['Value']
                elif tag['Key'] == "Production":
                    prod = tag['Value']
                else:
                    tags[tag['Key']] = tag['Value']
        key_name = instance['KeyName']

        if 'PublicIpAddress' not in instance:
            ip = 'Public Ip'
        else:
            ip = instance['PublicIpAddress']

        if 'PrivateIpAddress' not in instance:
            pr_ip = 'Private Ip'
        else:
            pr_ip = instance['PrivateIpAddress']

        if 'InstanceId' not in instance:
            instance_id = 'instance id'
        else:
            instance_id = instance['InstanceId']

        if name is None or name == '':
            name = 'default'

        instance_type = instance['InstanceType']
        av_zone = instance['Placement']['AvailabilityZone']

        if 'InstanceLifecycle' in instance:
            if instance['InstanceLifecycle'] == 'spot':
                if instance_type in instance_types:
                    name += ' (%0.2f/%.2f)' % (float(spot_modified[instance_type][av_zone]['SpotPrice']),
                                               float(instance_types[instance_type].split(',')[2]))
                name += ' SPOT'
        ec2_instances.append({'name': name, 'ip': ip, 'key': key_name,
                              'instance_id': instance_id, 'pr_ip': pr_ip,
                              'instance_type': instance_type,
                              'av_zone': av_zone,
                              'prod': prod,
                              'tags': tags
                              })

def print_instance_details(instances):
    for item in instances:
        copy_command = "echo ssh -i ~/.ssh/%s.pem ubuntu@%s | pbcopy" % (item['key'], item['ip'])
        # print "%s(%s)" % (item['name'], item['ip'])
        print item['name']
        # print "--" + item['ip']
        print "--copy ssh | bash='/bin/bash' param1='-c' param2='%s' terminal=false" \
            % (copy_command)
        copy_to_clipboard("--" + item['ip'], item['ip'])
        copy_to_clipboard("--" + item['pr_ip'], item['pr_ip'])
        for tag in item['tags'].items():
            print "--" + str(tag[0])
            print "----" + str(tag[1])
    
        alarm_name = item['name'] \
            .upper() \
            .replace(' ', '-') \
            .replace('/', '-') \
            .replace('$', '') \
            .replace('(', '') \
            .replace(')', '')
        alarm_name = 'LOW-CPU-MON-' + alarm_name
    
        low_alarm_string = "cloudwatch put-metric-alarm --alarm-name %s \
            --alarm-description %s --metric-name CPUUtilization \
            --namespace AWS/EC2 --statistic Average --period 300 \
            --threshold 20 --comparison-operator LessThanThreshold \
            --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 \
            --alarm-actions arn:aws:sns:us-east-1:051029754231:cpu-alerts-deep-learning \
            --unit Percent" % (alarm_name, "Alarm_when_CPU_less_than_20%", item['instance_id'])
        print "--Low CPU Alarm | bash='aws' param1='%s' terminal=true" % (low_alarm_string)
        print "--Delete Alarm | bash='aws' param1='cloudwatch delete-alarms --alarm-name %s' terminal=true" % (alarm_name)
    
        print "--Start | bash='/usr/local/bin/aws' param1='ec2' param2='start-instances' param3='--instance-ids' param4='%s' param5='>>/tmp/bitbar_ec2' terminal=true" % (item['instance_id'])
        print "--Stop | bash='/usr/local/bin/aws' param1='ec2' param2='stop-instances' param3='--instance-ids' param4='%s' param5='>>/tmp/bitbar_ec2' terminal=true" % (item['instance_id'])
        print "--Restart | bash='/usr/local/bin/aws' param1='ec2' param2='reboot-instances' param3='--instance-ids' param4='%s' param5='>>/tmp/bitbar_ec2' terminal=true" % (item['instance_id'])
        try:
            suffix = ' (%s)' % (','.join(instance_types[item['instance_type']].split(',')[:2]))
        except:
            suffix = ''
        print "--" + item['instance_type'] + suffix
        print "--" + item['av_zone']
        if item['prod'] is None:
            print "--TERMINATE | bash='/usr/local/bin/aws' param1='ec2' param2='terminate-instances' param3='--instance-ids' param4='%s' param5='>>/tmp/bitbar_ec2' terminal=true" % (item['instance_id'])
        else:
            print "--TERMINATE"

sorted_by_name = sorted(ec2_instances, key=lambda k: k['name'])
running = filter(lambda x: x['ip'] != 'Public Ip', sorted_by_name)
stopped = filter(lambda x: x['ip'] == 'Public Ip', sorted_by_name)

# sorted_by_name.append({'name': 'luzlasdf', 'key': 'lol', 'ip': 'lolz'})
print "Instances"
print_instance_details(running)
print "---"
print "Stopped"
print_instance_details(stopped)
print "---"
print "AMIs"
for ami in sorted_amis:
    print ami['Name']
    # print ami['Description']
    for instance_type in map(lambda x: x[0], instance_types_tups):
        print '--%s(%s)' % (instance_type, instance_types[instance_type])
        for av_zone in av_zones:
            copy_string = "spot -t start -i %s -z %s -a %s -p 1.2 -n" % (instance_type, av_zone, ami['ImageId'])
            show_string = '----%s(%0.2f)' % (av_zone, float(spot_modified[instance_type][av_zone]['SpotPrice']))
            copy_to_clipboard(show_string, copy_string)
            # print '----' + spot_modified[instance_type][av_zone]['SpotPrice']
print "---"
