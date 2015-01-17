import numpy as np
import pandas as pd
import csv
import bs4




	#lookup table import
df_lookup =pd.read_csv('zipfile.csv', thousands=',')

	#data import
df_data=pd.read_csv('datafile.csv', thousands=',')

df_data=df_data.dropna()
df_lookup=df_lookup.dropna()
df_data.columns=['postal_code','Ad_server_impressions']

	#data cleaning deleting last rows and non zip rows
df_data=df_data[df_data.postal_code.str.len()>3]
df_data=df_data.drop(df_data.tail(1).index)

	#reformatting 4 digit zipcodes to 5 digits with leading zero
df_lookup['zips'] = df_lookup['zips'].apply(lambda x: '{0:0>5}'.format(x))
df_data['postal_code'] = df_data['postal_code'].apply(lambda x: '{0:0>5}'.format(x))
df_lookup['fips'] = df_lookup['fips'].apply(lambda x: '{0:0>5}'.format(x))

	#joining data with lookup table
a=pd.merge(df_data, df_lookup, how='left',left_on = ['postal_code'], right_on =['zips'])
grouped_data=a.groupby('fips')
grouped_data=grouped_data.sum().reset_index(level=1)

	#assigning colors boundary
a0=float(grouped_data.quantile(0.40))
a1=float(grouped_data.quantile(0.50))
a2=float(grouped_data.quantile(0.65))
a3=float(grouped_data.quantile(0.75))
a4=float(grouped_data.quantile(0.85))
a5=float(grouped_data.quantile(0.9))
a6=float(grouped_data.quantile(0.95))

	
tempdict = {}
min_value = 100; max_value = 0
tempdict=dict(zip(grouped_data.fips,grouped_data.Ad_server_impressions))
		
 
 
# Load the SVG map
svg = open('counties.svg', 'r').read()
 
# Load into Beautiful Soup
soup = bs4.BeautifulSoup(svg,'xml')
 
# Find counties
paths = soup.findAll('path')
 
# Map colors
colors = ["#f7fbff","#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6","#2171b5", "#084594"]
 
# County style
path_style = "font-size:12px;fill-rule:nonzero;stroke:#221e1f;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:"

rate=0
# Color the counties based on data agains color boundaries
for p in paths:
	if p['id'] not in ["State_Lines", "separator"]:
		try:
			rate = tempdict[p['id']]
			
		except:
			color="#FFFFFF"
			p['style']=path_style+color
			continue   
		if rate > a6:
			color_class = 7
		elif rate > a5:
			color_class = 6
		elif rate > a4:
			color_class = 5
		elif rate > a3:
			color_class = 4
		elif rate > a2:
			color_class = 3
		elif rate > a1:
			color_class = 2
		elif rate>a0:
			color_class = 1
		else:
			color_class = 0

		color = colors[color_class]
		p['style'] = path_style + color
print soup.prettify()



