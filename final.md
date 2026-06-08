## Problem
Several years ago, I wrote a game engine and an AI player for the classic game snake. That prior AI is called Pickles. I thought it would be a fun use of Z3 to implement a new AI player, now called "Ziggy" (the Z3 Solver). The main difference between Pickles and Ziggy is how they calculate paths on the grid. Pickles uses A*; Ziggy uses SMT. Each path calculation is a new solver run.

For each calculation, the inputs are the starting position, the ending position, and the list of open spaces on the grid. The output of the solver is a series of cells from the start to the end; if that is sat the difference in the adjacent cells in the series is turned into a series of moves. The AI player scaffolding originally written for Pickles does the tedium of maintaining a position in that series and feeding the moves to the game in the correct order.

Before I started this, I hypothesized that a solver is probably *not* the right tool for this problem. Actual results seem to confirm this. My intuition is that representing the changing state of the game causes a huge explosion in the search tree and in ways that are difficult for CDCL to prune. I expect that any SAT solution to the problem will be far (Hamming distance) from any other solution; which means that not finding one in a certain region of the space doesn't mean there isn't one right next door, so CDCL can't pop back multiple levels in one shot (which is how it prunes large parts of the tree).

## Encoding
At the Milestone, Ziggy was not doing well. It took multiple seconds to find trivially simple solutions on the smallest possible boards. After coming to office hours on the last week I made two changes to my encoding.
1. I had been using the theory of algebraic datatypes. I wasn't actually relying on that theory; I was simply using the tools Z3 has for that theory as a convenient way to hold the tuples that represent cells of the game board. On the idea that perhaps this was causing Z3 to get bogged down in unnecessary calculations, I switched to maintaining the x and y values of those tuples separately and using a linear combination to give each of them a pair ID for some of the constraints.
2. I had been using a `ForAll` with `Implies` for convenience when working with the sequence of cells. I understood that `ForAll` could be problematic because there are potentially infinite models. I thought the conditions I put into the `Implies` would allow that to be pruned efficiently, but it was not. For the final, I instead reasoned that the number of cells on the board is an upper bound on the length of a solution sequence and put each consequent in separately.

Other differences between the milestone and the final are syntax changes for the above 2. They all represent constraints for the solution
1. The length of the x coordinates must match the length of the y coordinates; they must also match the length of the unique IDs
2. The pair IDs must be distinct in their sequence
3. The path must start with the beginning cell and end with ending cell
4. All pairs: x and y must be inside the bounds of the board
5. All pairs: the pair ID must be consistent with the x any y
6. All pairs: the pair ID must not match any prior pair ID
7. After 0th pair: the cell on the game grid must be adjacent to the cell from the prior pair
8. After 0th pair: the pair must be in the set of open cells (the first cell is the source, which will never be in `open` coming from the game engine)

A few observations about these constraints:
* 5 and 6 work together to ensure that the path of the snake doesn't cross itself. 8 makes sure that the path of the snake doesn't cross its existing body.
* 2 and 6 seem to be duplicative. However, turning either one of them off results in the solver taking longer to make decisions and losing the game of snake earlier.

## Beats Naive
I'll suppose we're saying that the naive approach to playing Snake is to use standard pathfinding algorithms, like A*. In that case, it's less that the solver beats naive and more that it sometimes ties for easy examples.

The amount of code needed for both, in Python, slightly favors the solver. The `z3_path` function is a little less than 70 lines, ignoring comments. The `a_star` function is just 30, but relies heavily on syntactic sugar that is built up by the definition of the `Point` class and the `Direction` global, which is another 50 lines of code. The solver could almost certainly be written in fewer lines of code and easier for a human to read, if I were not brand new to SMT in Z3 and better understood the tool.

The runtime is where the solver loses. For very small boards (just 36 cells) the solver is slower than A*. For larger boards it simply chokes. SMT is not the proper tool for pathfinding. Essentially, existing graph-search algorithms encode constraints using the control flow of the algorithm. Meanwhile, Ziggy is asking S3 to calculate against those constraints at every step; it's a massive disadvantage that the solver can't realistically overcome. We're using a best-in-class NP tool on a P problem.

## What I Learned
I used just a little ChatGPT right at the beginning of brainstorming for this project; I asked it for ways to apply SAT to Snake in hopes of finding something fun to do for this project. I hated its suggestions and decided to just go full bore on getting the solver to play the game.

The most valuable part of this project for me was the practice in doing pure SAT instead of optimization. I work as a data scientist; every day I build models that minimize an objective (loss) function. Getting a chance to practice SAT with something I already understand quite well (I've spent way too much time on Snake in the past) has got me thinking about how to apply this to real problems at work.

DEMO LINK: https://youtu.be/xnztW046NXA