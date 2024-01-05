# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class PlayerInput(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = PlayerInput()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsPlayerInput(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # PlayerInput
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # PlayerInput
    def PlayerIndex(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerInput
    def ControllerState(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from rlbot.flat.ControllerState import ControllerState
            obj = ControllerState()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def PlayerInputStart(builder):
    builder.StartObject(2)

def Start(builder):
    PlayerInputStart(builder)

def PlayerInputAddPlayerIndex(builder, playerIndex):
    builder.PrependInt32Slot(0, playerIndex, 0)

def AddPlayerIndex(builder, playerIndex):
    PlayerInputAddPlayerIndex(builder, playerIndex)

def PlayerInputAddControllerState(builder, controllerState):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(controllerState), 0)

def AddControllerState(builder, controllerState):
    PlayerInputAddControllerState(builder, controllerState)

def PlayerInputEnd(builder):
    return builder.EndObject()

def End(builder):
    return PlayerInputEnd(builder)

import rlbot.flat.ControllerState
try:
    from typing import Optional
except:
    pass

class PlayerInputT(object):

    # PlayerInputT
    def __init__(self):
        self.playerIndex = 0  # type: int
        self.controllerState = None  # type: Optional[rlbot.flat.ControllerState.ControllerStateT]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        playerInput = PlayerInput()
        playerInput.Init(buf, pos)
        return cls.InitFromObj(playerInput)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, playerInput):
        x = PlayerInputT()
        x._UnPack(playerInput)
        return x

    # PlayerInputT
    def _UnPack(self, playerInput):
        if playerInput is None:
            return
        self.playerIndex = playerInput.PlayerIndex()
        if playerInput.ControllerState() is not None:
            self.controllerState = rlbot.flat.ControllerState.ControllerStateT.InitFromObj(playerInput.ControllerState())

    # PlayerInputT
    def Pack(self, builder):
        if self.controllerState is not None:
            controllerState = self.controllerState.Pack(builder)
        PlayerInputStart(builder)
        PlayerInputAddPlayerIndex(builder, self.playerIndex)
        if self.controllerState is not None:
            PlayerInputAddControllerState(builder, controllerState)
        playerInput = PlayerInputEnd(builder)
        return playerInput
