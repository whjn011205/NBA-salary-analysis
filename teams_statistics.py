import urllib2
import re
import os
import time
import bs4 as bs
import pandas as pd


#workspace="D://IS5126//Guided//Webpages//"
#url = 'http://www.basketball-reference.com/'


#path_csv = workspace+'Teams//csv//'
csv_team = open('team.csv','w')

#path = workspace+'Teams//'
files=os.listdir('./')

start=time.time()
header_written=False
for eachFile in files:
	print(eachFile)

	#log.write(eachFile+'\n')
	if '.htm' not in eachFile:
		continue

	#print(eachFile)
	teamID=eachFile.strip('.html')
	f=open(path+eachFile,'r')
	sauce=f.read().decode('gbk','ignore').replace('!--', '').replace(u'\xa0', u'').encode('utf-8')
	soup= bs.BeautifulSoup(sauce, 'html')#,from_encoding='gbk')
	f.close()

	if header_written==False:
		csv_team.write('TeamName,')
		div = soup.find('div',{"id:info"})
		print div


		
		team_head = soup.find('table').find('thead').find_all('th')
		for head in team_head:
			#print head.get_text()
			csv_team.write(head.get_text()+',')
		csv_team.write('\n')
		header_written=True
		
	team_body = soup.find('table').find('tbody').find_all('tr')
	for this_row in team_body:
		try:
			season=this_row.find('th').get_text()
		except Exception as e:
			print e
			continue
		csv_team.write(teamID+','+season+',')
		
		other_cells = this_row.find_all('td')
		for item in other_cells:
			try:
				item=item.get_text().replace(',','')
				csv_team.write(item+',')
			except:
				item=item.encode('gbk','ignore')
				csv_team.write(item+',')
			
		csv_team.write('\n')
csv_team.close()