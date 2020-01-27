The code returns the optimal path for a given tree structure using Dijkstra's algorithm. 

The tree structure can be modified to analyze different problems. 

if tree is of the following format:
 
====> A --> B with a cost of p1 for going from A to B
 
then it's definition would be:

====> {A:{A:0, B:p1}} (It is important to initialize a cost with the self node (0) for each node) 


The return of this function is the optimal path printed as the tree nodes numbers. For example:
		
====> (A, B, C) 

It means, the optimal path would be if you go from A to B to C. 

Let me know if any problems! 
