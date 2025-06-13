# Uninformed-Search 
visual interface for Uninformed Search on a grid map

- To run the application, open the graph folder in some program (Visual Studio, etc.) and run the main file called: main.py (For this, the following libraries must be previously installed: tkinter, numpy, random, buscaGridNP).

- Then a window will open with some options, first you will have "Dimensions (NxN)", enter an integer to dimension the matrix, for example: if you enter 10, the matrix will be 10x10. Then, click on "New Grid" which will generate a matrix with random obstacles. You can also "Load a Grid that is in .txt format and correctly assembled by opening your file explorer and selecting the one you want.

- With the grid generated, select the "Search Method" to show the method you want to see, just below for the methods that are not "Limited Depth (LDS)" put 0 in the "limit" space, otherwise define the desired limit when running the search in limited depth.

- Finally, click with the cursor on a square painting it green declaring it as green and click again on another square to paint it red defining it as destination, and finally, click on "Search Path" the path will be shown starting as blue and changing color until reaching the destination turning red.
