import cplex
import sys
		
def main(argv):
	
    #Get X, Y, Z from command line
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
	
    #Needed for load balancing constraints
	sum_inversed = 1 / sum_volumes	
	print(sum_volumes)	
		
	c = cplex.Cplex()
	c.objective.set_sense(c.objective.sense.minimize)
		
    #Add path flow variable for each path ikj
	for i in range(1, X + 1):
		for j in range(1, Y + 1):
			for k in range(1, Z + 1):
				variable = 'x' + str(i) + str(j) + str(k)
				c.variables.add(names = [variable], lb = [0.0], ub = [cplex.infinity])
	
	#demand volume constraints	
	for i in range(1, X + 1):
		for j in range(1, Z + 1):
			constraint_name = ['h' + str(i) + str(j)]
			constraint_varnames = []
			constraint_coefficients = []
			for k in range(1, Y + 1): #Get all the paths/variables between i and j
				constraint_varnames.append('x' + str(i) + str(k) + str(j)) #Can give name of variable, Cplex will find it in var_names
				constraint_coefficients.append(1.0) #Coefficients, always 1.0 in this case
			constraint = [constraint_varnames, constraint_coefficients]
			my_sense = "E" #Equality constraint between sum of all path variables between source i and dest j, and i + j
			my_rhs = [i + j] #Set demand volume as i + j
			c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)
	
    #Path utilisation constraints - introduce binary variable Uij ikj
	for i in range(1, X + 1):
		for j in range(1, Z + 1):
			constraint_varnames = []
			constraint_coefficients = []
			constraint_name = ['pathUtil' + str(i) + str(j)]
			print(constraint_name)
			for k in range(1, Y + 1):
				variable = 'U' + str(i) + str(j) + str(i) + str(k) + str(j)
				c.variables.add(names = [variable], lb = [0.0], ub = [1.0], types = [c.variables.type.binary])
				constraint_varnames.append(variable)
				constraint_coefficients.append(1.0)
			constraint = [constraint_varnames, constraint_coefficients]
			my_sense = "E"
			my_rhs = [3.0]
			print(my_sense, my_rhs, constraint, constraint_name)
			c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)

    #Define path flows for each path ikj - either a third of demand volume ij or 0
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

    #capacity of links between source and transit - cik				
	for i in range(1, X + 1):
		for k in range(1, Y + 1):
			constraint_name = ['capacC' + str(i) + str(k)]
			print(constraint_name)
			variable = 'c' + str(i) + str(k)
			c.variables.add(names = [variable], lb = [0.0], ub = [cplex.infinity])
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
	
    #capacity of link between transit and destination - dkj		
	for k in range(1, Y + 1):
		for j in range(1, Z + 1):
			constraint_name = ['capacD' + str(k) + str(j)]
			print(constraint_name)
			variable = 'd' + str(k) + str(j)
			c.variables.add(names = [variable], lb = [0.0], ub = [cplex.infinity])
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
	
    #Determine load across each transit node 		
	for k in range(1, Y + 1):
		constraint_name = ['load' + str(k)]
		variable = 'loadk' + str(k)
		c.variables.add(names = [variable], lb = [0.0], ub = [cplex.infinity])
		constraint_varnames = []
		constraint_coefficients = []
		for i in range(1, X + 1):
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
			
			
	c.variables.add(names = ["r"], obj = [1.0], lb = [0.0], ub = [1.0])
	
    #Balance load across each transit node by utilising 'r'
	for k in range(1, Y + 1):
		constraint_name = ['loadbalance' + str(k)]
		constraint_varnames = ["r", 'loadk' + str(k)]
		constraint_coefficients = [1.0, -sum_inversed]
		constraint = [constraint_varnames, constraint_coefficients]
		my_sense = "G"
		my_rhs = [0.0]
		print(my_sense, my_rhs, constraint, constraint_name)
		c.linear_constraints.add(lin_expr = [constraint], senses = my_sense, rhs = my_rhs, names = constraint_name)		
	
		
	c.write("instance" + str(X) + str(Y) + str(Z) + ".lp")
    
	
if __name__ == "__main__":
	sys.exit(main(sys.argv))
