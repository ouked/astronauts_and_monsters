# Display mode. If 'emoji' is true, display in the console will use emojis, instead of the ASCII representation.
from enum import Enum

emoji = False
icon = {
    "m": '👩🏼‍🚀',
    "c": '👺',
    "s": '🌊',
    "b": '🛶',
    "l": '⬅️',
    "r": '➡️',
} if emoji else {
    "m": 'M',
    "c": 'C',
    "s": '~',
    "b": '#',
    "l": "<-",
    "r": "->",
}


# Class to represent moving m Missionaries and c Cannibals in the given direction
class Action:
    def __init__(self, direction, m, c):
        if type(direction) is str:
            direction = direction.upper()
            if direction in ['L', 'R']:
                self.left = direction == 'L'
            else:
                raise ValueError(f"Invalid direction: {direction}")
        else:
            self.left = bool(direction)

        # Set properties of Action
        self.right = not self.left
        self.missionaries = m
        self.cannibals = c

    # region Override inbuilt functions
    def __repr__(self):
        return f"[" \
               f"{icon['l' if self.left else 'r']} " \
               f"{icon['m'] * self.missionaries}" \
               f"{icon['c'] * self.cannibals}" \
               f"]"

    # Required for "if <action> in list<action>"
    def __eq__(self, other):
        return self.left == other.left and self.missionaries == self.missionaries and self.cannibals == self.cannibals
    # endregion


class Node:

    def __init__(self, m, c, b=1, parent=None, game=None, action=None):
        self.game = parent.game if not game else game

        self.action = action

        self.parent = parent

        team_size = self.game.team_size

        self.left = {
            "m": m,
            "c": c,
            "b": (b == 1)
        }

        self.right = {
            "m": team_size - self.left["m"],
            "c": team_size - self.left["c"],
            "b": (not self.left["b"])
        }

        self.is_goal_state = (self.left["m"] == 0) and \
                             (self.left["c"] == 0)
        self.is_valid_state = (self.left["m"] >= self.left["c"] or self.left["m"] == 0) and \
                              (self.right["m"] >= self.right["c"] or self.right["m"] == 0)

    def get_child_node(self, action):

        direction = (-1 if action.right else 1)

        d_m = action.missionaries * direction
        d_c = action.cannibals * direction

        new_m = self.left["m"] + d_m
        new_c = self.left["c"] + d_c

        new_b = direction

        return Node(m=new_m, c=new_c, b=new_b, parent=self, action=action)

    def possible_actions(self):
        # Array to store possible actions
        actions = []

        # Boat's capacity
        capacity = self.game.boat_capacity

        left = not self.left["b"]
        origin = self.right if left else self.left

        # Produces all combinations of m and c (MM, MC, CC)
        for m in range(min(origin["m"], capacity) + 1):
            for c in range(min(origin["c"], capacity) + 1):

                # Check if valid combination (Not empty, and not exceeding boat)
                if m + c > capacity or m == c == 0:
                    continue
                # Cast direction from boolean to "L" or "R"

                # Action to try
                action = Action(left, m, c)

                # Resulting node after running action
                node = self.get_child_node(action)

                # Check if the new node is in a valid state. If it is, add it to array
                if node.is_valid_state:
                    actions.append(action)
                else:
                    pass
        return actions

    # region Override inbuilt functions
    def __repr__(self):
        # line_width = (self.game.team_size * 4) + 2
        # right_width = self.left['c'] + self.left['m'] + int(self.left['b'])
        return f"{' ' * 0}" \
               f"{icon['c'] * self.left['c']}" \
               f"{icon['m'] * self.left['m']}" \
               f"{icon['b'] if self.left['b'] else ''}" \
               f" {icon['s'] * 3} " \
               f"{icon['b'] if self.right['b'] else ''}" \
               f"{icon['m'] * self.right['m']}" \
               f"{icon['c'] * self.right['c']}"

    def __eq__(self, other):
        return str(self) == str(other)
    # endregion


class Game:
    def __init__(self, boat_capacity=2, team_size=3):
        self.boat_capacity = boat_capacity
        self.team_size = team_size
        self.initial_node = Node(m=3, c=3, b=1, game=self)

    def search(self, type="dfs"):
        if type.upper() == "DFS":
            print("Depth First Search")

            def pop_frontier():
                return frontier.pop()
        else:
            print("Breadth First Search")

            def pop_frontier():
                return frontier.pop(0)

        frontier = [self.initial_node]
        explored = []
        generated = 0

        current_state = pop_frontier()
        while not current_state.is_goal_state:
            explored.append(current_state)
            actions = current_state.possible_actions()
            for action in actions:
                generated += 1
                new_state = current_state.get_child_node(action)
                if new_state not in explored and new_state not in frontier:
                    frontier.append(new_state)

            if len(frontier) == 0:
                print("No solution found...")
                return

            current_state = pop_frontier()
        print("Solution found!")
        print(f"Explored {len(explored)} states")
        print(f"Generated {generated} states")
        print()

        final_path = []
        while current_state.parent is not None:
            final_path.append(current_state)
            current_state = current_state.parent

        final_path.append(current_state)

        for state in reversed(final_path):
            if state.action is not None:
                print(state.action)
            print(state)
        print(f"Total {len(final_path) - 1} steps\n")

    def possible_actions(self):
        return self.state.possible_actions()


def main():
    g = Game()
    g.search("bfs")
    g.search("dfs")

    # Run demo code? Shows optimal solution.
    run_demo = True
    if run_demo:
        s = Node(3, 3, 1, game=g)

        # Optimal Solution
        actions = [
            Action(False, 1, 1),
            Action(True, 1, 0),
            Action(False, 0, 2),
            Action("L", 0, 1),
            Action("R", 2, 0),
            Action("L", 1, 1),
            Action("R", 2, 0),
            Action("L", 0, 1),
            Action("R", 0, 2),
            Action("L", 1, 0),
            Action("R", 1, 1)
        ]

        # Run all actions in optimal solution
        for a in actions:
            print(s, "Valid:", s.is_valid_state, "Goal:", s.is_goal_state)
            poss = s.possible_actions()
            if a not in poss:
                print(f"{a} not in possible actions")
            s = s.get_child_node(a)

        print(s, "Valid:", s.is_valid_state, "Goal:", s.is_goal_state)


if __name__ == "__main__":
    main()
