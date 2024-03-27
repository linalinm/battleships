
import asyncio
import json
from exceptions.ExceptionsEnum import ValidationException
from gamedataclasses.AttackResult import AttackResult
from gamedataclasses.Coordinates import Coordinates
from gamedataclasses.CoordinatesValidator import CoordinatesValidator
from entities.ShipValidator import ShipValidator
from entities.Ship import Ship
from players.Player import Player
from exceptions.ExceptionsEnum import *
import websockets

class RemotePlayerServer(Player):

    def __init__(self) -> None:
        super().__init__()
        self._coordval = CoordinatesValidator()
        self._shipval = ShipValidator()
        self.connection = None

    async def connect(self):
        self.running = True
        while self.connection == None:
            self.cont = False
            await websockets.serve(self.handler,"",8764,compression=None)
            while not self.cont:
                await asyncio.sleep(0.1)

    async def send(self, msg : str):
        await self.connection.send(msg)
        return

    def move(self) -> None:
        self.turn = True
        asyncio.get_running_loop().create_task(self.wait_for_action())

    def place(self, ship_type: str) -> None:
        self.placem = True
        self.ship_to_place = ship_type
        asyncio.get_running_loop().create_task(self.wait_for_action())

    def add_enemy_ship(self, ship: Ship, coord : Coordinates, vertical : bool):
        super().add_enemy_ship(ship)
        asyncio.get_running_loop().create_task(self.send(json.dumps({"reason":"placem","placem":self.place_to_json_obj(ship,coord,vertical)})))
        self.wait_for_response()

    def remove_enemy_ship(self, id: int):
        super().remove_enemy_ship(id)

    def process_attack(self, coord: Coordinates) -> AttackResult:
        super().process_attack(coord)
        asyncio.get_running_loop().create_task(self.send(json.dumps({"reason":"attack","coords":self.coords_to_json_obj(coord)})))
        return self.wait_for_response()

    def wait_for_response(self):
        self.tmp = None
        while self.tmp == None:
            continue
        tmp = self.tmp
        self.tmp = None
        return tmp

    async def wait_for_action(self):
        self.cont = False
        while not self.cont:
            await asyncio.sleep(0.1)

    def to_ship(self, ship : dict) -> Ship:
        return Ship(ship["id"],ship["type"])

    def ship_to_json_obj(self, ship : Ship) -> dict:
        return {"id":ship.id,"type":ship.ship_type}

    def to_attack_result(self, result : dict) -> AttackResult:
        return AttackResult(self.to_coordinates(result["coords"]),result["tile_hit"],result["sunk_ship_id"],result["sunk_ship_type"])

    def result_to_json_obj(self, result : AttackResult) -> dict:
        return {"coords":self.coords_to_json_obj(result.coords),"tile_hit":result.tile,"sunk_ship_id":result.get_sunk_ship(),"sunk_ship_type":result.get_sunk_ship_type()}

    def to_placement(self, placement : dict):
        return self.to_ship(placement["ship"]), self.to_coordinates(placement["coords"]), placement["rotation"]

    def place_to_json_obj(self, ship : Ship, location : Coordinates, vertical : bool) -> dict:
        return {"ship":self.ship_to_json_obj(ship),"coords":self.coords_to_json_obj(location),"rotation":vertical}

    def coords_to_json_obj(self, coords : Coordinates) -> dict:
        return {"x":coords.x,"y":coords.y}

    def to_coordinates(self, coords : dict):
        return Coordinates(coords["x"],coords["y"])

    async def handler(self, websocket : websockets):
        while self.running:
            try:
                msg = await websocket.recv()
            except websockets.ConnectionClosedOK:
                raise ConnectionException("Connection closed by peer.")
            self.cont = True
            msg_obj = json.loads(msg)
            if "reason" not in msg_obj:
                return
            if self.connection == None:
                if msg_obj["reason"] != "init":
                    return
                self.connection = websocket
                await websocket.send(json.dumps({"reason":"confirmation"}))
                return
            if self.connection != websocket:
                return
            if self.turn:
                if msg_obj["reason"] != "attack" or "coords" not in msg_obj:
                    return
                coords = self.to_coordinates(msg_obj["coords"])
                try:
                    self._coordval.validate(coords)
                except ValidationException:
                    return
                result = self.attack(coords)
                await websocket.send(json.dumps({"reason":"result","result":self.result_to_json_obj(result)}))
                return
            if self.placem:
                if msg_obj["reason"] != "placem" or "placem" not in msg_obj:
                    return
                ship,coords,vertical = self.to_placement(msg_obj["placem"])
                try:
                    self._shipval.validate(ship)
                    self._coordval.validate(coords)
                except ValidationException:
                    return
                self.place_ship(ship,coords,vertical)
                await websocket.send(json.dumps({"reason":"placement_confirmation"}))
                return
            if msg_obj["reason"] == "result":
                self.tmp = self.to_attack_result(msg_obj["result"])
                return
            if msg_obj["reason"] == "placement_confirmation":
                self.tmp = True
                return
        
        


        