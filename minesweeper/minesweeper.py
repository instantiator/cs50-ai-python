import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        new_sentence = Sentence(self.get_neighbours(cell), count)
        # mark the known mines and safes in this sentence
        for mine in self.mines:
            new_sentence.mark_mine(mine)
        for safe in self.safes:
            new_sentence.mark_safe(safe)
        self.knowledge.append(new_sentence)
        # iterate marking mines, safes, and inferring new sentences until there are no more changes
        changes = True
        while changes:
            changes = self.update_safes_and_mines() or self.infer_new_sentences()

    def infer_new_sentences(self):
        changes = False
        # step through each pair of sentences
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2:
                    # if sentence1 is a subset of sentence2 (either way around would have worked...)
                    if sentence1.cells.issubset(sentence2.cells):
                        # create a new sentence, representing the diff of the cells in each
                        # and the remainder of the count (as discussed in the Background)
                        new_sentence = Sentence(
                            sentence2.cells - sentence1.cells,
                            sentence2.count - sentence1.count,
                        )
                        # add the new sentence if it's not already known
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
                            changes = True
        # if we made changes, indicate we should iterate
        return changes

    def get_neighbours(self, cell):
        # neighbours are the 8 cells surrounding the given cell
        neighbours = []
        row, col = cell
        # step through each row and column around the cell
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue
                # the neighbour in question
                n_row = row + r
                n_col = col + c
                neighbour = (n_row, n_col)
                # if the neighbour is in bounds, add it to the list
                if 0 <= n_row < self.height and 0 <= n_col < self.width:
                    neighbours.append(neighbour)
        return neighbours

    def update_safes_and_mines(self):
        changes = False
        # step through each sentence
        for sentence in self.knowledge:
            # get hold of the safes and mines it knows about
            sentence_safes = sentence.known_safes().copy()
            sentence_mines = sentence.known_mines().copy()
            # mark each safe
            for safe in sentence_safes:
                if safe not in self.safes:
                    changes = True
                    self.mark_safe(safe)
            # mark each mine
            for mine in sentence_mines:
                if mine not in self.mines:
                    changes = True
                    self.mark_mine(mine)
        # if we made changes, indicate we should iterate
        return changes

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # just find a safe cell that hasn't been chosen yet
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        # we only get here if there weren't any safe moves to make
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = []
        # step through each cell - if it's not a mine and not already chosen, add it to the list of potential moves
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    moves.append(cell)
        # it would also have been fine to select the first acceptable cell, but the spec says random!
        if len(moves) > 0:
            return random.choice(moves)
        else:
            return None
