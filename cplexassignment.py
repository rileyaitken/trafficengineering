import cplex
import sys

my_obj = []
my_rhs = []
var_names = []
constraint_names = []
constraints = []
my_senses = []
sources = []
transits = []
dests = []

def main(argv):
	
	try:
		X = int(argv[1])
		Y = int(argv[2])
		Z = int(argv[3])
		print(X, Y, Z)
	except IndexError as e:
		print(e)
		
	for i in range(1, X + 1):
		for j in range(1, Y + 1):
			for k in range(1, Z + 1):
				variable = 'x' + str(i) + str(j) + str(k)
				var_names.append(variable)
				my_obj.append(1.0)
	
	#demand volume constraints	
	for i in range(0, len(var_names), Y * Z):
		for j in range(0, Z):
			constraint_name = 'h' + var_names[i][1] + var_names[j][3]
			constraint_rhs = []
			constraint_lhs = []
			for k in range(0, Y):
				constraint_lhs.append(j + i + (Z * k))
				constraint_rhs.append(1.0)
			constraint = [constraint_lhs, constraint_rhs]
			my_senses.append('E')
			my_rhs.append(int(var_names[i][1]) + int(var_names[j][3]))
			print(my_senses[-1], my_rhs[-1],constraint, constraint_name)
		
	
		
	
def populatebyrows(prob):
	prob.objective.set_sense(prob.objective.sense.minimize)
	
if __name__ == "__main__":
	sys.exit(main(sys.argv))
