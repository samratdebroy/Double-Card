# Double-Card
Double Card is a 2-player game played with 24 identical cards and an 8x12 board. This repo implements the game in Python for manual play as well as AI controlled play through the Minimax algorithm.

## Dependencies
Need to install numpy before being able to run

## How to run
git clone the repo and remember the <PATH-TO-REPO> where you store the folder

using anaconda (open the Anaconda Prompt):
```
conda create --name DoubleCard python=3.7
conda activate DoubleCard
conda install numpy
cd <PATH-TO-REPO>
python DoubleCard.py
```

You can use: ``` python TestDoubleCard.py``` instead if you want to start with a board ready for recycling

### For manual play
Choose whether the first player plays as colors or dots
input commands as defined in the project definition (ex: 0 2 H 1 or H 1 H 2 2 G 1)
