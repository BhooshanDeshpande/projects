SETTING GLOBAL VARIABLES: 
------------------------
In this section of the code we set all the global variables such as:
1. Forward Array 
2. Action Array 
3. Action Name Array 
4. Cost Array
5. Grid nested array
6. Initial and Goal Nodes 
7. Heuristics Array 

And Importing all the necessary files (from Utils.py) 
------------------------
------------------------
A* IMPLEMENTATION 
------------------------
Three additional functions are required for making code readable: 
1. find_chidren
'''
This function returns feasible children nodes for any parent node on a 2D grid. The inputs to this function are grid [nested 2D array] and the parent_node [tuple (x,y,o)]
 
'''

This function takes a parent node state and calculates the possible children nodes (maximum 4) from the parent node on the given grid. The possible filters for the finding childern are 
1. Whether the children node is outside the grid, if yes, discard 
2. Whether the children node is on an unnavigable space, if yes, discard 
3. Whether the children node makes our simple car move back in grid, if yes, discard (since back movement is not possible)

 
2. get_orientation
'''
This function returns the orientation of any child_node with respect to it's parent node while taking the 'Forward' global variable into account. The inputs to this function are parent_node (x,y,o) and child_node(x,y,o).

'''
This function takes a difference between the x and y locations of parent and child node and depending on the comparison of this differnce with the forward matrix, it return the possible orientation of the child node w.r.t. the global directions north,west,south,east.(0,1,2,3)

3. get_action
'''
This function returns the action to be taken by the parent_node after taking the global action_variable into account. The inputs to this function are parent_node (x,y,o) and child_node(x,y,o).
'''

This function takes the orientations from previous function and calculates the relative action to be taken by the parent_node. It takes the reference of the action variable and return [-1,0,1]

Main function: ComputePath 

Steps: 
1. Pop out current node from the open_set. 
2. Conditional Statement : if node is goal, Start tracking history of parents. 
	a. add the current_node in closed_set. 
	b. Start a while loop:
		1.Set current node as last node and derive the parent node from the parent matrix.
		2. Find out the action taken using get_action function.  
		3.Set the path matrix to the action vatiable name. 
		4.Set the current node to parent node. 
3. Add the current node to the closed set. 
4. Find feasible children  for the current node. 
5. Loop : Run a loop for every child in the feasible childern list. 
	a. Get action for the parent (based on child's orientation)  
	b. Calculate cost for the action:
		1. Path Cost(g)
		2. Heuristic (h)
		3. Action Cost 
	c. Condition: If child is not in open/closed set, add in the open set
	d. Condition: Else if child in the open set, retrieve child's cost. 
		1. Condition: if child's cost is less than previous cost, update the cost.
	e. Condition: if cost of the same child is less in history than current cost, pass.
	f. Condition: Else:  store current parent in the parent_matrix and update the cost in cost history matrix. 
6. Return the path and cost. 
-------------------------------





 
