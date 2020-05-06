# Brett Anzlovar
# ID 11570595
# CPTS 350
# Final Project

#----------- Linear Diophantine Equations -----------

#----------------------------------------------------
#---------- Must compile in Python 2.7 --------------
#----------------------------------------------------


# Find the value of Cmax given there are only 4 values
# of the d {0,1}
def C_Max(nums):
    max = 0
    for i in range(0,2):
        for j in range(0,2):
            for h in range(0,2):
                for l in range(0,2):
                    g = nums[0]*i + nums[1]*j + nums[2]*h + l
                    #print(g)
                    if abs(g) > max:
                        max = abs(g)
    return max

#Finds the value of K_c = #bits to represent the number
def Find_KC(number):
    b = bin(number)[2:]
    #print(b)
    if(number == 0):
        return 0
    return len(b)

# Finds the value of b at the i-th place
def Find_B_i(number, spot):
    b = bin(number)[2:]
    b = b+'0'
    k = Find_KC(number)
    if(1 <= spot and spot <= k+1):
        return (b[spot-1])
    return 0

# Creates the FA given an expression
def Create_FA(expression):
    # Set the values of a as tuples to speed up the comparison
    tuples = [(1,1,1), (1,1,0), (1,0,1), (1,0,0), (0,1,1), (0,1,0), (0,0,1), (0,0,0)]
    k = Find_KC(expression[3])
    print ("Value of kmax {}".format(k))
    m = C_Max(expression)
    print ("Value of Cmax {}".format(m))
    FA = {}
    # Start looping through each value of carry, i, carry', and i' and for each tuple of a
    for carry in range(-1*m, m+1):
        for i in range(1, k+2):
            for carry_prime in range(-1*m, m+1):
                for i_prime in range(1, k+2):
                    for h in tuples:
                        # Set the current state as a tuple
                        state = (carry, i)
                        # Set the new state
                        state_prime = (carry_prime, i_prime)
                        # Get value of R
                        R = expression[0]*h[0] +expression[1]*h[1] +expression[2]*h[2] + int(Find_B_i(expression[3], i)) +carry
                        #Checking if the value that is given will work for the given constraints
                        if(R % 2 == 0):
                            if(i_prime == i or i_prime == i+1):
                                if(carry_prime == R/2):
                                    # Insert the values into the dict
                                    if state in FA:
                                        FA[state].append((state_prime, h))
                                    else:
                                        FA[state] = [(state_prime, h)]
    #Prints the value of the dict to verify entries
    for key, value in FA.iteritems():
        print key, '\t', value
    return FA

# Finds what the final state will be for a given FA (0, Kc+1)
def Get_final(expression, FA):
    k = Find_KC(expression[3])
    print (k)
    for value, key in FA.iteritems():
        if value == (0, k+1):
            return value

# Generates the Cart Product of two FA's
def Cartesion_Product(M1, M2):
    cart_dict ={}
    # Loop through each node in each graph
    for value, key in M1.iteritems():
        for v, k in M2.iteritems():
            #print value
            #print v
            # Combining the states
            state = (value[0]*v[0], value[1]*v[1])
            #print "state {}".format(state)
            for i in key:
                for j in k:
                    # Check to see if the output is the same
                    if i[1] == j[1]:
                        carry = i[0][0] * j[0][0]
                        t = i[0][1] * j[0][1]
                        new_state = (carry, t)
                        h = i[1]
                        check = (new_state, h)
                        if state in cart_dict:
                            if check in cart_dict[state]:
                                continue
                            else:
                                cart_dict[state].append(check)
                        else:
                            cart_dict[state] = [check]
    return cart_dict
       
# DFS Search that use recursion to find the path from 
# start to end in the given graph
# This algorithm was found on python's website
# https://www.python.org/doc/essays/graphs/
def DFS(graph, end, start, path=[]):
    # Add the current node to path (aka visited and accepted nodes)
    path = path +[start]
    # Check for end condition
    if start[0] == end:
        return path
    # Check to see if the key entered exists
    if not graph.has_key(start[0]):
        return None
    # Look at all nodes that the current node points to
    # and run recursive call to test them 
    for node in graph[start[0]]:
        if node not in path:
            newpath = DFS(graph, end, node, path)
            if newpath: 
                return newpath
    return None

# Given the inputs from the end path in the final graph
# reverses the tuples then finds the solution by converty back to int   
def Find_solution(sol):
    f = []
    for value in sol:
        print value[1]
        f.append(value[1])
    f.reverse()
    num1 = ""
    num2 = ""
    num3 = ""
    for val in f:
        num1 = num1+str(val[0])
        num2 = num2+str(val[1])
        num3 = num3+str(val[2])
    return (int(num1, 2), int(num2, 2), int(num3, 2))


if __name__ =='__main__':
    expression1 = [3, -2, -1, 3]
    expression2 = [6, -4, 1, 3]

    print("Generate the graph of M1")
    M1 = Create_FA(expression1)
    print("Generate the graph of M2")
    M2 = Create_FA(expression2)

    end1 = Get_final(expression1, M1)
    print ("End1 {}".format(end1))

    end2 = Get_final(expression2, M2)
    print ("End2 {}".format(end2))

    final = (end1[0]*end2[0], end1[1]*end2[1])
    
    M = Cartesion_Product(M1, M2)
    start = ((0,1), (0,0,0))
    
    solution = DFS(M, final, start, []) 

    answer = Find_solution(solution)
    
    # Answer
    print answer