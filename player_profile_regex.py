## Copy this file into the folder where you store all players' htmls
## then run

import re
import bs4 as bs
import os
import time

person_initial= {
	"name":'',
	"position":'',
	"shoots":'',
	'height':'',
	'weight':'',
	'dob':'',
	'birth place':'',
	'country':'',
	'college':'',
	"draft_rank":'',
	"draft_year":'',
	"debut":'',
	#"High School":'',
}

person=person_initial
headers=person.keys()

log = open('players_profile_log.txt','w')
f=open('players_profile.csv','w')

## writing table headers into the csv
f.write('PlayerID'+',')
for head in headers:
	f.write(head+',')
f.write('\n')


start = time.time()


files=os.listdir('./')
for eachFile in (files):
	if ".htm" not in eachFile:
			continue

	## reset the player information to empty		
	for key in person.keys():
		person[key]=''

	print eachFile
	log.write(''.join(('-------',eachFile,'------------\n')))


	html_file=open(eachFile,'r')
	html=html_file.read().replace('!--','')
	html_file.close()

	playerID=eachFile.split('.')[0]
	f.write(playerID+',')

	div = re.findall(r'<div.*?itemtype="http.*?/Person(.*?)</div>',html, re.DOTALL)[0]
	person['name'] = '"'+re.findall(r'name">(.*?)</h1',div)[0]+'"'

	ps = re.findall(r'(<p>.*?</p>)',div,re.DOTALL)
	try:
		for p in ps:
			p=p.replace('\n','')
			if "Position" in p:
				person['position']=re.findall(r'Position.*?>(.*?)[<&]',p)[0].strip()

			if "Shoots" in p:
				person['shoots'] = re.findall(r'Shoots:.*?>(.*?)<',p,re.DOTALL)[0].strip()#[0].strip()
				
			if '"weight"' in p and '"height"' in p:
				person['height'], person['weight'] = re.findall(r'\((.*?)cm.*?;(.*?)kg\)',p)[0]
			
			if "Born:" in p:
				person['dob'] = re.findall(r'data-birth="(.*?)">',p)[0]
				person['birth place'] = '"'+re.findall(r'"birthPlace">.*?>(.*?)<',p)[0].strip()+'"'
				person['country'] = re.findall(r'country=(.*?)&',p)[0].strip()
			
			if "College:" in p:
				person['college'] = '"'+re.findall(r'href.*?>(.*?)</a',p)[0].strip()+'"'
				
			if "Draft:" and "/draft/" in p:
				person['draft_rank'], person['draft_year'] = re.findall(r'pick, (.*?)overall.*?>(.*?) NBA',p)[0]
				person['draft_rank'] = person['draft_rank'] [:-3]
				
			if "NBA Debut:" in p:
				y,m,d= re.findall(r'boxscores/(....)(..)(..)',p)[0]
				person['debut'] ="-".join((y,m,d)) 

		for head in headers:
			f.write(person[head]+',')	

	except Exception as e:
		log.write(str(e)+'\n')
		log.write(p+'\n')
		print e
		print p 		
	
	f.write('\n')

end = time.time()
print end-start
f.close()
log.close()















