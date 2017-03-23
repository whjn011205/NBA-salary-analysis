import urllib2
import re
import os
import time
import bs4 as bs
import pandas as pd


#workspace="D://IS5126//Guided//Webpages//"
#url = 'http://www.basketball-reference.com/'


#path_csv = workspace+'Teams//csv//'
f = open('team_profile.csv','w')

#path = workspace+'Teams//'
files=os.listdir('./')

#start=time.time()
header_written=False
for eachFile in files:
	

	#log.write(eachFile+'\n')
	if '.htm' not in eachFile:
		continue
	#print(eachFile)


	#sauce=f.read().decode('gbk','ignore').replace('!--', '').replace(u'\xa0', u'').encode('utf-8')
	html_file=open(eachFile,'r')
	html=html_file.read().replace('!--', '')
	html_file.close()

	soup= bs.BeautifulSoup(html, 'html')#,from_encoding='gbk')
	
	div = soup.find('div',{"id":"meta"}).find_all('div')[1]
	ps=div.find_all('p')
	
	alias=soup.find('table')['id']
	print alias

	headers=['Team',"Alias"]
	vals=[div.find('h1').find('span').get_text(), alias]
	
	for p in ps:
		header, val = p.get_text().replace('\n','').split(':')
		header,val = header.strip(), val.strip()
		vals.append('"'+val+'"')
		#print "---------"
		#print val
		if header_written==False:
			headers.append(header)

	# print headers
	# print vals		 
	
	if header_written==False:
		for header in headers:
			f.write(header+',')
		f.write("\n")
		header_written=True
		print "header written"

	for val in vals:
		f.write(val+',')
	f.write('\n')

		
	# team_body = soup.find('table').find('tbody').find_all('tr')
	# for this_row in team_body:
	# 	try:
	# 		season=this_row.find('th').get_text()
	# 	except Exception as e:
	# 		print e
	# 		continue
	# 	csv_team.write(teamID+','+season+',')
		
	# 	other_cells = this_row.find_all('td')
	# 	for item in other_cells:
	# 		try:
	# 			item=item.get_text().replace(',','')
	# 			csv_team.write(item+',')
	# 		except:
	# 			item=item.encode('gbk','ignore')
	# 			csv_team.write(item+',')
			
	#csv_team.write('\n')
f.close()