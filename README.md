# mancala-ai

## Usage

For example,

```bash
python mancala.py "nearlyrandom_ai" "naivegreedy3_ai" 100
```

returns the result of 100 matches between `nearlyrandom_ai` and `naivegreedy3_ai`

Each AI should have the `decide` static method which returns an index number from 0 to 5 based on the board status like `[4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]`

Log format is tsv of game_record, player1, player2, and winner(player1=1, player2=-1, draw=0).

Example:

```tsv
25,12,0,3,51,1,0,0,52,1,4,2,5,0,3,3,4,45,4	Nearly Random AI 2	Naive Greedy AI 3	1
```
