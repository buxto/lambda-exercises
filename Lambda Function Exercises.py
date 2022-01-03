#!/usr/bin/env python
# coding: utf-8

# In[96]:


# import necessary tools
import csv
from functools import reduce
import json


# In[62]:


# store in disparate lists for joining later - helps to know headers
fields = []
rows = []


# In[63]:


# open up file, read in, close out
csvfile = open('911_Calls_for_Service_(Last_30_Days).csv', 'r')
reader = csv.reader(csvfile)
fields = next(reader)
for row in reader:
    rows.append(row)
csvfile.close()


# In[64]:


data_dict = []
# zip together to form dictionaries
for row in rows:
    data_dict.append(dict(zip(fields, row)))
    
print(len(data_dict))


# In[65]:


# filter out bad entries
data_dict_filtered = list(filter(lambda x: x['zip_code'] != '0' and x['neighborhood'] != '' and x['totalresponsetime'] != '' and x['dispatchtime'] != '' and x['totaltime'] != '', data_dict))
print(len(data_dict_filtered))


# In[84]:


trt = []
dt = []
tt = []
# pull out the appropriate info
for item in data_dict_filtered:
    trt.append(float(item['totalresponsetime']))
    dt.append(float(item['dispatchtime']))
    tt.append(float(item['totaltime']))
    
avg_trt = reduce(lambda x, y: x + y, trt)/len(trt)

avg_dt = reduce(lambda x, y: x + y, dt)/len(dt)

avg_tt = reduce(lambda x, y: x + y, tt)/len(tt)
print('Average TRT: ' + str(avg_trt))
print('Average DT: ' + str(avg_dt))
print('Average TT: ' + str(avg_tt))


# In[70]:


# gonna have a dictionary of lists of dictionaries, lovely
neighborhood_dict = {}
# get all unique neighborhoods
for item in data_dict_filtered:
    if item['neighborhood'] not in neighborhood_dict:
        neighborhood_dict.update({item['neighborhood']: None})
# print(neighborhood_dict)


# In[78]:


# wtf
# damn it works
for ngbh in neighborhood_dict.keys():
    neighborhood_dict[ngbh] = list(filter(lambda x: x['neighborhood'] == ngbh, data_dict_filtered))


# In[85]:


# now that we got em all in, let's do some reduction
police_final_data = []
for ngbh in neighborhood_dict.keys():
    temp_dict = {}
    temp_dict.update({'Location' : ngbh})
    trt = []
    dt = []
    tt = []
    for item in neighborhood_dict[ngbh]:
        trt.append(float(item['totalresponsetime']))
        dt.append(float(item['dispatchtime']))
        tt.append(float(item['totaltime']))
    
    temp_trt = reduce(lambda x, y: x + y, trt)/len(trt)
    temp_dict.update({'Average TRT' : temp_trt})
    temp_dt = reduce(lambda x, y: x + y, dt)/len(dt)
    temp_dict.update({'Average DT' : temp_dt})
    temp_tt = reduce(lambda x, y: x + y, tt)/len(tt)
    temp_dict.update({'Average TT' : temp_tt})
    police_final_data.append(temp_dict)
                  
# we now have neighborhood average measures


# In[88]:


# Get overall average measures as well
temp_dict = {}
temp_dict.update({'Location' : 'Overall'})

trt = []
dt = []
tt = []
# pull out the appropriate info
for item in data_dict_filtered:
    trt.append(float(item['totalresponsetime']))
    dt.append(float(item['dispatchtime']))
    tt.append(float(item['totaltime']))
    
avg_trt = reduce(lambda x, y: x + y, trt)/len(trt)
temp_dict.update({'Average TRT' : avg_trt})
avg_dt = reduce(lambda x, y: x + y, dt)/len(dt)
temp_dict.update({'Average DT' : avg_dt})
avg_tt = reduce(lambda x, y: x + y, tt)/len(tt)
temp_dict.update({'Average TT' : avg_tt})
police_final_data.append(temp_dict)


# In[97]:


# output to JSON
f = open('lambda_fun_ex_test.JSON', 'a')
f.write(json.dumps(police_final_data))
f.close()

