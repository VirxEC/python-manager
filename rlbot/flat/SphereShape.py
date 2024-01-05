# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class SphereShape(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = SphereShape()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsSphereShape(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # SphereShape
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # SphereShape
    def Diameter(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def SphereShapeStart(builder):
    builder.StartObject(1)

def Start(builder):
    SphereShapeStart(builder)

def SphereShapeAddDiameter(builder, diameter):
    builder.PrependFloat32Slot(0, diameter, 0.0)

def AddDiameter(builder, diameter):
    SphereShapeAddDiameter(builder, diameter)

def SphereShapeEnd(builder):
    return builder.EndObject()

def End(builder):
    return SphereShapeEnd(builder)


class SphereShapeT(object):

    # SphereShapeT
    def __init__(self):
        self.diameter = 0.0  # type: float

    @classmethod
    def InitFromBuf(cls, buf, pos):
        sphereShape = SphereShape()
        sphereShape.Init(buf, pos)
        return cls.InitFromObj(sphereShape)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, sphereShape):
        x = SphereShapeT()
        x._UnPack(sphereShape)
        return x

    # SphereShapeT
    def _UnPack(self, sphereShape):
        if sphereShape is None:
            return
        self.diameter = sphereShape.Diameter()

    # SphereShapeT
    def Pack(self, builder):
        SphereShapeStart(builder)
        SphereShapeAddDiameter(builder, self.diameter)
        sphereShape = SphereShapeEnd(builder)
        return sphereShape