import urllib2
import re
import os
import time
import bs4 as bs
import pandas as pd

"""
This code is for Part I (3), to extract player info
"""

# Workspace is used to store the html files
workspace="D://IS5126//Guided//Webpages//"
url = 'http://www.basketball-reference.com/'
#df=pd.DataFrame()


# headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}
# request=urllib2.Request(url, headers=headers)
# sauce=urllib2.urlopen(request).read()
# time.sleep(1)
# print sauce


path_csv = workspace + 'Players//csv//'
csv_per_game = open(path_csv+'per_game.csv','w')
csv_advanced = open(path_csv+'advanced.csv','w')
csv_shooting = open(path_csv+'shooting.csv','w')

log_name = path_csv+'log.txt'
log = open(log_name,'w')


start=time.time()
path = workspace+'Players//'
files=os.listdir(path)
i=0
for eachFile in files:
	
	print(eachFile)

	log.write(eachFile+'\n')
	if '.html' not in eachFile:
		continue

	i+=1
	playerID=eachFile.strip('.html')
	f=open(path+eachFile,'r')	
	sauce=f.read().decode('gbk','ignore').replace('!--', '').replace(u'\xa0', u'').encode('utf-8')
	soup= bs.BeautifulSoup(sauce, 'html')#,from_encoding='gbk')
	f.close()

	#------------------ per game table ------------------------
	# filename=path_csv+playerID+'_per_game.csv'
	# f = open(filename,'w')

	if i<=1:

		print 'whritng header'
		csv_per_game.write('PlayerID,')
		per_game_head = soup.find('table', {"id":"per_game"}).find('thead').find_all('th')
		for head in per_game_head:
			csv_per_game.write(head.get_text()+',')
		csv_per_game.write('\n')
	

	per_game_body = soup.find('table', {"id":"per_game"}).find('tbody').find_all('tr')
	for this_row in per_game_body:
		try:
			season=this_row.find('th').get_text()
		except Exception as e:
			print e
			log.write(str(e) +' # per_game/body\n')
			continue
		csv_per_game.write(playerID+','+season+',')
		
		other_cells = this_row.find_all('td')
		for item in other_cells:
			csv_per_game.write(item.get_text()+',')
		csv_per_game.write('\n')
	#f.close()


	#------------------ advanced table ------------------------
	# filename=path_csv+playerID+'_advanced.csv'
	# f = open(filename,'w')
	if i<=1:
		csv_advanced.write('PlayerID,')
		advanced_head = soup.find('table', {"id":"advanced"}).find('thead').find_all('th')
		for head in advanced_head:
			try:
				head=head.get_text()#.encode('gbk','ignore')
				csv_advanced.write(head+',')
			except Exception as e:
				csv_advanced.write(',')
				log.write( str(e) +' # advanced/header\n')
				continue
		csv_advanced.write('\n')
		
	advanced_body = soup.find('table', {"id":"advanced"}).find('tbody').find_all('tr')
	for this_row in advanced_body:
		try:
			season=this_row.find('th').get_text()
		except Exception as e:
			log.write(str(e) +' # advanced/body\n')
			continue
		csv_advanced.write(playerID+','+season+',')
		
		other_cells = this_row.find_all('td')
		for item in other_cells:
			#item = item.get_text()
			# if len(item) ==0:
			# 	continue
			csv_advanced.write(item.get_text()+',')
		csv_advanced.write('\n')
	#f.close()



	# -----------------------------  shooting table ---------------------------------------
	# only extract the last eight colums from shooting table
	# filename=path_csv+playerID+'_shooting.csv'
	# f = open(filename,'w')
	if i<=1:
		csv_shooting.write('PlayerID,')
		shooting_head = soup.find("table", {"id":"shooting"}).find('thead').find_all('th')
		for head in shooting_head:
			head=head.get_text()
			if len(head)>10 or len(head)==0:
				continue
			if head in ['Dunks', 'Corner', 'Heaves']:
			 	continue
			#print head
			csv_shooting.write(head+',')
		csv_shooting.write('\n')

	shooting_body = soup.find('table', {"id":"shooting"}).find('tbody').find_all('tr')
	for this_row in shooting_body:
		try:
			season=this_row.find('th').get_text()
		except Exception as e:
			log.write(str(e) +' # shooting/body\n')
			continue

		csv_shooting.write(playerID+','+season+',')
		
		other_cells = this_row.find_all('td')
		for item in other_cells:
			csv_shooting.write(item.get_text()+',')
		csv_shooting.write('\n')
	#f.close()

end=time.time()
print(end-start)
log.close()
csv_per_game.close()
csv_advanced.close()
csv_shooting.close()



