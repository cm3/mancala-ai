# mancala-ai

## Usage

For example, 

```bash
python mancala.py "nearlyrandom_ai" "naivegreedy3_ai" 100
```

returns the result of 100 matches between `nearlyrandom_ai` and `naivegreedy3_ai`

Each AI should have the `decide` static method which returns an index number from 0 to 5 based on the board status like `[4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]`
