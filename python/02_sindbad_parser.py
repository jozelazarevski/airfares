# -*- coding: utf-8 -*-

# -*- coding: cp1251 -*-
# the first line does not wish to work ;)

########################
# Special edition :))))
# http://goo.gl/cZU0U
########################

# loading magic spells
import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import * 
# import numpy as np # to deal with arrays of numbers
# import pandas as pd # the must for econometrics :) in python
# import csv # read/write csv files

# what should i download?
dest_from = ["MOW"] # 'LED' --- Saint-Petersburg
dest_to = ["PAR"]
fly_class = ["E"] # 'E' stands for economy, 'B' --- for business
trip_length = [13] # nominal trip length in days

starting_departure_date = date(2013,5,15) # we will consider all departure days from this one
final_departure_date = date(2013,5,15) # upto this one


num_departure_dates=(final_departure_date-starting_departure_date).days+1 # the total number of departure dates to consider


# just checking the magic spells :)
# print(starting_departure_date.strftime('%Y%m%d')) 


all_pages = []

for i in range(num_departure_dates):
    for j in trip_length:
        departure_date = starting_departure_date + timedelta(days=i)
        return_date = departure_date + timedelta(days=j)
        departure_date_str = departure_date.strftime("%Y%m%d")
        return_date_str = return_date.strftime("%Y%m%d")
        
        # constructing all the pages for given departure and return dates...
        more_pages = [('http://sindbad.ru/ru/flight/results/'+x+y+departure_date_str+return_date_str+'100'+z+'0') for x in dest_from for y in dest_to for z in fly_class]
        
        # adding them in the all_pages list
        all_pages.extend(more_pages)

        
# all_pages

test = u"SVO17:1015&nbsp;Мая"

def convert_time_and_date(work):
    '''
    this function should convert a string of type 'SVO17:1015&nbsp;Мая' to something readable :) 
    we assume 3 letters airports acronyms
    we set the year to 2013
    '''
    
    # replace month names by numbers
    work = work.replace(u"Января","01")
    work = work.replace(u"Февраля","02")
    work = work.replace(u"Марта","03")
    work = work.replace(u"Апреля","04")
    work = work.replace(u"Мая","05")
    work = work.replace(u"Июня","06")
    work = work.replace(u"Июля","07")
    work = work.replace(u"Августа","08")
    work = work.replace(u"Сентября","09")
    work = work.replace(u"Октября","10")
    work = work.replace(u"Ноября","11")
    work = work.replace(u"Декабря","12")


    #cut the first 3 letters
    # WARNING!!!!! here we assume that airports abbreviations have 3 (three) letters
    work = work[3:]

    # convert string to date and time format
    time_and_date = datetime.strptime(work,"%H:%M%d&nbsp;%m")

    # the year is not specified and we set it manually
    time_and_date = time_and_date.replace(year=2013)
    
    return(time_and_date)

# testing ...
# convert_time_and_date(test)


test = u"7 ч. 10 мин."

def convert_fly_length(work):
    '''
    this function should convert a string of type '7 ч. 10 мин.' to a list [7, 10] 
    maybe one should use strptime function but i can't deal with encodings :(
    '''
    
    # we use spaces to split the line...
    chunks = work.split(' ')
    
    hours = int(chunks[0])
    minutes = int(chunks[2])

    return([hours,minutes])




# un lien pour que les nègres littéraires se reposent un peu
# http://www.vmdaily.ru/news/2005/09/26/rabi-aleksandra-dyuma-15713.html?print=true&isajax=true

# page = 'http://sindbad.ru/ru/flight/results/MOWPAR2013051520130528100B0'

file_num = 1000000 # i prefer that all file names have equal length


for page in all_pages:
    
    # I forgot completely about this:
    fl_class = page[61:62]
    fl_from = page[36:39]
    fl_to = page[39:42]
    
    # I wonder how much time does it take to parse one page
    begin_time = datetime.now() # get current time upto microseconds
    
    
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
    
    for n in range(quantity):
        table1.append(table.findAll('div', {'class': 'variants clf pie fForward'})[n])
            
    
    opt_quants = [] 
    
    for i in range(quantity):
        opt_quant = len(table1[i].findAll('div', {"class" : "clf resChain"}))
        opt_quants.append(opt_quant)
        
    print "рейсы туда: " + str(opt_quants)
    
    
    # количество вариантов в табличке обратно
    
    table2 = []
    
    for n in range(quantity):
        table2.append(table.findAll('div', {'class': 'variants back clf pie fBack'})[n])
            
    
    opt_quants2 = [] 
    
    for i in range(quantity):
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
    
    for n in range(quantity):
        table2.append(table.findAll('div', {'class': 'variants back clf pie fBack'})[n])
            
    
    trans_s2 = [] 
    
    for i in range(quantity):
        trans2 = len(table2[i].findAll('div', {"class" : "trans"}))
        trans_s2.append(trans2)
        
    print "пересадки обратно: " + str(trans_s2)
        
    # количество авиакомпаний в каждой табличке
    
    table3 = []
    
    for n in range(quantity):
        table3.append(table.findAll('div', {'class': 'carriers-logos'})[n])
		
    
    comp = [] 
    
    for i in range(quantity):
        alliance = len(table3[i].findAll('a', {'class' : 'company-logo'}))
        comp.append(alliance)
        
    print "кол-во авиакомпаний: " + str(comp)
    
     
    
    # Вытащить цены билетов
    
    price=[]
    
    for n in range(quantity):
        price.append(table.findAll('span', {"class" : "lPrice"})[n].text)
    
    for n in range(len(price)):
        price[n]=price[n][:6]
    
    # print price
    
    # Вытащить время вылета, время прилёта, длительность полёта
    
    q = (len(table('div', {"class" : "col"})))
    
    #print q 
    
    times_list=[]
    
    for n in range(q):
        times_list.append(table.findAll('div', {'class':'col'})[n].text)
        
    # print u" ".join(times_list)	
    
    
    # название авиакомпании
    
    qua = (len(table('a', {"class" : "company-logo"})))
    # print qua
    
    company=[]
    
    for n in range(qua):
        company.append(table.findAll('a', {'class':'company-logo'})[n])
    
    # print company
    
  
    
    ####################################
    # saving results...
    
    file_num = file_num + 1
    file_name = str(file_num)+'.csv'
    
    ####################################
    # save prices, number of changes, number of options
    
    # 1. remove space (replace space by nothing) 
    # 2. convert to integer with 'int' function
    new_price = [int(p.replace(" ","")) for p in price] 
    
    # print(new_price) # just checking
    
    
    # create a dataframe from lists...
    # df = pd.DataFrame({"price" : new_price,"ncomp" : comp,"changes1" : trans_s1,"changes2" : trans_s2,"options1" : opt_quants,"options2": opt_quants2})
    # df.to_csv('price_'+file_name) # save everything

    f = open('price_'+file_name,'w') # start writing file
    f.write(",changes1,changes2,ncomp,options1,options2,price\n") # write first line (variable names)
    
    for t in range(len(new_price)):
        f.write(str(t)+","+str(trans_s1[t])+","+str(trans_s2[t])+","+str(comp[t])+","+str(opt_quants[t])+","+str(opt_quants2[t])+","+str(new_price[t])+"\n") # write next line
    f.close() # end of writing

    
    
    # df # just look at it

    ####################################
    # save aviacompanies

    # save raw, unparsed companies list, for debugging purposes
    # df_raw_comp = pd.DataFrame({'raw':company})
    # df_raw_comp.to_csv("raw_comp_"+file_name)

    f = open('raw_comp_'+file_name,'w') # start writing file
    f.write(",raw\n") # write first line (variable names)
    
    for t in range(len(company)):
        f.write(str(t)+","+str(company[t])+"\n") # write next line
    f.close() # end of writing


    
    # Voila!

    comp_name = []
    
    for c in company:
        # the string is cut into 3 parts: before 'title="', the word 'title="' itself and after 'title="'
        left_part, middle_part, right_part = str(c).partition('title="') 
    
        # we need only the right_part
        new_name, garbage, garbage2 = right_part.partition('"') # the string is cut into 3 parts: the first '"' is the separator , we take the leftmost. The rest is garbage.
        comp_name.append(new_name)
    
  
    # comp_name[0:10] # just checking
    
    # with pandas we have 2 lines
    # df_companies = pd.DataFrame({'comp_name' : comp_name}) # create a dataframe with one variable
    # df_companies.to_csv("companies_"+file_name) # save dataframe to csv

    # without pandas we have 5 lines :)
    f = open('companies_'+file_name,'w') # start writing file
    f.write(",comp_name\n") # write first line (variable names)
    
    for t in range(len(comp_name)):
        f.write(str(t)+","+comp_name[t]+"\n") # write next line
    f.close() # end of writing

    ####################################
    # save times and flight length

    # save raw, unparsed times_list, for debugging purposes
    #df_raw_flights = pd.DataFrame({'raw':times_list})
    #df_raw_flights.to_csv("raw_fly_"+file_name)
    
    f = open('raw_fly_'+file_name,'w') # start writing file
    f.write(",raw\n") # write first line (variable names)
    
    for t in range(len(times_list)):
        f.write(str(t)+","+times_list[t]+"\n") # write next line
    f.close() # end of writing
    
    
    # remove the words "Прилет", "Вылет", "В пути". We leave only the strings with more than 10 characters (or bytes?)
    times3 = [p for p in times_list if len(p)>10] 
    
    if len(times3)%3>0: # if the residual is not zero then ACHTUNG!
        print("Achtung: something went wrong. We should have 3 lines for each flight!")
    
    num_flights = len(times3)/3
    
    dep_time = []
    arr_time = []
    duration_hours = []
    duration_minutes = []
    
    for i in range(num_flights):
        dep_time.append(convert_time_and_date(times3[3*i]).strftime("%Y-%m-%d %H:%M"))
        arr_time.append(convert_time_and_date(times3[3*i+1]).strftime("%Y-%m-%d %H:%M"))
        
        duration = convert_fly_length(times3[3*i+2])
        
        duration_hours.append(duration[0])
        duration_minutes.append(duration[1])
        
        
    parse_time = begin_time.strftime("%Y-%m-%d %H:%M") # we should also save the current time (!)

    # df_flights=pd.DataFrame({'dep_time' : dep_time, 'arr_time' : arr_time, 'dur_hours' : duration_hours, 'dur_minutes' : duration_minutes})
    
    # it will be constant for the given table but it will vary across flights tables
    # df_flights['parse_time'] = parse_time
    # df_flights['fl_class']=fl_class
    # df_flights['fl_from']=fl_from
    # df_flights['fl_to']=fl_to
    
    
    # df_flights.to_csv("flights_"+file_name) # save to csv
    
    f = open('flights_'+file_name,'w') # start writing file
    f.write(",arr_time,dep_time,dur_hours,dur_minutes,parse_time,fl_class,fl_from,fl_to\n") # write first line (variable names)
    
    for t in range(len(dep_time)):
        # write next line
        f.write(str(t)+","+arr_time[t]+","+dep_time[t]+","+str(duration_hours[t])+","+str(duration_minutes[t])+","+parse_time+","+fl_class+","+fl_from+","+fl_to+"\n") 
    f.close() # end of writing
    
    
    
    
    #####
    # calculating elapsed time
  
    end_time = datetime.now() # get current time upto microseconds
    time_elapsed = end_time - begin_time
        
    print(time_elapsed)



