library(lubridate)
# library(plyr) # not used 

setwd("~/courseworks/2013/annette/airfares/data/")
h <- read.csv(file="all_fly_data_dummy.csv")


# testing ideas...
# a <- h$dep_time.x[1] # departure date from Russia
# b <- h$arr_time.y[1] # arrival (return) date to Russia
# 
# a.date <- as.Date(a)
# b.date <- as.Date(b)
# seq(a,b,"days")
# wday(seq(a.date,b.date,"days"))

working_days_scalar <- function(start.date,end.date, working.days = 2:6) {
  # this function works only with scalar arguments 
  
  # start.date should be one date (not a vector)
  # end.date should be one date (not a vector)
  # otherwise the problem is in seq(a,b,"days"), it will have varying length
  
  # working.days --- the vector of days when I presumably work :)
  # 1 is Sunday, 7 is Saturday, so by default 2:6
  
  a <- as.Date(start.date) # remove time
  b <- as.Date(end.date) # remove time
  
  # the vector of all weekdays between a and b
  wdays.vector <- wday(seq(a,b,"days"))
  
  # the number of working days
  result <- sum(wdays.vector %in% working.days )
  
  return(result)
}

# vectorizing the created function
working_days <- Vectorize(working_days_scalar, vectorize.args=c("start.date","end.date"))

# now one line!
start.time <- now()

h$work.days <- working_days(h$dep_time.x,h$arr_time.y)

end.time <- now()

print(end.time-start.time)
# Ubuntu 12.04, dell inspiron n5110 with 4 Gb RAM ~45 seconds
