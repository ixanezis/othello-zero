import subprocess
from subprocess import PIPE, STDOUT, Popen

import config
from util import line_2_plane, log, plane_2_line

import numpy as np


class EdaxPlayer:
    def __init__(self, level):
        edax_exec = config.edax_path + " -q -eval-file " + config.edax_eval_path + " -book-file " + config.edax_book_path + " --level " + str(level)
        self.edax = Popen(edax_exec, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        self.read_stdout()

    def make_move(self, current_node):
        if current_node.move == config.pass_move:
            self.write_stdin("pass")
        else:
            self.write_stdin(line_2_plane(current_node.move))
        self.read_stdout()

        self.write_stdin("go")
        edax_move_plane = self.read_stdout().split("plays ")[-1][:2]
        if edax_move_plane == "PS":
            return config.pass_move
        else:
            return plane_2_line(edax_move_plane)

    def write_stdin(self, command):
        self.edax.stdin.write(str.encode(command + "\n"))
        self.edax.stdin.flush()

    def read_stdout(self):
        out = b''
        while True:
            next_b = self.edax.stdout.read(1)
            if next_b == b'>' and ((len(out) > 0 and out[-1] == 10) or len(out) == 0):
                break
            else:
                out += next_b
        return out.decode("utf-8")

    def close(self):
        self.edax.terminate()


class AlphaBetaPlayer:
    def __init__(self):
        self.player = Popen(config.alpha_beta_path, shell=True, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.DEVNULL)

    def make_move(self, current_node):
        def fill_board(board, bits, value):
            for i, v in enumerate(reversed('{{:0>{}}}'.format(config.N ** 2).format(bin(bits)[2:]))):
                if v == "1":
                    x = i % config.N
                    y = i // config.N
                    board[y][x] = value

        board = np.zeros((config.N, config.N), dtype=np.int)
        fill_board(board, current_node.board.black, 1)
        fill_board(board, current_node.board.white, 2)

        board_string = "\n".join(" ".join(map(str, row)) for row in board) \
            + "\n" + str(1 if current_node.player == config.black else 2) + "\n"

        self.player.stdin.write(board_string)
        self.player.stdin.flush()

        out = self.player.stdout.readline()

        if out.strip() == "pass":
            return config.pass_move

        return plane_2_line(out)


class HumanPlayer:
    def make_move(self, current_node):
        human_input = -1
        while True:
            human_input_str = input(">")
            if human_input_str == "pass":
                human_input = config.pass_move
            else:
                human_input = plane_2_line(human_input_str)

            if human_input is None or current_node.legal_moves[human_input] == 0:
                print("illegal.")
            else:
                return human_input
