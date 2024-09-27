import random
import pygame

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("2048")


def initialize_board():
  """Creates a 4x4 board with two random tiles (2 or 4)."""
  board = [[0] * 4 for _ in range(4)]  # Create an empty 4x4 board

  # Add two random tiles
  add_random_tile(board)
  add_random_tile(board)

  return board

def add_random_tile(board):
  """Adds a new tile (2 or 4) to a random empty cell."""
  empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
  if empty_cells:
    row, col = random.choice(empty_cells)
    board[row][col] = random.choice([2, 4])

def merge_tiles(board, direction):
  """Merges adjacent tiles with the same value in the specified direction."""
  if direction == "up":
    board = transpose(board)
    merged = merge_tiles_left(board)
    board = transpose(board)
  elif direction == "down":
    board = transpose(board)
    board = reverse(board)
    merged = merge_tiles_left(board)
    board = reverse(board)
    board = transpose(board)
  elif direction == "left":
    merged = merge_tiles_left(board)
  elif direction == "right":
    board = reverse(board)
    merged = merge_tiles_left(board)
    board = reverse(board)
  else:
    raise ValueError("Invalid direction")

  return merged

def merge_tiles_left(board):
  """Merges adjacent tiles to the left."""
  merged = False

  for i in range(4):
    for j in range(3):  # Iterate up to the second-to-last column
      if board[i][j] == board[i][j + 1] and board[i][j] != 0:
        board[i][j] *= 2
        board[i][j + 1] = 0
        merged = True

  return merged



def move_tiles_left(board):
  """Moves all tiles to the left, merging if possible."""
  moved = False  # Track if any tile moved

  for i in range(4):
    row = board[i]
    merged = [0] * 4  # Keep track of merged tiles
    j = 0  # Position to place the next non-zero tile

    for tile in row:
      if tile != 0:
        if merged[j] == 0:  
          merged[j] = tile
        elif merged[j] == tile:  # Same value, merge
          merged[j] *= 2
          j += 1
          moved = True
        else:  # Different value, move to the next spot
          j += 1
          merged[j] = tile
          moved = True

    board[i] = merged  # Update the row

  return moved

def move_tiles(board, direction):
    """Moves all tiles in the specified direction."""
    if direction == "up":
        new_board = transpose(board.copy())
        new_board = reverse(new_board)  # Reverse rows for upward movement
        moved = move_tiles_left(new_board)
        new_board = reverse(new_board) 
        board[:] = transpose(new_board)
    elif direction == "down":
        new_board = transpose(board.copy()) 
        moved = move_tiles_left(new_board)
        board[:] = transpose(new_board)
    elif direction == "left":
        moved = move_tiles_left(board)
    elif direction == "right":
        new_board = reverse(board.copy())
        moved = move_tiles_left(new_board)
        board[:] = reverse(new_board) 
    else:
        raise ValueError("Invalid direction")

    return moved


def transpose(board):
  """Transposes the board (rows become columns)."""
  return [[board[j][i] for j in range(4)] for i in range(4)]

def reverse(board):
  """Reverses each row of the board."""
  return [row[::-1] for row in board]

# Handle events
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:  # Check for key presses
        if event.key == pygame.K_UP:
            direction = "up"
        elif event.key == pygame.K_DOWN:
            direction = "down"
        elif event.key == pygame.K_LEFT:
            direction = "left"
        elif event.key == pygame.K_RIGHT:
            direction = "right"
        else:
            continue  # Ignore other keys

        # Move and merge tiles
        if move_tiles(board, direction):
            merge_tiles(board, direction) 
            move_tiles(board, direction)  # Move again after merging
            add_new_tile(board)


def add_new_tile(board):
  """Adds a new tile (2 or 4) to a random empty cell."""
  empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
  if empty_cells:
    row, col = random.choice(empty_cells)
    board[row][col] = random.choice([2, 4])


def game_over(board):
  """Checks if the game is over."""

  # Check for any empty cells
  for row in board:
    if 0 in row:
      return False

  # Check for any possible merges
  for i in range(4):
    for j in range(3):  # Check horizontal merges
      if board[i][j] == board[i][j + 1]:
        return False
  for i in range(3):
    for j in range(4):  # Check vertical merges
      if board[i][j] == board[i + 1][j]:
        return False

  return True  # Game over if no empty cells and no possible merges

def main():
  board = initialize_board() # Initialize the boardhere
  while True:
    # Handle events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:  # Check for key presses
        if event.key == pygame.K_UP:
          direction = "up"
        elif event.key == pygame.K_DOWN:
          direction = "down"
        elif event.key == pygame.K_LEFT:
          direction = "left"
        elif event.key == pygame.K_RIGHT:
          direction = "right"
        else:
          continue  # Ignore other keys

        # Move and merge tiles
        if move_tiles(board, direction):
          merge_tiles(board, direction)
          move_tiles(board, direction)  # Move again after merging
          add_new_tile(board)

    # Check for game over
    if game_over(board):
      print("Game Over!")
      break  

    # Draw the board
    draw_board(board)
    pygame.display.flip()



def print_board(board):
  """Prints the board to the console."""
  for row in board:
    print(" ".join(str(tile) for tile in row))
  print()

def draw_board(board):
  """Draws the game board and tiles on the screen."""
  tile_size = 80
  tile_gap = 10

  for i in range(4):
    for j in range(4):
      x = j * (tile_size + tile_gap) + tile_gap
      y = i * (tile_size + tile_gap) + tile_gap

      tile_value = board[i][j]
      tile_color = get_tile_color(tile_value)  

      pygame.draw.rect(screen, tile_color, (x, y, tile_size, tile_size))

      if tile_value != 0:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(str(tile_value), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
        screen.blit(text_surface, text_rect)

def get_tile_color(value):
  """Returns a color based on the tile value."""
  if value == 0:
    return (204, 192, 179)  # Light gray for empty tiles
  elif value == 2:
    return (238, 228, 218)  # Light beige for 2
  elif value == 4:
    return (237, 224, 200)  # Slightly darker beige for 4
  # ... add more colors for higher values
  else:
    return (249, 124, 95)   # Some bright color for high values


if __name__ == "__main__":
  main()
