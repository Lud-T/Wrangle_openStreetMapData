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
# 10. Improving street name
# 
# 
# https://classroom.udacity.com/nanodegrees/nd002-airbus/parts/35305c70-58f5-4614-b7d6-302fa3f916a3/modules/2166796a-7560-4387-ac5e-c6a4b8d2d61c/lessons/5436095827/concepts/54446302850923
# 
# 
# Performance check try.
# 
# https://jakevdp.github.io/PythonDataScienceHandbook/01.07-timing-and-profiling.html
# 
# 
# ## NOTA
# 
# As a python beginner, I put details I discovered learning on the documentation, tutorials, projects and trials in order to refer to my own work afterwards.

# ## citynames improvement !
# 
# I have checked the different occurences of city name :  
# Here is the list 
# 
# ```python
# [('Salon-de-Provence', 64),
#  ('Pélissanne', 46),
#  ('Lançon-Provence', 14),
#  ('Grans', 2),
#  ('Eyguières', 2),
#  ('PELISSANNE', 2),
#  ('Lançon-En-Provence', 2),
#  ('Aurons', 1),
#  ('Pelissanne', 1),
#  ('La Barben', 1),
#  ('Lançon', 1),
#  ('Salon de Provence', 1)]
#  ```
#  
#  
#  What I will do now is creating a dictionary and put the right city name for each of these occurences.

# In[200]:


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



def checkNupdate(filename):
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
            #print(mapping[tagV])
            #If Key name is not present in the count dict
            #add Key name in the dict with value 1
            if mapping[tagV] not in count.keys():
                count[mapping[tagV]] = 1
            #If tag name is already existing in the count dict
            #add 1  to the value of the already existing tag name
            else:
                count[mapping[tagV]] += 1

    return count



def main():
    #call function and return a dictionary
    count = checkNupdate(osm_file)
    #Sort dictionary
    count = sorted(count.items(), key=operator.itemgetter(1))[::-1]
    #Display dictionary !
    pprint(count)

    
if __name__ == "__main__":
    main()


# ***Nice !!!***
# 
# 
# Thanks to dictionnaries we replace wrong name by good one.

# Let's check if I have better results checking only errors !
# I try the same code with %%timeit

# In[201]:


get_ipython().run_cell_magic('timeit', '', '#\n#Basic code I\'ll use to go trhu the XML and count.\n#\n#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport xml.etree.ElementTree as ET\nimport re\nfrom pprint import pprint\nimport operator\n\n\n#osm_file = \'data/small_sample_map.osm\'\nosm_file = \'data/map.osm\'\n\n\nmapping = {\n    "Salon-de-Provence": "Salon de Provence",\n    "Pélissanne": "Pélissanne",\n    "Lançon-Provence": "Lançon-Provence",\n    "Grans": "Grans",\n    "Eyguières": "Eyguières",\n    "PELISSANNE": "Pélissanne",\n    "Lançon-En-Provence": "Lançon-Provence",\n    "Aurons": "Aurons",\n    "Pelissanne": "Pélissanne",\n    "La Barben": "La Barben",\n    "Lançon": "Lançon-Provence",\n    "Salon de Provence": "Salon de Provence"\n}\n\n\n\ndef checkNupdate(filename):\n    #count is a dictionary, dictionary manage pairs\n    count = {}\n    #Loop all the element in the file at first level !\n    #All element are tags\n    for _, element in ET.iterparse(filename):\n        #print(element.tag)\n        tagK = element.get(\'k\')\n        #tagK variable <= Key name\n        #If there is a k value count it\n        if tagK == \'addr:city\':\n            tagV = element.get(\'v\')\n            if tagV in mapping:\n                tagV=mapping[tagV]\n            #print(mapping[tagV])\n            #If Key name is not present in the count dict\n            #add Key name in the dict with value 1\n            if tagV not in count.keys():\n                count[tagV] = 1\n            #If tag name is already existing in the count dict\n            #add 1  to the value of the already existing tag name\n            else:\n                count[tagV] += 1\n\n    return count\n\n\n\ndef main():\n    #call function and return a dictionary\n    count = checkNupdate(osm_file)\n    #Sort dictionary\n    count = sorted(count.items(), key=operator.itemgetter(1))[::-1]\n    #Display dictionary !\n    pprint(count)\n\n    \nif __name__ == "__main__":\n    main()')


# In[202]:


get_ipython().run_cell_magic('timeit', '', '#\n#Basic code I\'ll use to go trhu the XML and count.\n#\n#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport xml.etree.ElementTree as ET\nimport re\nfrom pprint import pprint\nimport operator\n\n\n#osm_file = \'data/small_sample_map.osm\'\nosm_file = \'data/map.osm\'\n\n\nmapping = {\n    "Salon-de-Provence": "Salon de Provence",\n#    "Pélissanne": "Pélissanne",\n    "Lançon-Provence": "Lançon-Provence",\n#    "Grans": "Grans",\n    "Eyguières": "Eyguières",\n    "PELISSANNE": "Pélissanne",\n    "Lançon-En-Provence": "Lançon-Provence",\n#    "Aurons": "Aurons",\n    "Pelissanne": "Pélissanne",\n#    "La Barben": "La Barben",\n    "Lançon": "Lançon-Provence",\n#    "Salon de Provence": "Salon de Provence"\n}\n\n\n\ndef checkNupdate(filename):\n    #count is a dictionary, dictionary manage pairs\n    count = {}\n    #Loop all the element in the file at first level !\n    #All element are tags\n    for _, element in ET.iterparse(filename):\n        #print(element.tag)\n        tagK = element.get(\'k\')\n        #tagK variable <= Key name\n        #If there is a k value count it\n        if tagK == \'addr:city\':\n            tagV = element.get(\'v\')\n            if tagV in mapping:\n                tagV=mapping[tagV]\n            #print(mapping[tagV])\n            #If Key name is not present in the count dict\n            #add Key name in the dict with value 1\n            if tagV not in count.keys():\n                count[tagV] = 1\n            #If tag name is already existing in the count dict\n            #add 1  to the value of the already existing tag name\n            else:\n                count[tagV] += 1\n\n    return count\n\n\n\ndef main():\n    #call function and return a dictionary\n    count = checkNupdate(osm_file)\n    #Sort dictionary\n    count = sorted(count.items(), key=operator.itemgetter(1))[::-1]\n    #Display dictionary !\n    pprint(count)\n\n    \nif __name__ == "__main__":\n    main()')


# ***It sound to be not so significant***
# 
# But honestly, I am not sure of what I am doing.

# In[ ]:




