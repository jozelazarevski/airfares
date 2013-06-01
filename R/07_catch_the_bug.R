# Parsing sindbad.ru

# first _actual_ computer bug was found by a woman, Grace Hopper:
# http://ids.si.edu/ids/dynamic?id=NMAH-92-13130&container.fullpage

# catch the bug in file num 100 (!)


#### RESULT:

#  It's not a BUG, it's an undocumented FEATURE! 
#  RAW data may contain the SAME flight TWICE! 

#  I don't know why. One needs to find such an example live on sindbad.
#  So the replacement comp_name>0 ====> comp_name=1 seems OK

#####



# Convert all the files (check!)
# flights_xxx.csv, companies_xxx.csv, price_xxx.csv
# into one big "file.out" (without dummy variables!)

file.out <- "all_fly_data.csv"

# the flights file should have 'parse_time' column

setwd('~/courseworks/2013/annette/airfares/rawdata/problem_01/')

library(lubridate)


begin.time <- now()

# ################################################
# ### get all the filenames to convert...
# 
# # get all the file names that starts with "flights_"
# fly.files.list <- list.files(pattern="^flights_")
# 
# # check
# fly.files.list
# 
# # in the future I should learn the power of regular expressions :)
# # https://xkcd.com/208/
# 
# n.files <- length(fly.files.list) # number of files to convert
# file.nums <- rep(0,n.files) # internal files numbers
# # they may be not consecutive as we may parse from different computers
# 
# # without regular expressions I am doing somesing nasty:
# for (i in 1:n.files) {
#   part <- strsplit(fly.files.list[i],"_",fixed=TRUE)[[1]][2] # take the part after "_"
#   number <- as.numeric(strsplit(part,".",fixed=TRUE)[[1]][1]) # take the part before "."
#   file.nums[i] <- number
#   # here python beats R :)
# }
# 
# 
# # now we should have all the file numbers
# # file.nums

############################################
## convert 3 files into one big table WITHOUT dummies

# let's work with one file


file.num <- 1000100


# happy.end <- NULL # No happy end exists... yet ;)

# for (file.num in file.nums) {

  # create file names
  price.file.name <- paste("price_",as.character(file.num),".csv",sep="")
  flights.file.name <- paste("flights_",as.character(file.num),".csv",sep="")
  comp.file.name <-paste("companies_",as.character(file.num),".csv",sep="")
  
  # load
  price.df <- read.csv(price.file.name)
  flight.df <- read.csv(flights.file.name)
  company.df <- read.csv(comp.file.name)
  
  
  
  # check by hand!
  # str(price.df)
  # str(flight.df)
  # str(company.df)
  
  cat("Combining 3 files N",file.num,"\n")
  
  # Automatic check of the files consistency!!!!
  
  # total number of companies in companies file count two ways
  n.comp.check <- sum(price.df$ncomp)
  if (n.comp.check!=nrow(company.df))
    print("ACHTUNG!!! The number of companies in 'flight.df' and 'company.df' does not match")
  
  # total number of flights in flights file count two ways
  tot.flights.check <- sum(price.df$options1)+sum(price.df$options2)
  if (tot.flights.check!=nrow(flight.df)) 
    print("ACHTUNG! The number of flights does not match the total number of options from price file")
  
  # the number of stops should be 0 or 1
  if (sum((price.df$changes1>0)&(price.df$changes1!=price.df$options1))>0)
    print("ACHTUNG! The number of stops (1) is positive and not equal to the number of options")
  if (sum((price.df$changes2>0)&(price.df$changes2!=price.df$options2))>0)
    print("ACHTUNG! The number of stops (2) is positive and not equal to the number of options")
  
  ########## 
  # find correct number of stops (so we divide changes number by options number)
  price.df$stops1 <- price.df$changes1/price.df$options1
  price.df$stops2 <- price.df$changes2/price.df$options2
  
  
  ###########
  # identify correspondence between data frames...
  
  # number of flights that corresponds to the same price
  price.df$opt.sum <- price.df$options1+price.df$options2
  
  # for each flight in flight.df we find its index in price.df
  flight.df$price.index <- rep(price.df$X,times=price.df$opt.sum)
  
  
  # for each company in company.df we find its index in price.df
  company.df$price.index <- rep(price.df$X,times=price.df$ncomp)
  

  ###### SUBSET the data to find the BUG!

  flight.df <- subset(flight.df,price.index==48)
  company.df <- subset(company.df,price.index==48)
  price.df <- subset(price.df,X==48)
  # when I went to my school it's number was 48
  # Maybe there lie all my problems? :)



  #####################
  # classify flights as "allez" and "retour" 
  
  # create a funny vector that has...
  # options1 on odd places
  # options2 on even places
  opts12 <- as.vector(rbind(price.df$options1,price.df$options2))
  
  # create a vector "allez" "retour" ("allez" "retour")
  ararar <- rep(factor(c("allez","retour")),nrow(price.df))
  
  # classify flights as "allez" or "retour"
  flight.df$direction <- rep(ararar,times=opts12)
  

  #  It's not a BUG, it's a FEATURE! 
  #  RAW data may contain the SAME flight TWICE!
 
  print(flight.df)
  
  # NO merges have been done yet!


  ######################
  # match "allez" and "retour"
  
  flight.allez.df <- subset(flight.df,direction=="allez")
  flight.retour.df <- subset(flight.df,direction=="retour")



  ##### than try ordinary way

  all.flight.df <- merge(flight.allez.df,flight.retour.df,
                         by.x="price.index",by.y="price.index")


  #### The BUG is earlier than THIS comment!

  # check that the merge is ok
  if (nrow(all.flight.df)!=sum(price.df$options1*price.df$options2))
    print("ACHTUNG! The number of created allez-retour options does not match price file")
  
  
  # drop unused variables
  all.flight.df <- subset(all.flight.df, select = - c(X.x,X.y,direction.x,direction.y))
  
  # direction.x is always "allez"
  # direction.y is always "retour"
  # X.x is the index of "allez" part in the flights file
  # X.y is the index of "retour" part in the flights file
  
  ############
  # merging company names to price.df
  
  company.price.df <- merge(company.df,price.df,by.x="price.index",by.y="X")

  ############
  # THE MERGE!
  current.table <- merge(all.flight.df,company.price.df,by.x="price.index",by.y="price.index")
  
  
  # Happy End!!! Ils se marièrent et eurent beaucoup d'enfants!
#  happy.end <- rbind(happy.end,current.table)
# }

# write.csv(happy.end,file=file.out)

end.time <- now()

print(end.time - begin.time)







