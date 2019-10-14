class Human:
  def __init__(self):
    pass

  def set_symbol(self, player_number):
    self.player_number = player_number

  def take_action(self, env):
    while True:
      # break if we make a legal move
      move = input("Enter coordinates i,j for your next move (i,j=0..2): ")
      i, j = move.split(',')
      i = int(i)
      j = int(j)
      if env.is_empty(i, j):
        env.board[i, j] = 1 if self.player_number == 'x' else 2
        break

  def update(self, env):
    pass

  def update_state_values(self, s):
    pass

  def update_state_history(self, env):
      pass