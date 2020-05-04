from itertools import product
from functools import reduce
import operator

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

def Reverse_Bin(num, k):
    b = bin(num)
    rev = b[-1:1:-1]
    rev = rev+ (k-len(rev))*'0'
    return rev

def Create_FA(expression):
    #convert the expression to tuples
    #aka convert the values of x1, x2, and x3 to binary then gather the a1,a2,a3 accordingly
    #find the longest bit value to know how padded the binary number must be
    tuples = [(1,1,1), (1,1,0), (1,0,1), (1,0,0), (0,1,1), (0,1,0), (0,0,1), (0,0,0)]
    k = Find_KC(expression[3])
    print k
    m = C_Max(expression)
    print "Value of Cmax {}".format(m)
    #Find reverse values of x1,x2,x3 back filled with 0's
    FA = {}
    #Keep generating states until the accepting is found carry = 0, i = KC+1
    #while(carry !=0 and i != k+1)
    for carry in range(-1*m, m+1):
        for i in range(1, k+2):
            for carry_prime in range(-1*m, m+1):
                for i_prime in range(1, k+2):
                    for h in tuples:
                        state = (carry, i)
                        state_prime = (carry_prime, i_prime)
                        R = expression[0]*h[0] +expression[1]*h[1] +expression[2]*h[2] + int(Find_B_i(expression[3], i)) +carry
                        #Checking if the value that is given will work for the given constraints
                        if(R % 2 == 0):
                            if(i_prime == i or i_prime == i+1):
                                if(carry_prime == R/2):
                                    if state in FA:
                                        FA[state].append((state_prime, h))
                                    else:
                                        FA[state] = [(state_prime, h)]
    #Prints the value of the dict to verify entries
    #for key, value in FA.iteritems():
        #print key, '\t', value
    return FA

def Get_final(expression, FA):
    k = Find_KC(expression[3])
    print k
    for value, key in FA.iteritems():
        if value == (0, k+1):
            return value


def Cartesion_Product(M1, M2):
    cart_dict ={}
    for value, key in M1.iteritems():
        for v, k in M2.iteritems():
            #print value
            #print v
            state = (value[0]*v[0], value[1]*v[1])
            #print "state {}".format(state)
            for i in key:
                for j in k:
                    if i[1] is j[1]:
                        #print "{0} {1}".format(i, j)
                        carry = i[0][0] * j[0][0]
                        #print carry
                        t = i[0][1] * j[0][1]
                        #print t
                        new_state = (carry, t)
                        h = i[1]
                        if state in cart_dict:
                            cart_dict[state].append((new_state, h))
                        else:
                            cart_dict[state] = [(new_state, h)]
    return cart_dict
       
#DFS
def DFS(M, end, visited, node):
    if node not in visited:
        visited.append(node)
        for n in M[node]:
            DFS(M, end, visited, n)
    return visited




if __name__ =='__main__':
    expression1 = [-3, -2, -1, 3]
    expression2 = [6, -4, 1, 3]

    M1 = Create_FA(expression1)
    M2 = Create_FA(expression2)

    end1 = Get_final(expression1, M1)
    print "End1 {}".format(end1)

    end2 = Get_final(expression2, M2)
    print "End2 {}".format(end2)

    final = (end1[0]*end2[0], end1[1]*end2[1])

    M = Cartesion_Product(M1, M2)

    solution = DFS(M, final, [], (0,1))

    #for key, value in M.iteritems():
        #print key, '\t', value
  
