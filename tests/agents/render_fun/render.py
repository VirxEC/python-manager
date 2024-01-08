from render_mesh import *

from rlbot.agents import Controller
from rlbot.agents.standalone import StandaloneBot


class Bot(StandaloneBot):
    def initialize_agent(self):
        self.zero_two = unzip_and_build_obj()

    def get_output(self, _):
        # self.zero_two.render(self.renderer)

        return Controller()


if __name__ == "__main__":
    from rlbot.runners.python_bot import run_bot

    run_bot(Bot)
