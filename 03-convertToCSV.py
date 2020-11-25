#!/usr/bin/env python
# coding: utf-8

# # Third submission
# 
# ## Changes required
# 
# 
# 
# 
# ### (Optional) Improving the shape_element() function
# 
# This is the current shape_element function's definition:
# 
# def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
#                   problem_chars=PROBLEMCHARS, default_tag_type='regular'):
# 
# Currently, these four parameters node_attr_fields to default_tag_type were never used in the code. Instead, the constants were used e.g. NODE_FIELDS instead of node_attr_fields. This issue did not cause the functions to stop working properly, so I do not mark this as failing the specification, but I strongly suggest to replace the constants with parameter variables so you can more easily migrate the functions to other projects.
# 
# ***To be honest, it was already tough for me as is. I deleted the useless arguments but I prefer to let as is***
# 
# 
# ### Using DocString
# 
# I read a little bit of sphinx. It seems pretty productive, I'll use it in the next projects.
# 
# 
# ### Updates not applied
# 
# Update functions need to be called from inside the shape_element() function to ensure that records are cleaned before they are sent to the database.
# 
# See that in the file 02-cityNames-process.py you have a mapping variable to correct the street names. This variable needs to be utilized when iterating through the elements i.e. in the shape_element() function in 03-convertToCSV.py.
# 
# ### Some of the problems encountered during data audit are cleaned programmatically.
# 
# Update and correction functions need to be called from shape_element() function so they may be applied prior to extracting the osm file into the dataset.
# 
# 
# ***I have added mapping dic and an if statement to check if the data is 'addr:city'. If yes we apply the cleaning.
# 
# 
# ```python
# 
# if subElement.get('k') == 'addr:city':
#     #print ("corriger ", subElement.get('v'))
#     #print ("corrigé ", mapping[subElement.get('v')])
#     tag_dict['value'] = mapping[subElement.get('v')]
# else:
#     tag_dict['value'] = subElement.get('v')
# ```
# 
# 
# 
# 
# 
# ```python
# mapping = {
#     "Salon-de-Provence": "Salon de Provence",
#     "Pélissanne": "Pélissanne",
#     "Lançon-Provence": "Lançon-Provence",
#     "Grans": "Grans",
#     "Eyguières": "Eyguières",
#     "PELISSANNE": "Pélissanne",
#     "Lançon-En-Provence": "Lançon-Provence",
#     "Aurons": "Aurons",
#     "Pelissanne": "Pélissanne",
#     "La Barben": "La Barben",
#     "Lançon": "Lançon-Provence",
#     "Salon de Provence": "Salon de Provence"
# }
# ```

# # References
# 
# ## UDACITY
# 
# 4. Data Wrangling With MongoDB
# 
# LESSON 5 DATA QUALITY
# 
# 8. Example Using our Blueprint
# 
# https://classroom.udacity.com/nanodegrees/nd002-airbus/parts/35305c70-58f5-4614-b7d6-302fa3f916a3/modules/2166796a-7560-4387-ac5e-c6a4b8d2d61c/lessons/699689362/concepts/7796785460923
# 
# 
# 
# LESSON 13 CASE STUDY
# 
# 3. Iterative Parsing
# 
# https://classroom.udacity.com/nanodegrees/nd002-airbus/parts/35305c70-58f5-4614-b7d6-302fa3f916a3/modules/2166796a-7560-4387-ac5e-c6a4b8d2d61c/lessons/5436095827/concepts/54475500150923
# 
# 
# 
# 10. Improving street name
# 
# 
# https://classroom.udacity.com/nanodegrees/nd002-airbus/parts/35305c70-58f5-4614-b7d6-302fa3f916a3/modules/2166796a-7560-4387-ac5e-c6a4b8d2d61c/lessons/5436095827/concepts/54446302850923
# 
# 
# 
# 
# Python 2 => Python 3
# 
# https://intellipaat.com/community/12207/error-dict-object-has-no-attribute-iteritems
# 
# 
# 
# 
# 
# https://stackoverflow.com/questions/19877306/nameerror-global-name-unicode-is-not-defined-in-python-3
# 
# 
# 
# Schema importation into jupyter notebook
# 
# https://knowledge.udacity.com/questions/263986
# 
# 
# B problem
# 
# https://knowledge.udacity.com/questions/332545
# 
# 
# 
# ## NOTA
# 
# As a python beginner, I put details I discovered learning on the documentation, tutorials, projects and trials in order to refer to my own work afterwards.

# In[4]:


#No need to install it each time
#pip install cerberus


# 

# In[8]:


#Final !
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
To do so you will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in the correct format
- Write each data structure to the appropriate .csv files

We've already provided the code needed to load the data, perform iterative parsing and write the
output to csv files. Your task is to complete the shape_element function that will transform each
element into the correct format. To make this process easier we've already defined a schema (see
the schema.py file in the last code tab) for the .csv files and the eventual tables. Using the 
cerberus library we can validate the output against this schema to ensure it is correct.

## Shape Element Function
The function should take as input an iterparse Element object and return a dictionary.

### If the element top level tag is "node":
The dictionary returned should have the format {"node": .., "node_tags": ...}

The "node" field should hold a dictionary of the following top level node attributes:
- id
- user
- uid
- version
- lat
- lon
- timestamp
- changeset
All other attributes can be ignored

The "node_tags" field should hold a list of dictionaries, one per secondary tag. Secondary tags are
child tags of node which have the tag name/type: "tag". Each dictionary should have the following
fields from the secondary tag attributes:
- id: the top level node id attribute value
- key: the full tag "k" attribute value if no colon is present or the characters after the colon if one is.
- value: the tag "v" attribute value
- type: either the characters before the colon in the tag "k" value or "regular" if a colon
        is not present.

Additionally,

- if the tag "k" value contains problematic characters, the tag should be ignored
- if the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
  and characters after the ":" should be set as the tag key
- if there are additional ":" in the "k" value they and they should be ignored and kept as part of
  the tag key. For example:

  <tag k="addr:street:name" v="Lincoln"/>
  should be turned into
  {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}

- If a node has no secondary tags then the "node_tags" field should just contain an empty list.

The final return value for a "node" element should look something like:

{'node': {'id': 757860928,
          'user': 'uboot',
          'uid': 26299,
       'version': '2',
          'lat': 41.9747374,
          'lon': -87.6920102,
          'timestamp': '2010-07-22T16:16:51Z',
      'changeset': 5288876},
 'node_tags': [{'id': 757860928,
                'key': 'amenity',
                'value': 'fast_food',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'cuisine',
                'value': 'sausage',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'name',
                'value': "Shelly's Tasty Freeze",
                'type': 'regular'}]}

### If the element top level tag is "way":
The dictionary should have the format {"way": ..., "way_tags": ..., "way_nodes": ...}

The "way" field should hold a dictionary of the following top level way attributes:
- id
-  user
- uid
- version
- timestamp
- changeset

All other attributes can be ignored

The "way_tags" field should again hold a list of dictionaries, following the exact same rules as
for "node_tags".

Additionally, the dictionary should have a field "way_nodes". "way_nodes" should hold a list of
dictionaries, one for each nd child tag.  Each dictionary should have the fields:
- id: the top level element (way) id
- node_id: the ref attribute value of the nd tag
- position: the index starting at 0 of the nd tag i.e. what order the nd tag appears within
            the way element

The final return value for a "way" element should look something like:

{'way': {'id': 209809850,
         'user': 'chicago-buildings',
         'uid': 674454,
         'version': '1',
         'timestamp': '2013-03-13T15:58:04Z',
         'changeset': 15353317},
 'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
               {'id': 209809850, 'node_id': 2199822390, 'position': 1},
               {'id': 209809850, 'node_id': 2199822392, 'position': 2},
               {'id': 209809850, 'node_id': 2199822369, 'position': 3},
               {'id': 209809850, 'node_id': 2199822370, 'position': 4},
               {'id': 209809850, 'node_id': 2199822284, 'position': 5},
               {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
 'way_tags': [{'id': 209809850,
               'key': 'housenumber',
               'type': 'addr',
               'value': '1412'},
              {'id': 209809850,
               'key': 'street',
               'type': 'addr',
               'value': 'West Lexington St.'},
              {'id': 209809850,
               'key': 'street:name',
               'type': 'addr',
               'value': 'Lexington'},
              {'id': '209809850',
               'key': 'street:prefix',
               'type': 'addr',
               'value': 'West'},
              {'id': 209809850,
               'key': 'street:type',
               'type': 'addr',
               'value': 'Street'},
              {'id': 209809850,
               'key': 'building',
               'type': 'regular',
               'value': 'yes'},
              {'id': 209809850,
               'key': 'levels',
               'type': 'building',
               'value': '1'},
              {'id': 209809850,
               'key': 'building_id',
               'type': 'chicago',
               'value': '366409'}]}
"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import my_schema

OSM_PATH = 'data/map.osm'

NODES_PATH = "csv/nodes.csv"
NODE_TAGS_PATH = "csv/nodes_tags.csv"
WAYS_PATH = "csv/ways.csv"
WAY_NODES_PATH = "csv/ways_nodes.csv"
WAY_TAGS_PATH = "csv/ways_tags.csv"

mapping = {
    "Salon-de-Provence": "Salon de Provence",
    "Pélissanne": "Pélissanne",
    "Lançon-Provence": "Lançon-Provence",
    "Grans": "Grans",
    "Eyguières": "Eyguières",
    "PELISSANNE": "Pélissanne",
    "Lançon-En-Provence": "Lançon-Provence",
    "Aurons": "Aurons",
    "Pelissanne": "Pélissanne",
    "La Barben": "La Barben",
    "Lançon": "Lançon-Provence",
    "Salon de Provence": "Salon de Provence"
}

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = my_schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element):
    """Clean and shape node or way XML element to Python dict"""

    #Dict
    node_attribs = {}
    way_attribs = {}

    #List
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    
    # YOUR CODE HERE
    """Function main explanation.
    
    """  
    
    if element.tag == 'node':     

        #NODE
        node_attribs['id'] = element.get('id')
        node_attribs['lat'] = element.get('lat')
        node_attribs['lon'] = element.get('lon')
        node_attribs['user'] = element.get('user')
        node_attribs['uid'] = element.get('uid')
        node_attribs['version'] = element.get('version')
        node_attribs['changeset'] = element.get('changeset')
        node_attribs['timestamp'] = element.get('timestamp')
        #print("elementNode : ",node_attribs)
        #print("elementNode : ",node_attribs['id'])
        
        #TAGS of NODE
        for subElement in element:
            #print ("- subElement => ", subElement.get('k'))
            #Create a empty dictionary for the tag
            tag_dict = {}
            #We only want tag tags, /!\ everything is tag in XML but this one is named tag !
            if (subElement.tag == 'tag'):
                #print ("- subElement <tag => ", subElement.get('k'))
                #Get ':' place in the Key name
                
                if PROBLEMCHARS.search(subElement.get('k')):
                    print("problem raised : ", subElement.get('k'))
                    continue
                else:                
                    separator = subElement.get('k').find(':')
                    #print ("- find ':' =>", separator)
                    tag_dict['id'] = element.get('id')
                    
                    
                    if subElement.get('k') == 'addr:city':
                        #print ("corriger ", subElement.get('v'))
                        #print ("corrigé ", mapping[subElement.get('v')])
                        tag_dict['value'] = mapping[subElement.get('v')]
                    else:
                        tag_dict['value'] = subElement.get('v')
                    
                    if (separator != -1):
                        type_value = subElement.get('k')[:separator]
                        key_value = subElement.get('k')[separator+1:]
                        tag_dict['key'] = key_value
                        tag_dict['type'] = type_value
                    else:
                        tag_dict['key'] = subElement.get('k')
                        tag_dict['type'] = 'regular'
                    #print("-- Tag of NODE :",tag_dict)
                    #add the tag dictionary to tags list with id node to make the joint later.
                    tags.append(tag_dict)
        #return in the requested format
        # 6 !
        return {'node': node_attribs, 'node_tags': tags}
    
    
 
    elif element.tag == 'way':
        
        #WAY
        way_attribs['id'] = element.get('id')
        way_attribs['user'] = element.get('user')
        way_attribs['uid'] = element.get('uid')
        way_attribs['version'] = element.get('version')
        way_attribs['changeset'] = element.get('changeset')
        way_attribs['timestamp'] = element.get('timestamp')        
        #print("elementWay : ",way_attribs)
        #print("elementWay : ",way_attribs['id'])
               
        
        #NODEs of WAY
        position = 0
        for subElement in element:
            if subElement.tag == 'nd':
                nd_dict = {}
                #ID of WAY
                nd_dict['id'] = element.get('id')
                #ID of ways linked to the current WAY
                nd_dict['node_id'] = subElement.get('ref')
                nd_dict['position'] = position
                position += 1
                #print("- Node way : ",nd_dict)
                way_nodes.append(nd_dict)
        #return in the requested format
        
                
        
        #TAGS of WAY
        for subElement in element:
            #Create a empty dictionary for the tag
            tag_dict = {}
            #We only want tag tags, /!\ everything is tag in XML but this one is named tag !
            if (subElement.tag == 'tag'):
                #print ("- subElement <tag => ", subElement.get('k'))
                #Get ':' place in the Key name
                separator = subElement.get('k').find(':')
                #print ("- find ':' =>", separator)
                
                if PROBLEMCHARS.search(subElement.get('k')):
                    print("problem raised : ", subElement.get('k'))
                    continue
                else:             
                    tag_dict['id'] = element.get('id')
                    #print ("- subElement <tag => ", subElement.get('k'))
                    tag_dict['value'] = subElement.get('v')

                    if (separator != -1):
                        type_value = subElement.get('k')[:separator]
                        key_value = subElement.get('k')[separator+1:]
                        tag_dict['key'] = key_value
                        tag_dict['type'] = type_value
                    else:
                        tag_dict['key'] = subElement.get('k')
                        tag_dict['type'] = 'regular'
                    #print("-- Tag of WAY :",tag_dict)
                    #add the tag dictionary to tags list with id way to make the joint later.
                    tags.append(tag_dict)
        #return in the requested format
        # 7 !    
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}





# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: v for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""
    # 2
    with codecs.open(NODES_PATH, 'w', "utf-8") as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w', "utf-8") as nodes_tags_file,          codecs.open(WAYS_PATH, 'w', "utf-8") as ways_file,          codecs.open(WAY_NODES_PATH, 'w', "utf-8") as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w', "utf-8") as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            # 4
            el = shape_element(element)
            #print(el)
            if el:
                # 5 bis
                if validate is True:
                    validate_element(el, validator)
                
                # 5
                if element.tag == 'node':
                    #print(el['node'])
                    # 6
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    #print(el['way'])
                    # 7
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':

    # 1
    process_map(OSM_PATH, validate=True)


# ***Pretty big chunk of code***
# 
