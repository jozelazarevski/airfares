# -*- coding: cp1251 -*-
import urllib2
from BeautifulSoup import BeautifulSoup


# from = "MOW"
# to = "PAR"
# dep_date = "20130510"
# ret_date = "20130524"
# class = "B"


# page = 'http://sindbad.ru/ru/flight/results/'+from+to+dep_date+ret_date+'100'+class+'0'

page = 'http://sindbad.ru/ru/flight/results/MOWPAR2013051520130528100E0'

urllib_page = urllib2.urlopen(page)
soup_page = BeautifulSoup(urllib_page)


table = soup_page.find('div', {"id":"wrapper", 'class': 'pie'})

# Вытащить даты
# date=[]

# for n in range(0, 2):

#	date.append(table.findAll('div', {'class':'date'})[n].text)

#for n in range(len(date)):
#	date[n]=date[n][:2]

#print date


# Вытащить направления 
# destination=[]

# for n in range(0, 2):

#	destination.append(table.findAll('div', {'class':'city'})[n])

# print destination

# сколько цен
quantity = (len(table('span', {"class" : "lPrice"})))
#print quantity

# количество вариантов в табличке туда

table1 = []

for n in range(0,quantity):

	table1.append(table.findAll('div', {'class': 'variants clf pie fForward'})[n])
		

opt_quants = [] 

for i in range(0,quantity):

	opt_quant = len(table1[i].findAll('div', {"class" : "clf resChain"}))
	opt_quants.append(opt_quant)
	
print "рейсы туда: " + str(opt_quants)


# количество вариантов в табличке обратно

table2 = []

for n in range(0,quantity):

	table2.append(table.findAll('div', {'class': 'variants back clf pie fBack'})[n])
		

opt_quants2 = [] 

for i in range(0,quantity):

	opt_quant2 = len(table2[i].findAll('div', {"class" : "clf resChain"}))
	opt_quants2.append(opt_quant2)
	
print "рейсы обратно: " + str(opt_quants2)



# cколько рейсов с пересадками в табличке туда 

table1 = []

for n in range(0,quantity):

	table1.append(table.findAll('div', {'class': 'variants clf pie fForward'})[n])
		

trans_s1 = [] 

for i in range(0,quantity):

	trans1 = len(table1[i].findAll('div', {"class" : "trans"}))
	trans_s1.append(trans1)
	
print "пересадки туда: " + str(trans_s1)


# cколько рейсов с пересадками в табличке обратно

table2 = []

for n in range(0,quantity):

	table2.append(table.findAll('div', {'class': 'variants back clf pie fBack'})[n])
		

trans_s2 = [] 

for i in range(0,quantity):

	trans2 = len(table2[i].findAll('div', {"class" : "trans"}))
	trans_s2.append(trans2)
	
print "пересадки обратно: " + str(trans_s2)


# количество авиакомпаний в каждой табличке

table3 = []

for n in range(0,quantity):

	table3.append(table.findAll('div', {'class': 'carriers-logos'})[n])
		

comp = [] 

for i in range(0,quantity):

	alliance = len(table3[i].findAll('a', {'class' : 'company-logo'}))
	comp.append(alliance)
	
print "кол-во авиакомпаний: " + str(comp)

 

# Вытащить цены билетов

price=[]

for n in range(0, quantity):

	price.append(table.findAll('span', {"class" : "lPrice"})[n].text)

for n in range(len(price)):

	price[n]=price[n][:6]

# print price

# Вытащить время вылета, время прилёта, длительность полёта

q = (len(table('div', {"class" : "col"})))

#print q 

time=[]

for n in range(0, q):

	time.append(table.findAll('div', {'class':'col'})[n].text)
	
print u" ".join(time)	


# название авиакомпании

qua = (len(table('a', {"class" : "company-logo"})))
# print qua

company=[]

for n in range(0, qua):

	company.append(table.findAll('a', {'class':'company-logo'})[n])

print company







