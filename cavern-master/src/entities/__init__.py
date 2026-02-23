"""
entities/__init__.py — Re-exports all entity classes for convenient importing.

Usage:
    from src.entities import Player, Robot, Orb, Bolt, Fruit, Pop
"""

from src.entities.base import CollideActor, GravityActor
from src.entities.bolt import Bolt
from src.entities.fruit import Fruit
from src.entities.orb import Orb
from src.entities.player import Player
from src.entities.pop import Pop
from src.entities.robot import Robot

__all__ = [
    "CollideActor",
    "GravityActor",
    "Pop",
    "Bolt",
    "Orb",
    "Fruit",
    "Player",
    "Robot",
]