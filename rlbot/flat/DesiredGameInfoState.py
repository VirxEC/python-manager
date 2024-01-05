# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class DesiredGameInfoState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DesiredGameInfoState()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsDesiredGameInfoState(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # DesiredGameInfoState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DesiredGameInfoState
    def WorldGravityZ(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Float import Float
            obj = Float()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DesiredGameInfoState
    def GameSpeed(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Float import Float
            obj = Float()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DesiredGameInfoState
    def Paused(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Bool import Bool
            obj = Bool()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DesiredGameInfoState
    def EndMatch(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Bool import Bool
            obj = Bool()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def DesiredGameInfoStateStart(builder):
    builder.StartObject(4)

def Start(builder):
    DesiredGameInfoStateStart(builder)

def DesiredGameInfoStateAddWorldGravityZ(builder, worldGravityZ):
    builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(worldGravityZ), 0)

def AddWorldGravityZ(builder, worldGravityZ):
    DesiredGameInfoStateAddWorldGravityZ(builder, worldGravityZ)

def DesiredGameInfoStateAddGameSpeed(builder, gameSpeed):
    builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(gameSpeed), 0)

def AddGameSpeed(builder, gameSpeed):
    DesiredGameInfoStateAddGameSpeed(builder, gameSpeed)

def DesiredGameInfoStateAddPaused(builder, paused):
    builder.PrependStructSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(paused), 0)

def AddPaused(builder, paused):
    DesiredGameInfoStateAddPaused(builder, paused)

def DesiredGameInfoStateAddEndMatch(builder, endMatch):
    builder.PrependStructSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(endMatch), 0)

def AddEndMatch(builder, endMatch):
    DesiredGameInfoStateAddEndMatch(builder, endMatch)

def DesiredGameInfoStateEnd(builder):
    return builder.EndObject()

def End(builder):
    return DesiredGameInfoStateEnd(builder)

import rlbot.flat.Bool
import rlbot.flat.Float
try:
    from typing import Optional
except:
    pass

class DesiredGameInfoStateT(object):

    # DesiredGameInfoStateT
    def __init__(self):
        self.worldGravityZ = None  # type: Optional[rlbot.flat.Float.FloatT]
        self.gameSpeed = None  # type: Optional[rlbot.flat.Float.FloatT]
        self.paused = None  # type: Optional[rlbot.flat.Bool.BoolT]
        self.endMatch = None  # type: Optional[rlbot.flat.Bool.BoolT]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        desiredGameInfoState = DesiredGameInfoState()
        desiredGameInfoState.Init(buf, pos)
        return cls.InitFromObj(desiredGameInfoState)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, desiredGameInfoState):
        x = DesiredGameInfoStateT()
        x._UnPack(desiredGameInfoState)
        return x

    # DesiredGameInfoStateT
    def _UnPack(self, desiredGameInfoState):
        if desiredGameInfoState is None:
            return
        if desiredGameInfoState.WorldGravityZ() is not None:
            self.worldGravityZ = rlbot.flat.Float.FloatT.InitFromObj(desiredGameInfoState.WorldGravityZ())
        if desiredGameInfoState.GameSpeed() is not None:
            self.gameSpeed = rlbot.flat.Float.FloatT.InitFromObj(desiredGameInfoState.GameSpeed())
        if desiredGameInfoState.Paused() is not None:
            self.paused = rlbot.flat.Bool.BoolT.InitFromObj(desiredGameInfoState.Paused())
        if desiredGameInfoState.EndMatch() is not None:
            self.endMatch = rlbot.flat.Bool.BoolT.InitFromObj(desiredGameInfoState.EndMatch())

    # DesiredGameInfoStateT
    def Pack(self, builder):
        DesiredGameInfoStateStart(builder)
        if self.worldGravityZ is not None:
            worldGravityZ = self.worldGravityZ.Pack(builder)
            DesiredGameInfoStateAddWorldGravityZ(builder, worldGravityZ)
        if self.gameSpeed is not None:
            gameSpeed = self.gameSpeed.Pack(builder)
            DesiredGameInfoStateAddGameSpeed(builder, gameSpeed)
        if self.paused is not None:
            paused = self.paused.Pack(builder)
            DesiredGameInfoStateAddPaused(builder, paused)
        if self.endMatch is not None:
            endMatch = self.endMatch.Pack(builder)
            DesiredGameInfoStateAddEndMatch(builder, endMatch)
        desiredGameInfoState = DesiredGameInfoStateEnd(builder)
        return desiredGameInfoState