def fractional_knapsack():
    weights=[10,20,30]
    values=[60,100,120]
    capacity=50
    res=0
    for pair in sorted(zip(weights,values), key= lambda x: x[1]/x[0], reverse=True):
        if capacity<=0: 
            break 
        if pair[0]>capacity:
            res+=int(capacity * (pair[1]/pair[0])) 
            capacity=0
        elif pair[0]<=capacity:
            res+=pair[1]
            capacity-=pair[0]
    print(res)        

if __name__=="__main__":
    fractional_knapsack()
    

# Output:
# 240