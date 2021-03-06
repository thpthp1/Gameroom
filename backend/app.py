from flask import Flask, request, jsonify
import json
from .mock_models import *
import random
import datetime

app = Flask(__name__)


@app.route("/api/player/create", methods=["POST"])
def create_player():
    player_id = random.randint(1, 100)
    player = Player(player_id, random.randint(RATING_MIN, RATING_MAX),
                    username='Randomplayer{}'.format(player_id), password="rando{}".format(player_id))
    return _serialize(player)


@app.route("/api/player/list", methods=["GET"])
def list_players():
    return _serialize(list(Player._mem.values()))


@app.route("/api/room/create", methods=["POST"])
def create_room():
    players = request.get_json().get('players')
    print(players)
    room_id = random.randint(1, 100)
    room = Room(room_id, datetime.datetime.now(),
                type_=room_id, players=players)
    return _serialize(room)


@app.route("/api/server/match", methods=["POST"])
def match_room():
    print(request.json)
    player_id = request.get_json().get('player')
    # rooms = _serialize(Room._mem.values())
    # appendedRoom = None
    # for x in range (0, len(rooms)):
    #     if rooms[x] == room:
    #         continue
    #     if rooms[x].append(room) is not None:
    #         appendedRoom = rooms[x].append(room)
    #         break
    # if appendedRoom is not None:
    #     return _serialize(appendedRoom)
    # Create room with player in it
    room_id = random.randint(1, 100)
    single_room = Room(room_id, datetime.datetime.now(),
                       type_=room_id, players=[player_id])
    for room in Room._mem.values():
        if room == single_room:
            continue
        if len(room.players) < room.cap:
            room.append(single_room)
            print(single_room)
            print(room)
            del single_room
            return _serialize(room)


def _serialize(obj):
    return json.dumps(obj, default=obj_to_dict)


@app.route("/api/room/<int:room_id>", methods=["GET"])
def room_info(room_id):
    return _serialize(Room._mem[room_id])


@app.route("/api/player/<int:player_id>", methods=["GET"])
def player_info(player_id):
    return _serialize(Player._mem[player_id])


@app.route("/api/player/<int:player_id>/update-rating", methods=["POST"])
def update_rating(player_id):
    toxic = request.get_json().get('toxic')
    skill = request.get_json().get('skill')
    player = Player._mem[player_id]
    player.rating.updateRating(toxic, skill)
    return _serialize(player)
