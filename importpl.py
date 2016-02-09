#!/usr/bin/python
# Original Author: http://www.10flow.com/wp-content/uploads/2012/10/importpl.py_.gz

############################################################
#USER CONFIGURATION: SET YOUR PATHS
win_path = '' #be sure to use double backslashes if it's a Windows path!
lin_path = ''
############################################################

import codecs
import csv
import sys
import os
import urllib2

print "############################################################"
print "iTunes Playlist to Rhythmbox Playlist Converter"
print "This script will convert your iTunes playlist into a"
print "Rhythmbox-compatible playlist.\n"
print "Author: Justin Mitchell"
print "Date: February 2016"
print "Credits: Scott Sawyer\nhttp://www.10flow.com/wp-content/uploads/2012/10/importpl.py_.gz"
print "Added additional UTF-8 support and improved error handling\nand message responses"
print "############################################################\n"

if not win_path or not lin_path:
    print "You are required to adjust the values for 'win_path' and"
    print "'lin_path' before executing this script"
    sys.exit()

reload(sys)  
sys.setdefaultencoding('utf8')

file_in = sys.argv[1]
file_out = file_in + ".pls"

filename = file_in.split('/')[-1]
parts = filename.split('.')
if len(parts) > 1:
    pl_name = ".".join(parts[:-1])
else:
    pl_name = filename

f1 = codecs.open(file_in,'r','utf-16')

lines = []
for line in f1:
    lines.append(line.split('\t'))
f1.close()

print "Saving to file:\t" + file_out

f2 = codecs.open(file_out,'w','utf-8')

f2.write('[playlist]\n')
f2.write('X-GNOME-Title={0}\n'.format(pl_name))
f2.write('NumberOfEntries={0}\n'.format(len(lines)-1))

count = 0
error = 0

for i,l in enumerate(lines[1:]):
    win_file = l[-1].strip()
    title = l[0].strip()

    lin_file = win_file.replace(win_path,lin_path)
    lin_file = lin_file.replace('\\','/')

    lin_file = lin_file.replace("'", "\'").replace(';', '\;')

    if os.path.exists(lin_file):
        lin_uri = 'file://{0}'.format(lin_file.encode('utf-8').replace(' ','%20'))
        try:
            #write it out
            f2.write('File{0}={1}\n'.format(count, lin_uri))
            f2.write('Title{0}={1}\n'.format(count, title))
            count += 1
        except Exception, e:
            print str(e) + ":\t" + "Couldn't write uri: " + lin_uri.replace(' ','%20')
            error += 1

    else:
        print 'Could not find ' + lin_file
f2.close()

print "Wrote {0} songs, encountered {1} errors".format(count, error)
