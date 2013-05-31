# seek the error
# moral of the story:
# 1. After any non-obvious transformation check consistency!
# 2. Plot the data!

setwd("~/courseworks/2013/annette/airfares/data/")
h.all <- read.csv(file="all_fly_data.csv")
hd.all <- read.csv(file="all_fly_data_dummy.csv")

summary(h.all)
summary(hd.all)

# Frog-eaters and spaghetti-heads! 4 for Air-France and Alitalia :)
hd.bad <- subset(hd.all,comp_nameAlitalia>1)

h.problem <- subset(h.all,
  (price==63450)&(dur_hours.x==6)&(dur_minutes.x==5) & (price.index==48) &
                        (dur_hours.y==6)&(dur_minutes.y==25))

# the problem is in 01_create_big_table or even earlier!!!! Maybe with python :)




