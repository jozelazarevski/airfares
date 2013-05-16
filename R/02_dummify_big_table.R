# Parsing sindbad.ru

# create dummy for each company and coerce lines corresponding
# to one flight into one observation

## WARNING!

# We should already have the COMPLETE list of companies!
# So big hubs (London, Paris, Frankfurt...) should be already downloaded
# BEFORE running this part
# New company means new dummy variable

library(reshape)
library(dummies)
library(plyr)



setwd("~/courseworks/2013/annette/")
h <- read.csv(file="all_fly_data.csv")

file.out <- "all_fly_data_dummy.csv"

######################################
# using ddply from plyr

# It's a bad idead to have spaces in variable names (!)
# ddply will stop with an error in such a situation

# So we replace spaces by underscores in the company names
levels(h$comp_name) <- gsub(" ","_",levels(h$comp_name))

# replace company name by a just a number
# h$comp_name <- as.integer(h$comp_name)

# maybe we should use short company codes?
# avia.codes.link <- "http://www.census.gov/foreign-trade/reference/codes/aircarrier/acname.txt"


# create dummies
dummies <- dummy(h$comp_name)

# get all dummy names
dummy.names <- colnames(dummies)

# adding dummies to data set
hd <- cbind(h,dummies)
# str(hd)

# variables used to split the data set:

# that's an ugly way, but...
dput(colnames(h)) # and than edit by hands to get...
split.vars <- c("price.index", "arr_time.x", "dep_time.x", "dur_hours.x", 
                "dur_minutes.x", "parse_time.x", "fl_class.x", "fl_from.x", "fl_to.x", 
                "arr_time.y", "dep_time.y", "dur_hours.y", "dur_minutes.y", "parse_time.y", 
                "fl_class.y", "fl_from.y", "fl_to.y", "changes1", 
                "changes2", "ncomp", "options1", "options2", "price", "stops1", 
                "stops2", "opt.sum")

  
  
  
# res <- ddply (hd, split.vars, summarise, 
#               comp_name1 = sum(comp_name1),
#               comp_name2 = sum(comp_name2),
#               comp_name3 = sum(comp_name3),
#               # ...
#               # It works!
#               # Feng-Shui says that it should be done differenlty!
#               .progress="text")


result <- ddply(hd, split.vars, colwise(sum,dummy.names),
              .progress="text")

write.csv(result,file=file.out)


# ##########################################
# ### Using cast from reshape. Problems with big data set.
# 
# # names of all the variables
# var.names <- colnames(h)
# 
# # remove "comp_name", "X" and "X.1" from var.names
# var.names <- var.names[var.names != "comp_name"]
# var.names <- var.names[var.names != "X"]
# var.names <- var.names[var.names != "X.1"]
# 
# # formula for casting data from from "long" to "wide" format in text form
# # all the variables except "X", "X.1", "comp_name" on the left side
# # "comp_names" on the right side
# cast.formula.txt <- paste( paste(var.names,sep="",collapse="+") , "~comp_name" , sep="" )
# 
# # check it!
# print(cast.formula.txt)
# 
# # convert it to formula object
# cast.formula <- as.formula(cast.formula.txt)
# 
# # VERY important mystery command that will be explained later ;)
# h$ones <- 1 
# 
# # clearing chakras...
# 
# # ...
# 
# # receiving cosmic energy...
# 
# # ...
# 
# # refilling mana...
# 
# # ...
# 
# # READY?
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# # GO!
# all.data.dum <- cast(data=h , cast.formula, sum)
# 
# # ones are important because "cast" function will sum them
# # without this trick with "sum" and "ones" there will be NA instead of zeros
# 
# write.csv(all.data.dum,file=file.out)
