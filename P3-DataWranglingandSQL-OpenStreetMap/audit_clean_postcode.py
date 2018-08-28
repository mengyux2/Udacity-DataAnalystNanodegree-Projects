import xml.etree.cElementTree as ET
import pprint
osm_sample = 'temple_terrace.osm'
osm_filename = 'tampa.osm'
def count_postcodes(filename):
    postcodes = {}
    for event, elem in ET.iterparse(filename, events=('start', 'end')):
        if event == 'end':
            key = elem.attrib.get('k')
            if key == 'addr:postcode':
                postcode = elem.attrib.get('v')
                if postcode not in postcodes:
                    postcodes[postcode] = 1
                else:
                    postcodes[postcode] += 1
    return postcodes


#start_time = time.time()

postcodes = count_postcodes(osm_filename)
sorted_by_occurrence = [(k, v) for (v, k) in sorted([(value, key) for (key, value) in postcodes.items()], reverse=True)]

print 'Postcode values and occurrence in tampa.osm'
pprint.pprint(sorted_by_occurrence)

#print('\n--- %s seconds ---' % (time.time() - start_time))

def clean_postcode(postcode_value):

    if len(postcode_value)!=5:
        postcode=postcode_value[0:5]
                        
        return postcode


#print('\n--- %s seconds ---' % (time.time() - start_time))

#postcodes = count_postcodes('tampa_cleaned_postcode.xml')
#sorted_by_occurrence = [(k, v) for (v, k) in sorted([(value, key) for (key, value) in postcodes.items()], reverse=True)]

#print 'Postcode values and occurrence after cleaning:\n'
#pprint.pprint(sorted_by_occurrence)