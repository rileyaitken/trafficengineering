import cplex
import sys

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
		
	sum_volumes = 0
	for i in range(1, X + 1):
		for j in range(1, Z + 1):
			sum_volumes += i + j
		
	print(sum_volumes)	
		
	c = cplex.Cplex()
		
	for i in range(1, X + 1):
		for j in range(1, Y + 1):
			for k in range(1, Z + 1):
				variable = 'x' + str(i) + str(j) + str(k)
				c.variables.add(names = [variable], obj = [1.0], lb = [0.0], ub = [cplex.infinity])
	
	#demand volume constraints	
	for i in range(0, len(var_names), Y * Z):
		for j in range(0, Z):
			constraint_name = ['h' + var_names[i][1] + var_names[j][3]]
			constraint_varnames = []
			constraint_coefficients = []
			for k in range(1, Y + 1): #Get all the paths/variables between i and j
				constraint_varnames.append('x' + var_names[i][1] + str(k) + var_names[j][3]) #Can give name of variable, Cplex will find it in var_names
				constraint_coefficients.append(1.0) #Coefficients, always 1.0 in this case
			constraint = [constraint_varnames, constraint_coefficients]
			my_sense = ['E'] #Equality constraint between sum of all path variables between source i and dest j, and i + j
			my_rhs = [int(var_names[i][1]) + int(var_names[j][3])] #Set demand volume as i + j
			c.linear_constraints.add(lin_expr = constraint, senses = my_sense, rhs = my_rhs, names = constraint_name)
		
	for i in range(1, X + 1):
		for j in range(1, Z + 1):
			constraint_varnames = []
			constraint_coefficients = []
			constraint_name = ['pathUtil' + str(i) + str(j)]
			print(constraint_name)
			for k in range(1, Y + 1):
				variable = 'U' + str(i) + str(j) + str(i) + str(k) + str(j)
				c.variables.add(names = [variable], obj = [1.0], lb = [0.0], ub = [cplex.infinity], types = [c.variables.type.binary])
				constraint_varnames.append(variable)
				constraint_coefficients.append(1.0)
			constraint = [constraint_varnames, constraint_coefficients]
			my_sense = "E"
			my_rhs = [3.0]
			print(my_sense, my_rhs, constraint, constraint_name)
			c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)

	#for i in range(1, X + 1):
		#for j in range(1, Z + 1):
			#for k in range(1, Y + 1):
				#constraint_name = ['linkUsed' + str(i) + str(k)]
				#variable = 'link' + str(i) + str(j) + str(i) + str(k) + str(j) + str(i) + str(k)
				#c.variables.add(names = [variable], obj = [1.0], lb = [0.0], ub = [cplex.infinity], types = [c.variables.type.binary])
				#pathUtil = 'U' + str(i) + str(j) + str(i) + str(k) + str(j)
				#constraint_varnames = [variable, pathUtil]
				#constraint_coefficients = [1.0, -1.0]
				#constraint = [constraint_varnames, constraint_coefficients]
				#my_sense = "E"
				#my_rhs = [0]
				#c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)
				#constraint_varnames = []
				#constraint_coefficients = []
				#constraint_name = ['linkUsed' + str(k) + str(j)]
				#variable = 'link' + str(i) + str(j) + str(i) + str(k) + str(j) + str(k) + str(j)
				#c.variables.add(names = [variable], obj = [1.0], lb = [0.0], ub = [cplex.infinity], types = [c.variables.type.binary])
				#pathUtil = 'U' + str(i) + str(j) + str(i) + str(k) + str(j)
				#constraint_varnames = [variable, pathUtil]
				#constraint_coefficients = [1.0, -1.0]
				#constraint = [constraint_varnames, constraint_coefficients]
				#my_sense = "E"
				#my_rhs = [0]
				#c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)

	for i in range(1, X + 1):
		for j in range(1, Z + 1):
			for k in range(1, Y + 1):
				constraint_name = ['splith' + str(i) + str(j)]
				splith = (i + j) / 3
				pathUtil = 'U' + str(i) + str(j) + str(i) + str(k) + str(j)
				pathFlow = 'x' + str(i) + str(k) + str(j)
				constraint_varnames = [pathUtil, pathFlow]
				constraint_coefficients = [splith, -1.0]
				constraint = [constraint_varnames, constraint_coefficients]
				my_sense = "E"
				my_rhs = [0]
				print(my_sense, my_rhs, constraint, constraint_name)
				c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)
				
	for i in range(1, X + 1):
		for k in range(1, Y + 1):
			constraint_name = ['capacC' + str(i) + str(k)]
			print(constraint_name)
			variable = 'c' + str(i) + str(k)
			c.variables.add(names = [variable], obj = [1.0], lb = [0.0], ub = [cplex.infinity])
			constraint_varnames = []
			constraint_coefficients = []
			for j in range(1, Z + 1):
				constraint_varnames.append('x' + str(i) + str(k) + str(j))
				constraint_coefficients.append(1.0)
			constraint_varnames.append(variable)
			constraint_coefficients.append(-1.0)
			constraint = [constraint_varnames, constraint_coefficients]
			my_sense = "E"
			my_rhs = [0.0]
			print(my_sense, my_rhs, constraint, constraint_name)
			c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)
			
	for k in range(1, Y + 1):
		for j in range(1, Z + 1):
			constraint_name = ['capacC' + str(k) + str(j)]
			print(constraint_name)
			variable = 'd' + str(k) + str(j)
			c.variables.add(names = [variable], obj = [1.0], lb = [0.0], ub = [cplex.infinity])
			constraint_varnames = []
			constraint_coefficients = []
			for i in range(1, X + 1):
				constraint_varnames.append('x' + str(i) + str(k) + str(j))
				constraint_coefficients.append(1.0)
			constraint_varnames.append(variable)
			constraint_coefficients.append(-1.0)
			constraint = [constraint_varnames, constraint_coefficients]
			my_sense = "E"
			my_rhs = [0.0]
			print(my_sense, my_rhs, constraint, constraint_name)
			c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)	
			
			
			
			

				


    

def populatebyrows(prob):
	prob.objective.set_sense(prob.objective.sense.minimize)
	
if __name__ == "__main__":
	sys.exit(main(sys.argv))
