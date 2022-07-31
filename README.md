# DecodeDemcon3 Solution Description

By running main.py, a minesweeper game is played.
The code is built for Python3, so please make sure to use this.

If no arguments are passed, a beginner field is solved (or tried to).<br/>
Valid arguments are:<br/>
<b>"beginner", "intermediate", "expert"</b> for corresponding field types to solve.<br />
<b>width: int, height: int, number_of_mines: int</b> to specifiy a custom field

##Examples
python3 main.py beginner<br/>
python3 main.py intermediate<br/>
python3 main.py expert<br/>
python3 main.py 15 15 20<br/>

##Output
The output shows the field after the game is finished. Numbers indicate cells that are opened and are not a mine. An 'x' indicates a mine that was marked and a '_' marks an unopened cell.<br/>
A message saying 'Finished' or 'Hit a mine' will indicate how the game ended.<br/>
Finally, a list of found mine coordinates is printed to the screen.<br/>