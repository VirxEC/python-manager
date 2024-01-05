# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# The state of a rigid body in Rocket League's physics engine.
# This gets updated in time with the physics tick, not the rendering framerate.
# The frame field will be incremented every time the physics engine ticks.
class RigidBodyState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = RigidBodyState()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsRigidBodyState(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # RigidBodyState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # RigidBodyState
    def Frame(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # RigidBodyState
    def Location(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # RigidBodyState
    def Rotation(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Quaternion import Quaternion
            obj = Quaternion()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # RigidBodyState
    def Velocity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # RigidBodyState
    def AngularVelocity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def RigidBodyStateStart(builder):
    builder.StartObject(5)

def Start(builder):
    RigidBodyStateStart(builder)

def RigidBodyStateAddFrame(builder, frame):
    builder.PrependInt32Slot(0, frame, 0)

def AddFrame(builder, frame):
    RigidBodyStateAddFrame(builder, frame)

def RigidBodyStateAddLocation(builder, location):
    builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(location), 0)

def AddLocation(builder, location):
    RigidBodyStateAddLocation(builder, location)

def RigidBodyStateAddRotation(builder, rotation):
    builder.PrependStructSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(rotation), 0)

def AddRotation(builder, rotation):
    RigidBodyStateAddRotation(builder, rotation)

def RigidBodyStateAddVelocity(builder, velocity):
    builder.PrependStructSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(velocity), 0)

def AddVelocity(builder, velocity):
    RigidBodyStateAddVelocity(builder, velocity)

def RigidBodyStateAddAngularVelocity(builder, angularVelocity):
    builder.PrependStructSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(angularVelocity), 0)

def AddAngularVelocity(builder, angularVelocity):
    RigidBodyStateAddAngularVelocity(builder, angularVelocity)

def RigidBodyStateEnd(builder):
    return builder.EndObject()

def End(builder):
    return RigidBodyStateEnd(builder)

import rlbot.flat.Quaternion
import rlbot.flat.Vector3
try:
    from typing import Optional
except:
    pass

class RigidBodyStateT(object):

    # RigidBodyStateT
    def __init__(self):
        self.frame = 0  # type: int
        self.location = None  # type: Optional[rlbot.flat.Vector3.Vector3T]
        self.rotation = None  # type: Optional[rlbot.flat.Quaternion.QuaternionT]
        self.velocity = None  # type: Optional[rlbot.flat.Vector3.Vector3T]
        self.angularVelocity = None  # type: Optional[rlbot.flat.Vector3.Vector3T]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        rigidBodyState = RigidBodyState()
        rigidBodyState.Init(buf, pos)
        return cls.InitFromObj(rigidBodyState)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, rigidBodyState):
        x = RigidBodyStateT()
        x._UnPack(rigidBodyState)
        return x

    # RigidBodyStateT
    def _UnPack(self, rigidBodyState):
        if rigidBodyState is None:
            return
        self.frame = rigidBodyState.Frame()
        if rigidBodyState.Location() is not None:
            self.location = rlbot.flat.Vector3.Vector3T.InitFromObj(rigidBodyState.Location())
        if rigidBodyState.Rotation() is not None:
            self.rotation = rlbot.flat.Quaternion.QuaternionT.InitFromObj(rigidBodyState.Rotation())
        if rigidBodyState.Velocity() is not None:
            self.velocity = rlbot.flat.Vector3.Vector3T.InitFromObj(rigidBodyState.Velocity())
        if rigidBodyState.AngularVelocity() is not None:
            self.angularVelocity = rlbot.flat.Vector3.Vector3T.InitFromObj(rigidBodyState.AngularVelocity())

    # RigidBodyStateT
    def Pack(self, builder):
        RigidBodyStateStart(builder)
        RigidBodyStateAddFrame(builder, self.frame)
        if self.location is not None:
            location = self.location.Pack(builder)
            RigidBodyStateAddLocation(builder, location)
        if self.rotation is not None:
            rotation = self.rotation.Pack(builder)
            RigidBodyStateAddRotation(builder, rotation)
        if self.velocity is not None:
            velocity = self.velocity.Pack(builder)
            RigidBodyStateAddVelocity(builder, velocity)
        if self.angularVelocity is not None:
            angularVelocity = self.angularVelocity.Pack(builder)
            RigidBodyStateAddAngularVelocity(builder, angularVelocity)
        rigidBodyState = RigidBodyStateEnd(builder)
        return rigidBodyState