# Airline-Scheduling-and-Routing-using-AI
This project was developed in the context of Artificial Intelligence and Decision Systems course where the problem of finding the daily schedule and routing of aeroplanes that maximize the company profit, hereby called the Airline Scheduling And Routing (ASAR) problem.

# The algorith
The A* algorithm, which is an informed search algorithm, was implemented. With a given initial state, A* is able to find the shortest path with the smallest cost. 

At each iteration, the algorithm must choose the path that optimizes:

f(n) = g(n) + h(n)

where g(n) represents the cost of the past from the start to the current node n and h(n) the heuristic function that estimates the cheapest path from the current node until the end. 

The heuristic function was defined as:

h += (1/max_profit)

this was, by minimizing the heuristic function, the solution with maximum profit is found. The same strategy was used to define the cost function

cost = c + 1/action_profit

with c being the cost from the initial to the current state and 1/action_profit the cost of the new action.  

The goal function tests if all the flights have been performed and if the final destination matches the initial departure airport. Every time a new action is performed, the algorithms tests if the goal has already been reached.

# Testing/Input/Output

The folder test contains a series of tests used to evaluate the performance of the developed algorithm. 

The solutions and execution time to each test can be found in the file solutions.txt.

For a more detailed explanation on the input and output file format, please read the document AirlineSchedulingProject.pdf in the Docs folder.
