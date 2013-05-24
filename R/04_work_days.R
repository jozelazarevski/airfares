# Количество выходных дней в течение поездки
fun_work_days <- function(start.date,end.date,saturday=TRUE) {
  n.days <- ceiling(new_interval(start.date,end.date) / ddays(1) )
  dates <- start.date + 0:n.days * ddays(1)
  week.days <- wday(dates)
  
  res <- sum(week.days==1)
  if (saturday) res <- res + sum(week.days==7)
  return(res)
}

data$index <- 1:nrow(data)

data <- ddply(data, ~index ,transform, 
               fun_work_days(dep_time.x,arr_time.y),
               .progress="text")
