# Double-Card
Double Card is a 2-player game played with 24 identical cards and an 8x12 board. This repo implements the game in Python for manual play as well as AI controlled play through the Minimax algorithm.

![](name-of-giphy.gif)

## Dependencies
# <img alt="NumPy" src="https://cdn.rawgit.com/numpy/numpy/master/branding/icons/numpylogo.svg" height="60">
Need to install numpy before being able to run

## How to run
download or git clone the repo and remember the <PATH-TO-REPO> where you store the folder

using anaconda (open the Anaconda Prompt):
```
conda create --name DoubleCard python=3.7
conda activate DoubleCard
conda install numpy
cd <PATH-TO-REPO>
python DoubleCard.py
```

### For manual play
After running ''' python DoubleCard.py ''' in the Anaconda Prompt
Choose whether the first player plays as colors or dots
Enter '0' for Colors or '1' for Dots
input commands as defined in the project specification
Ex:
Regular move
```
0 2 H 1
```
Recycle move
```
* H 1 H 2 2 G 1
```
### Running test cases

##### Batch Input
to test multiple moves in one input run ''' python DoubleCard.py '''
then copy and paste the moves into the command prompt.
Note each move should be separated by a new line
Ex:
```
0 3 A 1
0 7 C 1
0 4 E 1
```

##### Recycling Mode
You can use: ``` python TestDoubleCard.py``` instead if you want to start with a board ready for recycling.
Then continue playing the game as usual using recycling moves.



