# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Color(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Color()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsColor(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Color
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Color
    def A(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Color
    def R(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Color
    def G(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Color
    def B(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

def ColorStart(builder):
    builder.StartObject(4)

def Start(builder):
    ColorStart(builder)

def ColorAddA(builder, a):
    builder.PrependUint8Slot(0, a, 0)

def AddA(builder, a):
    ColorAddA(builder, a)

def ColorAddR(builder, r):
    builder.PrependUint8Slot(1, r, 0)

def AddR(builder, r):
    ColorAddR(builder, r)

def ColorAddG(builder, g):
    builder.PrependUint8Slot(2, g, 0)

def AddG(builder, g):
    ColorAddG(builder, g)

def ColorAddB(builder, b):
    builder.PrependUint8Slot(3, b, 0)

def AddB(builder, b):
    ColorAddB(builder, b)

def ColorEnd(builder):
    return builder.EndObject()

def End(builder):
    return ColorEnd(builder)


class ColorT(object):

    # ColorT
    def __init__(self):
        self.a = 0  # type: int
        self.r = 0  # type: int
        self.g = 0  # type: int
        self.b = 0  # type: int

    @classmethod
    def InitFromBuf(cls, buf, pos):
        color = Color()
        color.Init(buf, pos)
        return cls.InitFromObj(color)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, color):
        x = ColorT()
        x._UnPack(color)
        return x

    # ColorT
    def _UnPack(self, color):
        if color is None:
            return
        self.a = color.A()
        self.r = color.R()
        self.g = color.G()
        self.b = color.B()

    # ColorT
    def Pack(self, builder):
        ColorStart(builder)
        ColorAddA(builder, self.a)
        ColorAddR(builder, self.r)
        ColorAddG(builder, self.g)
        ColorAddB(builder, self.b)
        color = ColorEnd(builder)
        return color
