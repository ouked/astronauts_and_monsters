# Astronauts and Monsters 🛶

An implementation of the common ["river crossing problem"](https://en.wikipedia.org/wiki/River_crossing_puzzle) for the [Artificial Intelligence (CM20252)](http://www.bath.ac.uk/catalogues/2017-2018/cm/CM20252.html) module at University of Bath.

## The problem 👺
> "Three missionaries and three cannibals are on one side of a river, along with a boat that can hold one or two people. Find a way to get everyone to the other side without ever leaving a group of missionaries in one place outnumbered by the cannibals in that place."

*Exercise 3.9 in Russell & Norvig (2016, 3rd ed.)*

*Note that missionaries have been renamed to "Astronauts" and cannibals to "Monsters" in an attempt to avoid the problematic theme, though the code still uses the original names so that it is inline with the course content.*

## Solution 👩🏼‍🚀
The ```game.search()``` method will use **Breadth-first** or **Depth-first** graph traversal to find a solution to the problem, shown below:

![Optimal Solution](http://www.aiai.ed.ac.uk/~gwickler/images/mc-search-space.png)

*Credit: [Gerhard Wickler](http://www.aiai.ed.ac.uk/~gwickler/missionaries.html)*

## Demo 🌊
Probably an outdated version, but shows the code in action.

https://repl.it/@AlexDawkins/astronautsandmonsters
