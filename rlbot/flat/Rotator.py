# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# Expresses the rotation state of an object in Euler angles, with values in radians.
class Rotator(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 12

    # Rotator
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Rotator
    def Pitch(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Rotator
    def Yaw(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # Rotator
    def Roll(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))

def CreateRotator(builder, pitch, yaw, roll):
    builder.Prep(4, 12)
    builder.PrependFloat32(roll)
    builder.PrependFloat32(yaw)
    builder.PrependFloat32(pitch)
    return builder.Offset()


class RotatorT(object):

    # RotatorT
    def __init__(self):
        self.pitch = 0.0  # type: float
        self.yaw = 0.0  # type: float
        self.roll = 0.0  # type: float

    @classmethod
    def InitFromBuf(cls, buf, pos):
        rotator = Rotator()
        rotator.Init(buf, pos)
        return cls.InitFromObj(rotator)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, rotator):
        x = RotatorT()
        x._UnPack(rotator)
        return x

    # RotatorT
    def _UnPack(self, rotator):
        if rotator is None:
            return
        self.pitch = rotator.Pitch()
        self.yaw = rotator.Yaw()
        self.roll = rotator.Roll()

    # RotatorT
    def Pack(self, builder):
        return CreateRotator(builder, self.pitch, self.yaw, self.roll)