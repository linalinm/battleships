



import asyncio
from players.Player import Player
from players.AIPlayer import AIPlayer
from players.RemotePlayerClient import RemotePlayerClient
from players.RemotePlayerServer import RemotePlayerServer
from service.Game import Game
from strategies.HitStrategy import HitStrategy
from strategies.RandomStrategy import RandomStrategy
from ui.ConsoleUI import ConsoleUI
from ui.GUI import GUI
from ui.MainMenu import MainMenu


async def main():
    menu = MainMenu()
    state = menu.main()
    player1 = Player()
    if state == "easy":
        player2 = AIPlayer(RandomStrategy())
    elif state == "normal":
        player2 = AIPlayer(HitStrategy())
    elif state == "host":
        player2 = RemotePlayerServer()
        await player2.connect()
    elif state.startswith("connect"):
        player2 = RemotePlayerClient(state.split(" ")[1])
        clientloop = asyncio.create_task(player2.client())
    else:
        return
    game = Game(player1, player2)
    ui = GUI(player1)
    gameloop = asyncio.create_task(game.main())
    uiloop = asyncio.create_task(ui.main())
    while not gameloop.done() or not uiloop.done():
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())

