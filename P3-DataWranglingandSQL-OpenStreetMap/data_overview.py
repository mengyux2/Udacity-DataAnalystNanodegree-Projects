import os
import os.path
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

osm_sample = 'temple_terrace.osm'
osm_filename = 'tampa.osm'
def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename, events=('start', )):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags

tags = count_tags(osm_filename)
sorted_by_occurrence = [(k, v) for (v, k) in sorted([(value, key) for (key, value) in tags.items()], reverse=True)]

print 'Element types and occurrence of tampa.osm'
pprint.pprint(sorted_by_occurrence)

##regular expressions to define tag key characters
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            k = tag.get('k')
            if lower.search(element.attrib['k']):
                keys['lower'] = keys['lower'] + 1
            elif lower_colon.search(element.attrib['k']):
                keys['lower_colon'] = keys['lower_colon'] + 1
            elif problemchars.search(element.attrib['k']):
                print 'problemchars:',k
                keys['problemchars'] = keys['problemchars'] + 1
            else:
                #print k
                keys['other'] = keys['other'] + 1
    
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

print 'Key types and occurrence of tampa.osm'
pprint.pprint(process_map(osm_filename))

def count_keys(filename):
    keys = {}
    for event, elem in ET.iterparse(filename, events=('start', 'end')):
        if event == 'end':
            key = elem.attrib.get('k')
            if key:
                if key not in keys:
                    keys[key] = 1
                else:
                    keys[key] += 1
    return keys

keys = count_keys(osm_filename)
sorted_by_occurrence = [(k, v) for (v, k) in sorted([(value, key) for (key, value) in keys.items()], reverse=True)]

print 'Keys and occurrence in tampa.osm'
pprint.pprint(sorted_by_occurrence[0:20]) ##print 20 most frequent keys

