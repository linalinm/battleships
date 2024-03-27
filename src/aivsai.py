
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
    player1 = AIPlayer(RandomStrategy())
    player2 = AIPlayer(HitStrategy())
    game = Game(player1, player2)
    ui1 = GUI(player1)
    gameloop = asyncio.create_task(game.main())
    uiloop1 = asyncio.create_task(ui1.main())
    while not gameloop.done() or not uiloop1.done():
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())