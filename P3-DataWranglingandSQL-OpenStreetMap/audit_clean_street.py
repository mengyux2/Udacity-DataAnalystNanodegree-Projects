import xml.etree.cElementTree as ET
import re
from collections import defaultdict
osm_sample = 'temple_terrace.osm'
osm_filename = 'tampa.osm'

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "av":"Avenue",
            "ave": "Avenue",
           'Ave.':"Avenue",
           'Blvd':"Boulevard",
           'Blvd.':"Boulevard",
           'Bolevard':"Boulevard",
           'Boulvard':"Boulevard",
           'Cir':"Circle",
           'Cswy':"Causeway",
           'Ct':"Court",
           'Dr':"Drive",
           'Dr.':"Drive",
           'Hwy':"Highway",
           'Ln':"Lane",
           'Pkwy':"Parkway",
           'Pky':"Parking",
           'Pl':"Plaza",
           'Rd':"Road",
           'Rd.':"Road",
           'St':"Street",
           'street':"Street",
           'dr':"Drive",
           'drive':"Drive"          
}

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:street":
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

#audit(osm_filename)

def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping.keys():
            name = re.sub(street_type_re, mapping[street_type], name)

    return name

street_types = audit(osm_filename)

for st_type, ways in street_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        if name != better_name:
            print name, "=>", better_name

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")


def clean_street_name(filename, cleaned_filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    for tag in root.findall('*/tag'):
        if is_street_name(tag):
            name = tag.get('v')
            better_name = update_name(name, mapping)
            tag.set('v', better_name)

    return tree.write(cleaned_filename)


