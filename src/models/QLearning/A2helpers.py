# COMP 4900C Fall 2023 Assignment 2
# Carleton University
# NOTE: We provide some helper functions here. 
#       See the A2 instructions for more information.
import numpy as np
from scipy.linalg import block_diag
import matplotlib
from matplotlib import pyplot as plt
import gymnasium as gym
from gymnasium.error import DependencyNotInstalled


class GridWorld(gym.Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 20}

    def __init__(self, render_mode=None, init_state=None, goal=None):

        if not hasattr(self, 'layout'):
            raise ValueError("Need layout in subclass")

        # Parse the layout
        layout_lines = self.layout.splitlines()
        self._occupancy = np.array([list(map(lambda c: 1 if c == 'w' else 0, line))
                                    for line in layout_lines])

        # From any state the agent can perform one of four actions, up, down, left or right
        self._n_actions = 4
        self._n_states = int(np.sum(self._occupancy == 0))
        self._directions = [np.array((-1, 0)), 
                            np.array((1, 0)), 
                            np.array((0, -1)), 
                            np.array((0, 1))]

        self._to_state = {}  # maps (x, y) to state #
        state_num = 0
        self._limits = [len(layout_lines), len(layout_lines[0])]
        for i in range(self._limits[0]):
            for j in range(self._limits[1]):
                if self._occupancy[i, j] == 0:
                    self._to_state[(i, j)] = state_num
                    state_num += 1
        self._to_cell = {v: k for k, v in self._to_state.items()}  # maps state # to (x, y)

        self._goal = goal

        if init_state is None:
            self._init_states = list(range(self._n_states))
            self._init_states = np.delete(self._init_states, goal)  # remove goal
        else:
            assert init_state != goal
            self._init_states = [init_state]

        self._current_cell = None

        self.window_cell_size = 50  # The length of a cell in the PyGame window
        self.window_size = np.array(self._limits) * self.window_cell_size

        # Standard Gym interface
        self.observation_space = gym.spaces.Box(low=0, 
                                                high=self.n_states-1, 
                                                dtype=int)  # cell index
        self.action_space = gym.spaces.Discrete(self.n_actions)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None  # window we draw to
        self.clock = None  # control framerate

    def reset(self, init_state=None):

        if init_state is not None:
            # assert init_state in self._init_states
            state = init_state
        else:
            state = np.random.choice(self._init_states)
        self._current_cell = self._to_cell[state]

        if self.render_mode == "human":
            self.render()

        return state, {}

    def step(self, action):
        """
        The agent can perform one of four actions:
                             up, down, left or right
        If the movement would take the agent into a wall
        then the agent remains in the same cell.

        We consider a case in which reward is 1 when reach the goal and 0 everywhere else.
        """

        next_cell = tuple(self._current_cell + self._directions[action])

        if not self._occupancy[next_cell]:
            self._current_cell = next_cell

        state = self._to_state[self._current_cell]

        terminated = state == self._goal
        reward = 1 if terminated else 0.

        if self.render_mode == "human":
            self.render()

        return state, reward, terminated, False, {}

    def render(self):

        # PyGame has a different coordinate system (flip)
        try:
            import pygame
        except ImportError as e:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install gymnasium[classic-control]`"
            ) from e
        
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(np.flip(self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface(np.flip(self.window_size))
        canvas.fill((255, 255, 255))

        # First we draw the goal
        pygame.draw.rect(
            canvas,
            (255, 0, 0),
            pygame.Rect(
                self.window_cell_size * np.flip(self._to_cell[self.goal]),
                (self.window_cell_size, self.window_cell_size),
            ),
        )

        # Draw the walls
        for i in range(self._limits[0]):
            for j in range(self._limits[1]):
                if self._occupancy[i, j]:
                    pygame.draw.rect(
                        canvas,
                        0,
                        pygame.Rect(
                            (j * self.window_cell_size, i * self.window_cell_size),
                            (self.window_cell_size, self.window_cell_size),
                        ),
                    )

        # Draw the agent
        pygame.draw.circle(
            canvas,
            (0, 0, 255),
            (np.flip(self._current_cell) + 0.5) * self.window_cell_size,
            self.window_cell_size / 3,
        )

        # Finally, add some gridlines
        for i in range(self._limits[0]):
            pygame.draw.line(
                canvas,
                0,
                (0, self.window_cell_size * i),
                (self.window_size[1], self.window_cell_size * i),
                width=3,
            )
        for i in range(self._limits[1]):
            pygame.draw.line(
                canvas,
                0,
                (self.window_cell_size * i, 0),
                (self.window_cell_size * i, self.window_size[0]),
                width=3,
            )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            import pygame
            pygame.display.quit()
            pygame.quit()

    @property
    def n_actions(self):
        return self._n_actions

    @property
    def n_states(self):
        return self._n_states

    @property
    def goal(self):
        return self._goal

    @property
    def to_cell(self):
        return self._to_cell


class FourRoom(GridWorld):

    def __init__(self, render_mode=None, init_state=None, goal=None):

        self.layout = """\
wwwwwwwwwwwww
w     w     w
w     w     w
w           w
w     w     w
w     w     w
ww wwww     w
w     www www
w     w     w
w     w     w
w           w
w     w     w
wwwwwwwwwwwww
"""
        super().__init__(render_mode=render_mode,
                         init_state=init_state, 
                         goal=goal)


def diagonalization(A, n_states, n_actions):
    """
        Input A is a matrix of shape (n_states, n_actions), OR a column vector
        of shape (n_states * n_actions, 1).
        This function returns the diagonalization of A. The resultant matrix
        is a block-diagonal matrix of shape (n_states, n_states * n_actions) 
        such that each row has at most n_actions non-zero elements.
    """
    A = A.reshape([n_states, n_actions])
    return block_diag(*list(A))


def deDiagonalization(A):
    """
        Reverse of diagonalization. It converts a block-diagona lmatrix of 
        shape (n_states, n_states * n_actions) into a matrix of shape
        (n_states, n_actions).
    """
    n_states = A.shape[0]
    n_actions = A.shape[1] // n_states
    a = [A[i, i*n_actions:(i+1)*n_actions] for i in range(n_states)]
    return np.array(a)


# Ploting helpers below
def func_to_vectorize(x, y, dx, dy, color, scalarMap, scaling=0.3):

    if dx != 0 or dy != 0:

        arrow_color = scalarMap.to_rgba(color)
        plt.arrow(x, y,
                  dx * scaling, dy * scaling,
                  color=arrow_color,
                  head_width=0.15, head_length=0.15)


def convert_grid_to_numpy(grid):

    mappings = {'w': 1.,
                ' ': 0}

    grid = grid.split('\n')
    grid = list(filter(lambda x: len(x) > 0, grid))
    m, n = len(grid), len(grid[0])

    matrix = np.zeros([m, n])
    for i in range(m):
        for j in range(n):
            matrix[i, j] = mappings[grid[i][j]]

    return matrix


def plot_policy(env, xv, yv, xdir, ydir, policy, action):

    xdir = np.zeros_like(xdir)
    ydir = np.zeros_like(ydir)
    arrow_colors = np.zeros_like(xdir)

    cNorm = matplotlib.colors.Normalize(vmin=0., vmax=1.)
    scalarMap = matplotlib.cm.ScalarMappable(norm=cNorm, cmap='gray_r')
    for s in range(env.n_states):

        x, y = env.to_cell[s]
        if action == 0:
            ydir[x, y] = -policy[s, action]
        elif action == 1:
            ydir[x, y] = policy[s, action]
        elif action == 2:
            xdir[x, y] = -policy[s, action]
        else:
            xdir[x, y] = policy[s, action]
        arrow_colors[x, y] = policy[s, action]

    vectorized_arrow_drawing = np.vectorize(func_to_vectorize)
    vectorized_arrow_drawing(xv, yv, xdir, ydir, arrow_colors, scalarMap)
    return xdir, ydir


def plot_grid_world(env, Pi, q):

    n_states = env.n_states

    matrix = convert_grid_to_numpy(env.layout)

    v = np.amax(q.reshape([env.n_states, env.n_actions]), axis=1)
    v = 0.5 * (v - np.amin(v)) / (np.amax(v) - np.amin(v))
    for s in range(n_states):
        x, y = env.to_cell[s]
        matrix[x, y] = v[s]

    policy = deDiagonalization(Pi)

    m, n = matrix.shape
    xv, yv = np.meshgrid(np.arange(0.5, 0.5 + n), np.arange(0.5, 0.5 + m))
    xdir = np.zeros_like(matrix)
    ydir = np.zeros_like(matrix)

    plt.figure(figsize=(9, 9))

    plt.pcolormesh(matrix, edgecolors='k', linewidth=0.5, cmap='hot_r')
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.invert_yaxis()

    plot_policy(env, xv, yv, xdir, ydir, policy, 0)
    plot_policy(env, xv, yv, xdir, ydir, policy, 1)
    plot_policy(env, xv, yv, xdir, ydir, policy, 2)
    plot_policy(env, xv, yv, xdir, ydir, policy, 3)

    plt.xticks([])
    plt.yticks([])
    plt.show()
