###################################################################################################
# ************************* Board **********************
###################################################################################################

board = []
for i in range(9):
  if i == 0 or i == 8:
    row = [' ',0,1,2,3,4,5,6,' ']
  else:
    row = ['-']*9
    row[0] = row[8]= 7 - i

  board.append(row)

def Show_board(matrix):
  for i in range(9):
    if i>= 2 :
      print((i-1)*'  ' , end = '')
    for j in range(9):
      print(matrix[i][j], end = '  ')
    print('\n')
    
from copy import deepcopy

###################################################################################################
# *************************Check if RED win**********************
###################################################################################################
def win_red(temp_board,row,col):

  if row == 7:
    return True

# Check the left side
  if temp_board[row][col-1] == 'R':  
    temp_board[row][col] = '*'
    return win_red(temp_board, row, col-1)

    # Check the right side
  if temp_board[row][col+1] == 'R': 
    temp_board[row][col] = '*'
    return win_red(temp_board, row, col+1)

    # Check the bottom side
  if temp_board[row+1][col] == 'R': 
    temp_board[row][col] = '*'
    return win_red(temp_board, row+1, col)

    # Check the left bottom side
  if temp_board[row+1][col-1] == 'R': 
    temp_board[row][col] = '*'
    return win_red(temp_board, row+1, col-1)

    # Check the right bootom side
  if temp_board[row+1][col+1] == 'R': 
    return win_red(temp_board, row+1 ,col+1)

##################################################################################################
# *************************Check if BLUE win**********************
###################################################################################################
def win_blue(temp2_board,row,col):

  if col == 7:
    return True

# Check the up side
  if temp2_board[row-1][col] == 'B':  
    temp2_board[row][col] = '*'
    return win_blue(temp2_board, row-1, col)

# Check the bottom side
  if temp2_board[row+1][col] == 'B': 
    temp2_board[row][col] = '*'
    return win_blue(temp2_board, row+1, col)

# Check the right up side
  if temp2_board[row-1][col+1] == 'B': 
    temp2_board[row][col] = '*'
    return win_blue(temp2_board, row-1, col+1)

# Check the right bottom side
  if temp2_board[row+1][col+1] == 'B': 
    temp2_board[row][col] = '*'
    return win_blue(temp2_board, row+1, col+1)

# Check the right  side
  if temp2_board[row][col+1] == 'B': 
    return win_blue(temp2_board, row ,col+1)


###################################################################################################
# *************************chck win fonctions**********************
###################################################################################################

def check_win_red(board) :
  temp_board = deepcopy(board)
  for i in range(1,8):
    if temp_board[1][i] == 'R':
      col = i
      row = 1
      if win_red(temp_board,row,col) == True:
        return  True    

def check_win_blue(board):
  temp2_board = deepcopy(board)
  for i in range(1,8):
    if temp2_board[i][1] == 'B':
      col = 1
      row = i
      if win_blue(temp2_board, row, col) == True:
        return  True
    
###################################################################################################
# ************************* heuristic **********************
###################################################################################################

# heuristic = (no of empty adjacent* 0.05) +(forward + backward)*0.2 + (no_of_samecolor *0.05) +(no_of_seq *0.40)
                # +((remain_to_win_left + remain_to_win_right)* 0.3)
def remain_to_win_left(hold, i, j):
  remain = 0
  if hold[i][j-1] == 'B':
    remain = (1 + remain_to_win_left(hold, i, j-1))
  return (7-remain)

def remain_to_win_right(hold, i, j):
  remain = 0
  if hold[i][j+1] == 'B':
    remain = (1 + remain_to_win_right(hold, i, j+1))
  return (7-remain)

def backward(hold, i, j):
  b = 0
  if hold[i-1][j-1] == 'B':
    b = (1 + backward(hold, i-1, j-1)) 
  if hold[i][j-1] == 'B':
    b = (1 + backward(hold, i, j-1))
  if hold[i+1][j-1] == 'B':
    b = (1 + backward(hold, i+1, j-1))
  return b

def forward(hold, i, j):
  f = 0
  if hold[i-1][j+1] == 'B':
    f = (1 + forward(hold, i-1, j+1)) 
  if hold[i][j+1] == 'B':
    f = (1 + forward(hold, i, j+1))
  if hold[i+1][j+1] == 'B':
    f = (1 + forward(hold, i+1, j+1))
  return f

def no_of_seq(hold , i, j):
    r = [-1,0,1]
    c = [-1,0,1]
    seq = 0
    for x in r:
        for y in c:
            if hold[i+x][j+y] == 'B':
                hold[i+x][j+y] = '*'
                seq = max(seq,1 + no_of_seq(hold, i+x , j+y)) 
        return seq
def no_of_seq_red(hold , i, j):
    r = [-1,0,1]
    c = [-1,0,1]
    seq = 0
    for x in r:
        for y in c:
            if hold[i+x][j+y] == 'R':
                hold[i+x][j+y] = '*'
                seq = max(seq,1 + no_of_seq_red(hold, i+x , j+y)) 
        return seq
def no_of_samecolor(hold , i, j):
    same = 0
    t = [-1,0,1]
    for x in t:
        for y in t:
            if hold[i+x][j+y] == 'B':
                same += 1
            if hold[i+x][j+y] == 'R':
                same += 0.5
    return same

def no_of_empty_adjacent(hold, i, j):
    empty = 0
    t = [-1,0,1]
    for x in t:
        for y in t:
            if hold[i+x][j+y] == '-':
                empty += 1
    return empty


def heuristic(board):
    hold = deepcopy(board)     
    max = 0
    best_i = 0
    best_j = 0

    for i in range(1,8):
        for j in range(1,8):
            # in this section we score each element of board array
            if hold[i][j] == '-' :
                hold[i][j] =  (no_of_empty_adjacent(hold , i, j) * 0.05) +(forward(hold, i, j)+backward(hold, i, j))*0.25 + (no_of_samecolor(hold , i, j) *0.05) +(no_of_seq(hold , i, j) *0.3)
                +((remain_to_win_left(hold,i,j) + remain_to_win_right(hold,i,j)) * 0.35)
                if hold[i][j] >= max:
                    max = hold[i][j]
                    best_i = i
                    best_j = j 

    # and then return index of the best choice  +(no_of_seq_red(hold , i, j) *0.15)   
    return best_i, best_j
    # return hold
    
def heuristic_R(board):
    hold = deepcopy(board)     
    max = 0
    best_i = 0
    best_j = 0
    for i in range(1,8):
      for j in range(1,8):
        if hold[i][j] == '-':
          hold[i][j] = no_of_seq_red(hold,i,j)
          if hold[i][j] >= max:
            max = hold[i][j]
            best_i = i
            best_j = j
            
    return best_i, best_j 
###################################################################################################
# ********************** MinMax Algorithm **********************
###################################################################################################

def minmax(temporary_board,depth):
      
  hold = deepcopy(temporary_board)
  
  for x in range(depth):
    i , j= heuristic(hold)
    hold[i][j] = 'B'
    if check_win_blue(hold):
      return i, j 
    
    x , y= heuristic_R(hold)
    hold[x][y] = 'R'
    if check_win_red(hold):
      return x, y 
  return heuristic(hold)


  
###################################################################################################
# ************************* Main progaram **********************
################################################################################################### 
from termcolor import colored
print(colored('Who starts the Game? 1.player , 2.Agent (Enter 1 or 2) ','black'))
inp = input()
if inp == '1':
    turn = 0
if inp == '2':
    turn = 1
# turn = 0 means R and turn = 1 means B

Show_board(board)

while( True ):
    print(colored('Enter place: (use two int number first for row and second for column i.g 1 2)','black'))
    print(colored('up dwon is for RED and right left is for BLUE','black'))

    if turn == 0:
        print(colored('Its RED turn', 'yellow'))
        inp = input().split() # [0,1]
        if (int(inp[0])  > 6 or int(inp[0]) < 0) or (int(inp[1]) > 6 or int(inp[1]) < 0):
            print(colored('Your chioce is wrong please select indexs between 0 to 6','black'))
            continue
        if board[6 - int(inp[0])+ 1][int(inp[1]) + 1] == '-' :
            board[6  -int(inp[0]) + 1][int(inp[1]) + 1] = 'R'
            turn = 1
        else:
            print(colored('Select indexes which is NOT full', 'red'))
            continue
        Show_board(board)
    if check_win_red(board) == True:
        print(colored('************* RED WON the game **************' , 'green'))
        break

    if turn == 1:
        print('Its BLUE turn')
        x,y = minmax(board,depth = 6)    
        
        if board[x][y] == '-' and turn == 1:
            board[x][y] = 'B'
            turn = 0
        else:
            print(colored('Select indexes which is NOT full', 'red'))
            continue
        Show_board(board)
    if check_win_blue(board) == True:
        print(colored('************* BLUE WON the game **************', 'green'))
        break