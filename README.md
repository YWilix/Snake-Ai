# Snake-Ai

An Ai that plays and wins tha Snake Game using Python

## How it Works 

**1-** The program starts by creating a hamiltonian cycle for the map 

**2-** The Snake will try to find a path to the apple and follow it if it's **safe to follow**
> We say that the path is safe to follow if the snake can continue the hamiltonian cycle after following it

**3-** if no such path exists or it's not safe the snake will **take a tour** around the map that helps him finding a safe path to the apple
> the tour's path also must be **safe to follow**

**4-** if steps 2 and 3 are not safe the snake will just follow the hamiltonian cycle
>steps 2 , 3 and 4 will repeat over and over making the snake getting longer

**5-** when the snake's length reaches 65% of the map he will stop doing steps 2 and 3 and instead he will just follow the hamiltonian cycle
