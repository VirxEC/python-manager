# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# Rigid body state for a player / car in the game. Includes the latest
# controller input, which is otherwise difficult to correlate with consequences.
class PlayerRigidBodyState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = PlayerRigidBodyState()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsPlayerRigidBodyState(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # PlayerRigidBodyState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # PlayerRigidBodyState
    def State(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from rlbot.flat.RigidBodyState import RigidBodyState
            obj = RigidBodyState()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # PlayerRigidBodyState
    def Input(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from rlbot.flat.ControllerState import ControllerState
            obj = ControllerState()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def PlayerRigidBodyStateStart(builder):
    builder.StartObject(2)

def Start(builder):
    PlayerRigidBodyStateStart(builder)

def PlayerRigidBodyStateAddState(builder, state):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(state), 0)

def AddState(builder, state):
    PlayerRigidBodyStateAddState(builder, state)

def PlayerRigidBodyStateAddInput(builder, input):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(input), 0)

def AddInput(builder, input):
    PlayerRigidBodyStateAddInput(builder, input)

def PlayerRigidBodyStateEnd(builder):
    return builder.EndObject()

def End(builder):
    return PlayerRigidBodyStateEnd(builder)

import rlbot.flat.ControllerState
import rlbot.flat.RigidBodyState
try:
    from typing import Optional
except:
    pass

class PlayerRigidBodyStateT(object):

    # PlayerRigidBodyStateT
    def __init__(self):
        self.state = None  # type: Optional[rlbot.flat.RigidBodyState.RigidBodyStateT]
        self.input = None  # type: Optional[rlbot.flat.ControllerState.ControllerStateT]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        playerRigidBodyState = PlayerRigidBodyState()
        playerRigidBodyState.Init(buf, pos)
        return cls.InitFromObj(playerRigidBodyState)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, playerRigidBodyState):
        x = PlayerRigidBodyStateT()
        x._UnPack(playerRigidBodyState)
        return x

    # PlayerRigidBodyStateT
    def _UnPack(self, playerRigidBodyState):
        if playerRigidBodyState is None:
            return
        if playerRigidBodyState.State() is not None:
            self.state = rlbot.flat.RigidBodyState.RigidBodyStateT.InitFromObj(playerRigidBodyState.State())
        if playerRigidBodyState.Input() is not None:
            self.input = rlbot.flat.ControllerState.ControllerStateT.InitFromObj(playerRigidBodyState.Input())

    # PlayerRigidBodyStateT
    def Pack(self, builder):
        if self.state is not None:
            state = self.state.Pack(builder)
        if self.input is not None:
            input = self.input.Pack(builder)
        PlayerRigidBodyStateStart(builder)
        if self.state is not None:
            PlayerRigidBodyStateAddState(builder, state)
        if self.input is not None:
            PlayerRigidBodyStateAddInput(builder, input)
        playerRigidBodyState = PlayerRigidBodyStateEnd(builder)
        return playerRigidBodyState
