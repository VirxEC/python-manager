# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# A minimal version of player data, useful when bandwidth needs to be conserved.
class TinyPlayer(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = TinyPlayer()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsTinyPlayer(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # TinyPlayer
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # TinyPlayer
    def Location(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # TinyPlayer
    def Rotation(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Rotator import Rotator
            obj = Rotator()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # TinyPlayer
    def Velocity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # TinyPlayer
    def HasWheelContact(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # TinyPlayer
    def IsSupersonic(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # TinyPlayer
    def Team(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # TinyPlayer
    def Boost(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def TinyPlayerStart(builder):
    builder.StartObject(7)

def Start(builder):
    TinyPlayerStart(builder)

def TinyPlayerAddLocation(builder, location):
    builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(location), 0)

def AddLocation(builder, location):
    TinyPlayerAddLocation(builder, location)

def TinyPlayerAddRotation(builder, rotation):
    builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(rotation), 0)

def AddRotation(builder, rotation):
    TinyPlayerAddRotation(builder, rotation)

def TinyPlayerAddVelocity(builder, velocity):
    builder.PrependStructSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(velocity), 0)

def AddVelocity(builder, velocity):
    TinyPlayerAddVelocity(builder, velocity)

def TinyPlayerAddHasWheelContact(builder, hasWheelContact):
    builder.PrependBoolSlot(3, hasWheelContact, 0)

def AddHasWheelContact(builder, hasWheelContact):
    TinyPlayerAddHasWheelContact(builder, hasWheelContact)

def TinyPlayerAddIsSupersonic(builder, isSupersonic):
    builder.PrependBoolSlot(4, isSupersonic, 0)

def AddIsSupersonic(builder, isSupersonic):
    TinyPlayerAddIsSupersonic(builder, isSupersonic)

def TinyPlayerAddTeam(builder, team):
    builder.PrependInt32Slot(5, team, 0)

def AddTeam(builder, team):
    TinyPlayerAddTeam(builder, team)

def TinyPlayerAddBoost(builder, boost):
    builder.PrependInt32Slot(6, boost, 0)

def AddBoost(builder, boost):
    TinyPlayerAddBoost(builder, boost)

def TinyPlayerEnd(builder):
    return builder.EndObject()

def End(builder):
    return TinyPlayerEnd(builder)

import rlbot.flat.Rotator
import rlbot.flat.Vector3
try:
    from typing import Optional
except:
    pass

class TinyPlayerT(object):

    # TinyPlayerT
    def __init__(self):
        self.location = None  # type: Optional[rlbot.flat.Vector3.Vector3T]
        self.rotation = None  # type: Optional[rlbot.flat.Rotator.RotatorT]
        self.velocity = None  # type: Optional[rlbot.flat.Vector3.Vector3T]
        self.hasWheelContact = False  # type: bool
        self.isSupersonic = False  # type: bool
        self.team = 0  # type: int
        self.boost = 0  # type: int

    @classmethod
    def InitFromBuf(cls, buf, pos):
        tinyPlayer = TinyPlayer()
        tinyPlayer.Init(buf, pos)
        return cls.InitFromObj(tinyPlayer)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, tinyPlayer):
        x = TinyPlayerT()
        x._UnPack(tinyPlayer)
        return x

    # TinyPlayerT
    def _UnPack(self, tinyPlayer):
        if tinyPlayer is None:
            return
        if tinyPlayer.Location() is not None:
            self.location = rlbot.flat.Vector3.Vector3T.InitFromObj(tinyPlayer.Location())
        if tinyPlayer.Rotation() is not None:
            self.rotation = rlbot.flat.Rotator.RotatorT.InitFromObj(tinyPlayer.Rotation())
        if tinyPlayer.Velocity() is not None:
            self.velocity = rlbot.flat.Vector3.Vector3T.InitFromObj(tinyPlayer.Velocity())
        self.hasWheelContact = tinyPlayer.HasWheelContact()
        self.isSupersonic = tinyPlayer.IsSupersonic()
        self.team = tinyPlayer.Team()
        self.boost = tinyPlayer.Boost()

    # TinyPlayerT
    def Pack(self, builder):
        TinyPlayerStart(builder)
        if self.location is not None:
            location = self.location.Pack(builder)
            TinyPlayerAddLocation(builder, location)
        if self.rotation is not None:
            rotation = self.rotation.Pack(builder)
            TinyPlayerAddRotation(builder, rotation)
        if self.velocity is not None:
            velocity = self.velocity.Pack(builder)
            TinyPlayerAddVelocity(builder, velocity)
        TinyPlayerAddHasWheelContact(builder, self.hasWheelContact)
        TinyPlayerAddIsSupersonic(builder, self.isSupersonic)
        TinyPlayerAddTeam(builder, self.team)
        TinyPlayerAddBoost(builder, self.boost)
        tinyPlayer = TinyPlayerEnd(builder)
        return tinyPlayer