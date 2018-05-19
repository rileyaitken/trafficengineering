import cplex
from cplex.exceptions import CplexError
import sys

f_writer = open("outputs.txt", "w+")

#Data common across all instances of this script
my_obj = [5.0, 10.0]
my_ub = [cplex.infinity, cplex.infinity]
my_rhs = [0.0, 10.0, 10.0]  #First value represents 'h' which varies 
var_names = ["x132", "x12"]
constraint_names = ["demandvolume", "capp1", "capp2"]
first_constraint = [[0, 1], [1.0, 1.0]]
second_constraint = [[0], [1.0]]
third_constraint = [[1], [1.0]]
constraints = [first_constraint, second_constraint, third_constraint]
my_sense = ["E", "L", "L"]

def frange(start, end, step):
	tmp = start
	while (tmp < end):
		yield tmp
		tmp += step

def populatebyrows(prob):
	prob.objective.set_sense(prob.objective.sense.minimize)
	
	#Lower bounds weren't defined, by default they are 0, so they are omitted
	prob.variables.add(obj = my_obj, ub = my_ub, names = var_names)
	
	prob.linear_constraints.add(lin_expr = constraints, senses = my_sense,
								rhs = my_rhs, names = constraint_names)
							
	return prob
	
	
if __name__ == "__main__":
	for h in frange(18.8, 19.0, 0.1):
		try:
			my_rhs[0] = h
			prob = cplex.Cplex()
			prob = populatebyrows(prob)
			prob.write("lpex1h" + str(h) + ".lp")
			prob.solve()
			x12 = prob.solution.get_values(1)
			f_writer.write("%f %f\n" % (h, x12))
		except CplexError as exc:
			print(exc)
		
	



