import os
import re
import sys
from time import sleep

import openai
from adventure import load_advent_dat
from adventure.game import Game

openai.api_key = os.getenv("OPENAI_API_KEY")

WORDS_RE = re.compile(r"\w+")

# This code was copied from adventure.__main__. I can't just import it because that module imports
# readline, which isn't in my environment due to (I think) pyenv compilation options.
BAUD = 1200


def baudout(s):
    out = sys.stdout
    for c in s:
        sleep(9.0 / BAUD)  # 8 bits + 1 stop bit @ the given baud rate
        out.write(c)
        out.flush()
# end of copied code


class GptPlayer:
    def __init__(self) -> None:
        self.prompts = []
        self.responses = []
        self.llm_prompt = ""

    def _append_prompt(self, prompt: str) -> None:
        self.prompts.append(prompt)
        self.llm_prompt += prompt + "> "

    def _append_response(self, response: str) -> None:
        self.responses.append(response)
        self.llm_prompt += response + "\n\n"

    def _get_llm_prompt(self) -> str:
        return self.llm_prompt

    def get_response(self, prompt: str) -> str:
        self._append_prompt(prompt)
        completion = openai.Completion.create(
            model="text-davinci-003",  # not actually GPT. TODO: change class name
            prompt=self._get_llm_prompt(),
            max_tokens=4,
        )
        response = completion.choices[0].text
        # response cannot contain "\n"
        response = response.split("\n", maxsplit=1)[0]
        self._append_response(response)
        return response


def main() -> None:
    """Have text-davinci play Adventure"""
    game = Game()
    load_advent_dat(game)
    game.start()

    gpt_player = GptPlayer()

    baudout(game.output)
    while not game.is_finished:
        baudout("> ")
        sleep(0.1)
        response = gpt_player.get_response(game.output)
        baudout(f"{response}\n\n")
        response_words = WORDS_RE.findall(response.lower())
        baudout(game.do_command(response_words))


if __name__ == "__main__":
    main()
