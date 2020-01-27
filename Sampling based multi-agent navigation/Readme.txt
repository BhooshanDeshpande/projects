============================================================|
The parameters selected for the simulation scenarios are :  |	
============================================================|
SCENARIO : 

	 |  3 Agents 	|   8 Agents  	|  Crossing Agents |
	 |______________|_______________|__________________|
	 | alpha = 7  	| alpha = 8   	| alpha =8	   |
	 | beta = 11  	| beta = 12	| beta = 22	   |
	 | gamma = 17 	| gamma = 30	| gamma = 40       | 

================================================|
Slight modification to the cost function:	|
================================================|

To account for ttc = 0, I added a very small fraction at to my ttc variable, making it (10e-18 + my_ttc_variable).
Now the division is possible, even if ttc is zero.
New Cost Function:
--------------------------------------------------------------------------------------------------
alpha * mag(self.vcand - self.gvel) + beta * mag(self.vcand - self.vel) + gamma / (10e-200 + tau)
---------------------------------------------------------------------------------------------------

================================================|
THE REASONS FOR SELECTING THESE PARAMETERS	|
================================================|

1. gamma is the largest.
Priority is to keep the the agents separated first.(factors for increasing ttc) 
------------------------------------------------------------------------------------
2. Beta is slightly larger than alpha, but significantly lesser than gamma.
The colliding agent should be able to maintain it's current velocity rather 
than pursuing it's goal velocity (So that behavior is more natural).
------------------------------------------------------------------------------------
3.alpha is kept lowest.
Increasing alpha causes agents to reach their destination faster, but it comes at
the cost of collision and unnatural behavior.

============|
COMMENTS    |	
============|

The simulation was tried with multiple cost functions, and one startegy of considering
the closest's neighbors velocity and defining our escape velocity according to it was 
working out. But unfortunately, I could only test it with 3_agents scenario, and as more agents get 
involved, the work on K-nearest neighbors needs to be done, which is out of the current scope.
If there is a scope to work on this, I'd like to pursue more on this part.
 