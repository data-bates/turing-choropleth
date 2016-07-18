
# coding: utf-8

# In[2]:

import pandas as pd


# In[3]:

employees_df = pd.read_csv("data/cbp13co.txt", dtype={'fipstate': object, 'fipscty': object})
codes_df = pd.read_csv("data/georef12.txt", dtype={'fipstate': object, 'fipscty': object})
land_area_df = pd.read_csv('data/DEC_00_SF1_GCTPH1.US05PR.csv', dtype={'GCT_STUB.target-geo-id2': object})


# In[106]:

print employees_df


# In[11]:

# want the total over all naics codes (where naics column = '------')
# excluding statewide totals (where county code = 999)
emp_all_df = employees_df[(employees_df['naics'] == '------') & (employees_df['fipscty'] != '999')].copy()
emp_all_df.shape


# In[9]:

# also want the name of the county and state
print codes_df[:5]
with_names_df = pd.merge(emp_all_df, codes_df, on=['fipstate', 'fipscty'], how='inner')


# In[70]:

with_names_df[:5]


# In[71]:

# combine fip codes to be 5 digit code for topojson compatibility
with_names_df['id'] = with_names_df['fipstate'] + with_names_df['fipscty']


# In[72]:

# only need total number of businesses with 50-99 employees
sb_df = with_names_df[['id', 'ctyname', 'n50_99']].copy()


# In[73]:

sb_df[:5]


# In[75]:

# calculate density using county land area


# In[96]:

land_area_df[:5]


# In[97]:

# total land area is column HC04
area_df = land_area_df.rename(columns={'GCT_STUB.target-geo-id2':'id', 'HC06':'area'})[['id', 'area']]


# In[98]:

# left join on fips id, convert to int
sb_area_df = pd.merge(sb_df, area_df, on=['id'], how='left')
sb_area_df['id'] = sb_area_df['id'].apply(int)


# In[99]:

# calculate density
sb_area_df['density'] = sb_area_df['n50_99'] / sb_area_df['area']


# In[100]:

sb_density_df = sb_area_df[['id', 'ctyname', 'density', 'n50_99']]
sb_density_df[:5]


# In[101]:

sb_density_df.to_csv('data/sbdata.csv', index=False)


# In[103]:

sb_density_df['density'].describe()


# In[ ]:



