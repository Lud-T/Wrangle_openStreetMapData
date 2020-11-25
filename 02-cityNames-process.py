#!/usr/bin/env python
# coding: utf-8

# # Third submission
# 
# 
# ## Scripts cannot be run from the command prompt/terminal
# 
# There are some function calls that come from Jupyter notebook in your Python scripts i.e. the lines that begin with get_ipython(). They produce errors when running the python scripts e.g. python 02-cityNames-process.py. Make sure your code can be run to correct the elements from the command prompt to pass this specification.
# 
# 
# 
# 
# ***As I was not sure about what I was doing to measure the performances so, as it is not the purpose of this exercice, I delete these portion of code, and now the code works using command prompt.***

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

# In[ ]:




