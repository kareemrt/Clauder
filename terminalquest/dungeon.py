"""Procedural dungeon generation using room-and-corridor placement with Bresenham LOS FOV."""

import math
import random
from typing import Dict, List, Optional, Set, Tuple

TILE_WALL = "#"
TILE_FLOOR = "."
TILE_STAIRS_DOWN = ">"
TILE_STAIRS_UP = "<"

MAP_WIDTH = 90
MAP_HEIGHT = 32


class Rect:
    """Axis-aligned rectangular room."""

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def x2(self) -> int:
        return self.x + self.w

    @property
    def y2(self) -> int:
        return self.y + self.h

    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)

    def inner_points(self) -> List[Tuple[int, int]]:
        return [
            (x, y)
            for y in range(self.y + 1, self.y2 - 1)
            for x in range(self.x + 1, self.x2 - 1)
        ]

    def intersects(self, other: "Rect") -> bool:
        return (
            self.x <= other.x2
            and self.x2 >= other.x
            and self.y <= other.y2
            and self.y2 >= other.y
        )


class Dungeon:
    """A procedurally generated dungeon floor."""

    def __init__(
        self, width: int = MAP_WIDTH, height: int = MAP_HEIGHT, level: int = 1
    ):
        self.width = width
        self.height = height
        self.level = level
        self.tiles = [[TILE_WALL] * width for _ in range(height)]
        self.rooms: List[Rect] = []
        self.revealed = [[False] * width for _ in range(height)]
        self.visible = [[False] * width for _ in range(height)]
        self.item_map: Dict[Tuple[int, int], object] = {}
        self.enemy_map: Dict[Tuple[int, int], object] = {}
        self.stairs_up: Optional[Tuple[int, int]] = None
        self.stairs_down: Optional[Tuple[int, int]] = None
        self._generate()

    # ------------------------------------------------------------------ #
    # Generation
    # ------------------------------------------------------------------ #

    def _generate(self) -> None:
        max_rooms = 8 + min(self.level, 4)
        min_room, max_room = 5, 12

        for _ in range(max_rooms * 6):
            if len(self.rooms) >= max_rooms:
                break
            w = random.randint(min_room, max_room)
            h = random.randint(min_room - 2, max_room - 2)
            x = random.randint(1, self.width - w - 2)
            y = random.randint(1, self.height - h - 2)
            room = Rect(x, y, w, h)
            # Keep a one-tile gap between rooms
            padded = Rect(x - 1, y - 1, w + 2, h + 2)
            if not any(padded.intersects(r) for r in self.rooms):
                self._carve_room(room)
                if self.rooms:
                    self._connect_rooms(self.rooms[-1], room)
                self.rooms.append(room)

        if len(self.rooms) >= 2:
            cx, cy = self.rooms[0].center
            self.tiles[cy][cx] = TILE_STAIRS_UP
            self.stairs_up = (cx, cy)

            cx, cy = self.rooms[-1].center
            self.tiles[cy][cx] = TILE_STAIRS_DOWN
            self.stairs_down = (cx, cy)

    def _carve_room(self, room: Rect) -> None:
        for y in range(room.y + 1, room.y2 - 1):
            for x in range(room.x + 1, room.x2 - 1):
                self.tiles[y][x] = TILE_FLOOR

    def _connect_rooms(self, r1: Rect, r2: Rect) -> None:
        cx1, cy1 = r1.center
        cx2, cy2 = r2.center
        if random.random() < 0.5:
            self._h_tunnel(cx1, cx2, cy1)
            self._v_tunnel(cy1, cy2, cx2)
        else:
            self._v_tunnel(cy1, cy2, cx1)
            self._h_tunnel(cx1, cx2, cy2)

    def _h_tunnel(self, x1: int, x2: int, y: int) -> None:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= y < self.height and 0 <= x < self.width:
                self.tiles[y][x] = TILE_FLOOR

    def _v_tunnel(self, y1: int, y2: int, x: int) -> None:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= y < self.height and 0 <= x < self.width:
                self.tiles[y][x] = TILE_FLOOR

    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #

    def is_walkable(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.width
            and 0 <= y < self.height
            and self.tiles[y][x] != TILE_WALL
        )

    def compute_fov(self, px: int, py: int, radius: int = 9) -> None:
        """Shadowcast FOV using 360-angle Bresenham ray sweep."""
        for row in self.visible:
            row[:] = [False] * self.width

        self.visible[py][px] = True
        self.revealed[py][px] = True

        # Cast a ray at each integer angle degree around the player
        for deg in range(360):
            rad = deg * math.pi / 180
            dx_f = math.cos(rad)
            dy_f = math.sin(rad)
            rx, ry = float(px), float(py)
            for _ in range(radius + 1):
                ix, iy = int(rx + 0.5), int(ry + 0.5)
                if not (0 <= ix < self.width and 0 <= iy < self.height):
                    break
                self.visible[iy][ix] = True
                self.revealed[iy][ix] = True
                if self.tiles[iy][ix] == TILE_WALL:
                    break
                rx += dx_f
                ry += dy_f

    def get_random_floor_pos(
        self,
        room: Optional[Rect] = None,
        exclude: Optional[Set[Tuple[int, int]]] = None,
    ) -> Optional[Tuple[int, int]]:
        if exclude is None:
            exclude = set()
        if room is None:
            room = random.choice(self.rooms) if self.rooms else None
        if room is None:
            return None
        candidates = [
            (x, y)
            for x, y in room.inner_points()
            if self.tiles[y][x] == TILE_FLOOR and (x, y) not in exclude
        ]
        return random.choice(candidates) if candidates else None
