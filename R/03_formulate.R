

# function to include sets of variables into a model
# basic usage:

# lm(formulate(price~stops1+stops2,dummies),data=h)

# where "dummies" is a vector with dummy names


formulate <- function (base.formula, ...) {

  # decompose formula into `~`, left side, right side:
  formula.parts <- as.character(base.formula)
  
  # original formula in text form
  formula.txt <- paste(formula.parts[2],formula.parts[3],sep="~")
  
  # adding other variables
  final.txt <- paste(c(formula.txt,...),collapse="+")
  
  return(as.formula(final.txt))
}
