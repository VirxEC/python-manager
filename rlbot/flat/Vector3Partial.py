# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Vector3Partial(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Vector3Partial()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsVector3Partial(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Vector3Partial
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Vector3Partial
    def X(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Float import Float
            obj = Float()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Vector3Partial
    def Y(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Float import Float
            obj = Float()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Vector3Partial
    def Z(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from rlbot.flat.Float import Float
            obj = Float()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def Vector3PartialStart(builder):
    builder.StartObject(3)

def Start(builder):
    Vector3PartialStart(builder)

def Vector3PartialAddX(builder, x):
    builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(x), 0)

def AddX(builder, x):
    Vector3PartialAddX(builder, x)

def Vector3PartialAddY(builder, y):
    builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(y), 0)

def AddY(builder, y):
    Vector3PartialAddY(builder, y)

def Vector3PartialAddZ(builder, z):
    builder.PrependStructSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(z), 0)

def AddZ(builder, z):
    Vector3PartialAddZ(builder, z)

def Vector3PartialEnd(builder):
    return builder.EndObject()

def End(builder):
    return Vector3PartialEnd(builder)

import rlbot.flat.Float
try:
    from typing import Optional
except:
    pass

class Vector3PartialT(object):

    # Vector3PartialT
    def __init__(self):
        self.x = None  # type: Optional[rlbot.flat.Float.FloatT]
        self.y = None  # type: Optional[rlbot.flat.Float.FloatT]
        self.z = None  # type: Optional[rlbot.flat.Float.FloatT]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        vector3Partial = Vector3Partial()
        vector3Partial.Init(buf, pos)
        return cls.InitFromObj(vector3Partial)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, vector3Partial):
        x = Vector3PartialT()
        x._UnPack(vector3Partial)
        return x

    # Vector3PartialT
    def _UnPack(self, vector3Partial):
        if vector3Partial is None:
            return
        if vector3Partial.X() is not None:
            self.x = rlbot.flat.Float.FloatT.InitFromObj(vector3Partial.X())
        if vector3Partial.Y() is not None:
            self.y = rlbot.flat.Float.FloatT.InitFromObj(vector3Partial.Y())
        if vector3Partial.Z() is not None:
            self.z = rlbot.flat.Float.FloatT.InitFromObj(vector3Partial.Z())

    # Vector3PartialT
    def Pack(self, builder):
        Vector3PartialStart(builder)
        if self.x is not None:
            x = self.x.Pack(builder)
            Vector3PartialAddX(builder, x)
        if self.y is not None:
            y = self.y.Pack(builder)
            Vector3PartialAddY(builder, y)
        if self.z is not None:
            z = self.z.Pack(builder)
            Vector3PartialAddZ(builder, z)
        vector3Partial = Vector3PartialEnd(builder)
        return vector3Partial