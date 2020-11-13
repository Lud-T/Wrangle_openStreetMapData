#!/usr/bin/env python
# coding: utf-8

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
# ## NOTA
# 
# As a python beginner, I put details I discovered learning on the documentation, tutorials, projects and trials in order to refer to my own work afterwards.

# ### First  tags analysis 
# 
# Although we have a description of the data into the OSM wiki.
# 
# To understand parsing and the data, I feel the need to analyse the different level of tags.

# In[1]:


#
#Basic code I'll use to go trhu the XML and count.
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
from pprint import pprint
import operator

#osm_file = 'data/small_sample_map.osm'
osm_file = 'data/map.osm'

def count_tags(filename):
    #count is a dictionary, dictionary manage pairs
    count = {}
    #Loop all the element in the file at first level !
    #All element are tags
    for _, element in ET.iterparse(filename):
        tag = element.tag
        #print(tag)
        #tag variable <= tag name
        #If tag name is not present in the count dict
        #add tag name in the dict with value 1
        if tag not in count.keys():
            count[tag] = 1
        #If tag name is already existing in the count dict
        #add 1  to the value of the already existing tag name
        else:
            count[tag] += 1

    return count



def main():
    #call function and return a dictionary
    count = count_tags(osm_file)
    #Sort dictionary
    count = sorted(count.items(), key=operator.itemgetter(1))[::1]
    #Display dictionary !
    pprint(count)

    
if __name__ == "__main__":
    main()


# **The tags are the same as described in OSM wiki datamodel**
# 

# ### Keys analysis 
# 
# Now, I check the keys and count them.
# 
# My goal will be to look for relevant keys and check if it is easy to find errors.

# In[2]:


#
#Basic code I'll use to go trhu the XML and count.
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
from pprint import pprint
import operator

#osm_file = 'data/small_sample_map.osm'
osm_file = 'data/map.osm'

def count_tags(filename):
    #count is a dictionary, dictionary manage pairs
    count = {}
    #Loop all the element in the file at first level !
    #All element are tags
    for _, element in ET.iterparse(filename):
        #print(element.tag)
        tagK = element.get('k')
        #tagK variable <= Key name
        #If there is a k value count it
        if tagK:
            #If Key name is not present in the count dict
            #add Key name in the dict with value 1
            if tagK not in count.keys():
                count[tagK] = 1
            #If Key name  is already existing in the count dict
            #add 1  to the value of the already existing Key name 
            else:
                count[tagK] += 1

    return count



def main():
    #call function and return a dictionary
    count = count_tags(osm_file)
    #Sort dictionary
    count = sorted(count.items(), key=operator.itemgetter(1))[::-1]
    #Display dictionary !
    pprint(count)

    
if __name__ == "__main__":
    main()


# ***What I will check according to result***
#  
#  City names occurences and post code seems easy to check because I choose an area with less than a dozen of towns I know very well
#  
#  ('addr:city', 137),
#  ('addr:postcode', 136),
# 

# ### Postcode analysis 
# 
# Now, I check the keys postcode value and count them.
# 
# My goal will be to look for wrong value

# In[3]:


#
#Basic code I'll use to go trhu the XML and count.
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
from pprint import pprint
import operator

#osm_file = 'data/small_sample_map.osm'
osm_file = 'data/map.osm'

def count_tags(filename):
    #count is a dictionary, dictionary manage pairs
    count = {}
    #Loop all the element in the file at first level !
    #All element are tags
    for _, element in ET.iterparse(filename):
        #print(element.tag)
        tagK = element.get('k')
        #tagK variable <= Key name
        #If there is a k value check it
        if tagK == 'addr:postcode':
            #if if it is the right one get the value
            tagV = element.get('v')
            #If value is not present in the count dict
            #add value in the dict with value 1
            if tagV not in count.keys():
                count[tagV] = 1
            #If value is already existing in the count dict
            #add 1  to the count of the already existing tag name
            else:
                count[tagV] += 1

    return count



def main():
    #call function and return a dictionary
    count = count_tags(osm_file)
    #Sort dictionary
    count = sorted(count.items(), key=operator.itemgetter(1))[::-1]
    #Display dictionary !
    pprint(count)

    
if __name__ == "__main__":
    main()


# ***Postcodes have the expected format***

# ## citynames analysis
# 
# Now, I check the keys citynames value and count them.
# 
# My goal will be to look for wrong value
# 

# In[4]:


#
#Basic code I'll use to go trhu the XML and count.
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
from pprint import pprint
import operator

#osm_file = 'data/small_sample_map.osm'
osm_file = 'data/map.osm'

def count_tags(filename):
    #count is a dictionary, dictionary manage pairs
    count = {}
    #Loop all the element in the file at first level !
    #All element are tags
    for _, element in ET.iterparse(filename):
        #print(element.tag)
        tagK = element.get('k')
        #tagK variable <= Key name
        #If there is a k value count it
        if tagK == 'addr:city':
            tagV = element.get('v')
            #If Key name is not present in the count dict
            #add Key name in the dict with value 1
            if tagV not in count.keys():
                count[tagV] = 1
            #If tag name is already existing in the count dict
            #add 1  to the value of the already existing tag name
            else:
                count[tagV] += 1

    return count



def main():
    #call function and return a dictionary
    count = count_tags(osm_file)
    #Sort dictionary
    count = sorted(count.items(), key=operator.itemgetter(1))[::-1]
    #Display dictionary !
    pprint(count)

    
if __name__ == "__main__":
    main()


# ***Some city names are not written in the same way***
# 
# 
# I'll have to take care of them when I transpose the data into a database
# 
# I'll make this work in another file.

# ## Road name analysis
# 
# More complicated, I'll analyze road names

# In[5]:


#
#Basic code I'll use to go trhu the XML and count.
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import operator
from pprint import pprint

osm_file = 'data/small_sample_map.osm'
#osm_file = 'data/map.osm'

decoupe = re.compile(r'\W+')

def audit():
    typeOfWays = {}
    for _, element in ET.iterparse(osm_file):
        #As we want only name of road, I check for name tag in way containing tag highway
        for way in element.iter('way'):
            for tag in way.iter('tag'):
                if tag.attrib['k'] == "highway":
                    for tag in way.iter('tag'):
                        if tag.attrib['k'] == "name":
                            streetName = tag.attrib['v']
                            #print(streetName)
                            #According to regular expression I want only the first word of the full street name
                            typeOfStreetName = decoupe.split(streetName)[0]
                            #I count the type !
                            if (typeOfStreetName) not in typeOfWays.keys():
                                   typeOfWays[typeOfStreetName] = 1
                            else:
                                    #print(elem.tag)
                                    typeOfWays[typeOfStreetName] += 1
    return typeOfWays



def main():
    typeOfWays = audit()
    typeOfWays = sorted(typeOfWays.items(), key=operator.itemgetter(1))[::-1]
    pprint(typeOfWays)

    
if __name__ == "__main__":
    main()


# ***No problem on ways type***
# 

# ## For test purpose only, to be deleted

# In[ ]:


# !/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
from pprint import pprint
import operator

osm_file = 'data/small_sample_map.osm'
#osm_file = 'data/map.osm'

def count_tags(filename):
    count = {}
    #Loop all the element in the file at first level !
    for _, elem1 in ET.iterparse(filename):
        print(elem1.tag,"->",elem1.keys() )
        #Loop all the elements into the first level tag !
        for subtag in elem1:
            print ("-",subtag.tag , "->", subtag.keys())
            for subsubtag in subtag:
               print ("--",subsubtag.tag , "->", subsubtag.keys())
                 
                
    return count



def main():
    count = count_tags(osm_file)
    count = sorted(count.items(), key=operator.itemgetter(1))[::-1]
    pprint(count)

    
if __name__ == "__main__":
    main()


# In[ ]:




