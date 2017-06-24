#! /usr/bin/python
import random

print "TEST"
print "---"

def random_str():
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for x in range(7)])
sorted_by_name = [{'key': random_str(), 'ip': random_str(), 'name': random_str()}
                  ,{'key': random_str(), 'ip': random_str(), 'name': random_str()}]

for item in sorted_by_name:
    copy_command = "echo ssh -i ~/.ssh/%s.pem ubuntu@%s | pbcopy" % (item['key'], item['ip'])
    print "%s | bash='%s' terminal=false" % (item['name'], copy_command)
    print item['ip']
    print "---"
