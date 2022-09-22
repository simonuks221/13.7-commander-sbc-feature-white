from typing import Callable
import socketio
from socketio.asyncio_client import AsyncClient

class ControlSocket:
    sio: AsyncClient
    name: str
    address: str
    animations: dict[str, Callable]

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.sio = socketio.AsyncClient()
        self.animations = {}

        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("run", self.on_run)

    def animation(self, func: Callable):
        self.animations[func.__name__] = func
        return func

    async def on_connect(self):
        print("Connected")
        await self.sio.emit('set_identity', self.name)
        await self.sio.emit('set_animations', list(self.animations.keys()))

    async def on_run(self, anim_name):
        if anim_name in self.animations:
            self.animations[anim_name]()

    def run_animation(self, anim_name: str):
        if anim_name not in self.animations:
            raise Exception(f"Animation '{anim_name}' not found")
        self.animations[anim_name]()

    async def on_disconnect(self):
        print("Disconnected")

    async def listen(self):
        await self.sio.connect(self.address, wait_timeout = 10)
        await self.sio.wait()
