#! /usr/bin/env python
# -*- coding: utf-8 -*-
# <bitbar.title>Copy Keys</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>syllogismos</bitbar.author>
# <bitbar.author.github>syllogismos</bitbar.author.github>
# <bitbar.desc>copy to clipboard stuff</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/syllogismos/dotfiles/master/bitbar_plugins.symlink/ec2.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/syllogismos/dotfiles/bitbar.symlink</bitbar.abouturl>

import json

print "KEYS"
print "---"


def copy_to_clipboard(show_string, copy_string):
    """
    show_string is what you see in the menu
    copy_string is what gets copied
    """
    copy_command = "echo %s | pbcopy" % (copy_string)
    print "%s | bash='/bin/bash' param1='-c' param2='%s' terminal=false" \
        % (show_string, copy_command)
f = open('/Users/anil/.dotfiles/bitbar_plugins.symlink/keys.json', 'rb')
parsed = json.load(f)
print "EC2"
for key, value in map(lambda x: x.items()[0], parsed['ec2']):
    copy_to_clipboard(key, value)
print "---"
print "Miscellaneous"
# for key, value in items['misc']:
for key, value in map(lambda x: x.items()[0], parsed['misc']):
    copy_to_clipboard(key, value)
