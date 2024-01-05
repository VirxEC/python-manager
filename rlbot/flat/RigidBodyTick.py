# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# Contains all rigid body state information.
class RigidBodyTick(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = RigidBodyTick()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsRigidBodyTick(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # RigidBodyTick
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # RigidBodyTick
    def Ball(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from rlbot.flat.BallRigidBodyState import BallRigidBodyState
            obj = BallRigidBodyState()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # RigidBodyTick
    def Players(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from rlbot.flat.PlayerRigidBodyState import PlayerRigidBodyState
            obj = PlayerRigidBodyState()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # RigidBodyTick
    def PlayersLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # RigidBodyTick
    def PlayersIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def RigidBodyTickStart(builder):
    builder.StartObject(2)

def Start(builder):
    RigidBodyTickStart(builder)

def RigidBodyTickAddBall(builder, ball):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(ball), 0)

def AddBall(builder, ball):
    RigidBodyTickAddBall(builder, ball)

def RigidBodyTickAddPlayers(builder, players):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(players), 0)

def AddPlayers(builder, players):
    RigidBodyTickAddPlayers(builder, players)

def RigidBodyTickStartPlayersVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartPlayersVector(builder, numElems):
    return RigidBodyTickStartPlayersVector(builder, numElems)

def RigidBodyTickEnd(builder):
    return builder.EndObject()

def End(builder):
    return RigidBodyTickEnd(builder)

import rlbot.flat.BallRigidBodyState
import rlbot.flat.PlayerRigidBodyState
try:
    from typing import List, Optional
except:
    pass

class RigidBodyTickT(object):

    # RigidBodyTickT
    def __init__(self):
        self.ball = None  # type: Optional[rlbot.flat.BallRigidBodyState.BallRigidBodyStateT]
        self.players = None  # type: List[rlbot.flat.PlayerRigidBodyState.PlayerRigidBodyStateT]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        rigidBodyTick = RigidBodyTick()
        rigidBodyTick.Init(buf, pos)
        return cls.InitFromObj(rigidBodyTick)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, rigidBodyTick):
        x = RigidBodyTickT()
        x._UnPack(rigidBodyTick)
        return x

    # RigidBodyTickT
    def _UnPack(self, rigidBodyTick):
        if rigidBodyTick is None:
            return
        if rigidBodyTick.Ball() is not None:
            self.ball = rlbot.flat.BallRigidBodyState.BallRigidBodyStateT.InitFromObj(rigidBodyTick.Ball())
        if not rigidBodyTick.PlayersIsNone():
            self.players = []
            for i in range(rigidBodyTick.PlayersLength()):
                if rigidBodyTick.Players(i) is None:
                    self.players.append(None)
                else:
                    playerRigidBodyState_ = rlbot.flat.PlayerRigidBodyState.PlayerRigidBodyStateT.InitFromObj(rigidBodyTick.Players(i))
                    self.players.append(playerRigidBodyState_)

    # RigidBodyTickT
    def Pack(self, builder):
        if self.ball is not None:
            ball = self.ball.Pack(builder)
        if self.players is not None:
            playerslist = []
            for i in range(len(self.players)):
                playerslist.append(self.players[i].Pack(builder))
            RigidBodyTickStartPlayersVector(builder, len(self.players))
            for i in reversed(range(len(self.players))):
                builder.PrependUOffsetTRelative(playerslist[i])
            players = builder.EndVector()
        RigidBodyTickStart(builder)
        if self.ball is not None:
            RigidBodyTickAddBall(builder, ball)
        if self.players is not None:
            RigidBodyTickAddPlayers(builder, players)
        rigidBodyTick = RigidBodyTickEnd(builder)
        return rigidBodyTick