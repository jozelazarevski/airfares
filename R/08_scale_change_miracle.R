
setwd("~/courseworks/2013/annette/airfares/data/")
h.all <- read.csv(file="all_fly_data.csv")
d <- read.csv(file="all_fly_data_dummy.csv")

library(lubridate)
library(ggplot2)


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

d$work.days <- working_days(d$dep_time.x,d$arr_time.y)


library(plyr)
d$work.days
?ddply

price.means <- ddply(d,.(work.days),summarize,mean=mean(price))
ggplot(price.means,aes(x=work.days,y=mean))+geom_bar(stat="identity")

ggplot(d, aes(x = factor(work.days))) + geom_bar()


ggplot(d, aes(x = factor(work.days), y=price)) + geom_boxplot()
ggplot(d, aes(x = factor(work.days), y=price)) + geom_violin()




# ONE
ggplot(d, aes(x = factor(work.days), y=price)) + 
  geom_bar(stat="identity")

# TWO
ggplot(d, aes(x = factor(work.days), y=price)) + 
  geom_bar(stat="identity") + scale_y_continuous(limits=c(0, 100000))









