import cplex
from cplex.exceptions import CplexError
import sys

my_obj = []
my_rhs = []
var_names = []
constraint_names = []
constraints = []
my_senses = []
sources = ['A', 'B', 'C', 'D']
transits = ['X', 'Y', 'Z']
dests = ['1', '2', '3', '4']

def main(argv):
	
	for source in sources:
		for transit in transits:
			for dest in dests:
				variable = 'x' + source + transit + dest
				var_names.append(variable)
				my_obj.append(1.0)
				print(variable)
				
	for i in range(0, len(var_names), 3):
		constraint = [[i, i+1, i+2], [1.0, 1.0, 1.0]]
		constraints.append(constraint)
		constraint_name =  + var_names[i][1] + var_names[i][3]
		constraint_names.append(constraint_name)
		print(constraint_name)
				
	
	
				
	
	
def populatebyrows(prob):
	prob.objective.set_sense(prob.objective.sense.minimize)
	
	

if __name__ == "__main__":
	sys.exit(main(sys.argv))
