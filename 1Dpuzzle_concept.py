import numpy as np
import random
import string
from IPython.display import clear_output
import time
np.set_printoptions(linewidth=200) # just for visual checking

letters = [char * 2 for char in string.ascii_lowercase]
random.shuffle(letters)

def generate_grid(width=32, height=17):
    """
    whole grid size including padding: 32*17
    padding: outer 3 layers
    pad = 2, empty = 0, not empty = 1
    """
    grid = []
    for i in range(height):
        if i < 2 or i >= height - 1:
          if i == 0:
            grid.append([f"{y:02}" for y in range(width)])
          else:
            grid.append([f"{i:02}"]+["--" for y in range(width-1)])
        else:
            grid.append([f"{i:02}"] + ["--"] + ['||' for y in range(width-2-2)] + ["--" for y in range(2)])
    grid_np = np.array(grid)
    return grid_np

def generate_piece_initial(grid):
    """
    make a temporary grid copy to not affect original grid
    parse the grid (disregard outerlayer) using non-overlapping 5x5 pieces
    for the ith piece, consider every pixel that is not "xx" and is 00, randomly assign it as i or 0
    then append the ith piece to the pieces list/dictionary (whichever better)
    """
    pieces = []
    temp_grid = grid.copy()
    # there should be 18 initial 5x5 pieces
    # center pixel of each piece ((col, row) = (x, y))
    centers = [(3, 3), (8, 3), (13, 3), (18, 3), (23, 3), (28, 3),
               (3, 8), (8, 8), (13, 8), (18, 8), (23, 8), (28, 8),
               (3, 13), (8, 13), (13, 13), (18, 13), (23, 13), (28, 13)]
    for i, (center_col, center_row) in enumerate(centers, start=1):
      for row in range(center_row-2, center_row + 3): #if grid_coor_row = 5, row from 3 to 7
        for col in range(center_col-2, center_col + 3):
          if temp_grid[row][col] == '||':
            if random.randint(0, 1) == 0:
              temp_grid[row][col] = letters[i-1] # f"{i:02}"
      piece = temp_grid[center_row-2:center_row + 3, center_col-2:center_col + 3]
      pieces.append(piece)
    return pieces, temp_grid

def generate_piece_followup(temp_grid, pieces):
    """
    make a temporary grid copy to not affect original grid
    parse the grid (disregard outerlayer) using non-overlapping 7x7 pieces
    for the 18+ith piece, consider every pixel that is not "xx" and is 00, assign it as 18+i
    then append the ith piece to the pieces list/dictionary (whichever better)
    """
    # there should be 8 follow up 7xx pieces
    # center pixel of each piece ((col, row) = (x, y))
    num_initial_pieces = len(pieces)
    centers = [(5, 5), (12, 5), (19, 5), (26, 5),
               (5, 12), (12, 12), (19, 12), (26, 12)]
    for i, (center_col, center_row) in enumerate(centers, start=1):
      for row in range(center_row-3, center_row + 4):
        for col in range(center_col-3, center_col + 4):
          # print(col, row)
          if temp_grid[row][col] == '||':
            temp_grid[row][col] = letters[num_initial_pieces-1 + i] #f"{num_initial_pieces + i:02}"
      piece = temp_grid[center_row-3:center_row + 4, center_col-3:center_col + 4]
      pieces.append(piece)
    return pieces, temp_grid

def piece_cleaning(pieces):
    """
    Process pieces to:
    1. Convert non-piece cells to '||'
    2. Ensure all pieces are 7x7 by padding smaller pieces with '||'
    """
    cleaned_pieces = []
    for idx, piece in enumerate(pieces):
        # Get piece ID based on position in list
        target = letters[idx]
        # Create mask for current piece's cells
        cleaned = np.where(piece == target, target, '||')
        # Pad to 7x7 if needed
        if cleaned.shape != (7, 7):
            # Calculate padding needed (for 5x5 -> 7x7)
            pad_size = (7 - cleaned.shape[0]) // 2
            cleaned = np.pad(cleaned, pad_size, mode='constant', constant_values='||')
        cleaned_pieces.append(cleaned)
    return cleaned_pieces

def available_pieces(grid):
  """
  returns array PLAYABLE that contains cleaned and randomly rotated and flipped pieces that can be placed on the grid
  """
  pieces, temp_grid = generate_piece_initial(grid)
  pieces, temp_grid = generate_piece_followup(temp_grid, pieces)
  cleaned_pieces = piece_cleaning(pieces)
  PLAYABLE = []
  for piece in cleaned_pieces:
    x = random.randint(1, 4)
    piece = rotate(piece, x)
    flip = random.randint(0, 2)
    if flip == 1:
      piece = flip_horizontal(piece)
    elif flip == 2:
      piece = flip_vertical(piece)
    PLAYABLE.append(piece)
  return PLAYABLE

def rotate(piece, x):
    """
    Rotate the piece 90 degrees counterclockwise x times
    Args:
        piece: numpy array representing the puzzle piece
        x: number of 90-degree rotations (1=90°, 2=180°, 3=270°, 4=360°)
    Returns:
        Rotated numpy array
    """
    return np.rot90(piece, x)

def flip_horizontal(piece):
    """Left-right flip"""
    return np.fliplr(piece)

def flip_vertical(piece):
    """Top-bottom flip"""
    return np.flipud(piece)

def update_grid(grid, piece):
    print("\033c", end="") # clear terminal for updating the visual interface
    clear_output(wait=False)
    time.sleep(0.1)
    print(grid, "\n")
    print(piece) # the current selected piece, empty by default

def place_piece(grid, piece, x, y, PLAYABLE):
    """
    place the piece in the grid, if overlap or out of bounds, dont place and print error message
    overlap condition: if any non "||" in the piece takes the same place as a non "||" in the grid
    out of bounds condition: if any non "||" in the piece takes the same place as a "--" in the grid
    x, y represents where the center of the 7x7 piece is in the grid
    """
    # Calculate top-left corner of the piece
    start_x = x - 3
    start_y = y - 3
    # Check boundaries and overlaps
    for i in range(7):
        for j in range(7):
            piece_cell = piece[i, j]
            # if piece_cell == '||':
            #     print("analyzing next cell")
            grid_x = start_x + j
            grid_y = start_y + i
            # Check playable area boundaries (columns 2-29, rows 2-15)
            if not (2 <= grid_x <= 29 and 2 <= grid_y <= 15):
                print("Error: Piece extends outside play area")
                # return False, "Out of bounds"
            # Check for existing pieces or padding
            current_cell = grid[grid_y, grid_x]
            if current_cell != '||':
                print(f"Error: Collision at ({grid_x}, {grid_y})")
                # return False, "Overlap detected"
    # Place the piece
    for i in range(7):
        for j in range(7):
            piece_cell = piece[i, j]
            if piece_cell != '||':
                grid_x = start_x + j
                grid_y = start_y + i
                grid[grid_y, grid_x] = piece_cell
    PLAYABLE.pop(0) # if the piece is rotated, may not be able to remove, use similar method as next
    print("Piece placed successfully")


# game
game = True
grid = generate_grid()
PLAYABLE = available_pieces(grid) # mutable and can decrease in size as pieces are used
current_piece = PLAYABLE[0]
while game == True:
  update_grid(grid, current_piece) #not clearing terminal b4 update
  print(f"availiable actions: place[x,y], fliph, flipv, rotate90*z), next, quit")
  print(f"fliph: flips the piece horizontally, flipv: flips the piece vertically, rotate90*z: rotate the piece counterclockwise by 90*z degrees")
  print(f"next: view next available piece, you have {len(PLAYABLE)} pieces left")

  # check if grid contains any "||", if yes -> pass, if no, player wins
  if "||" not in grid:
    print("YOU WIN")
    break
  else:
    update_grid
  print("\n")
  command = input("Enter command: ")

  if command == "fliph":
    current_piece = flip_horizontal(current_piece)
  elif command == "flipv":
    current_piece = flip_vertical(current_piece)
  elif command.startswith("rotate90*"):
    try:
        z = int(command[9:])  # Extract z from the command string
        current_piece = rotate(current_piece, z)
    except ValueError:
        print("Invalid rotation value. Please use 'rotate90*z' where z is an integer.")
  elif command.startswith("place"):
    try:
        x, y = map(int, command[6:-1].split(','))
        place_piece(grid, current_piece, x, y, PLAYABLE)
        print(len(PLAYABLE))
        current_piece = PLAYABLE[0]
        time.sleep(1)
    except ValueError:
        print("Invalid place command. Please use 'place x,y' where x and y are integers.")
  elif command == "next": #issue: it doesnt detect if the piece is rotated thus breaking
    # Find a unique identifier (e.g., the first non-"||" element)
    identifier = (current_piece[current_piece != '||'][0])
    # Find the index of the piece with the identifier in PLAYABLE
    for index, piece in enumerate(PLAYABLE):
        if identifier in piece:
            ind = index
            break
    else:
        # Handle case where identifier is not found (shouldn't happen normally)
        ind = PLAYABLE.index(current_piece) # Fallback to original behavior
    if ind < len(PLAYABLE) - 1:
      current_piece = PLAYABLE[ind + 1]
    else:
      current_piece = PLAYABLE[0]
  elif command == "quit":
    game = False
  else:
    print(f"unrecognized command, try the available actions")
