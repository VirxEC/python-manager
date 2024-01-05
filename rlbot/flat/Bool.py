# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Bool(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 1

    # Bool
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Bool
    def Val(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))

def CreateBool(builder, val):
    builder.Prep(1, 1)
    builder.PrependBool(val)
    return builder.Offset()


class BoolT(object):

    # BoolT
    def __init__(self):
        self.val = False  # type: bool

    @classmethod
    def InitFromBuf(cls, buf, pos):
        bool = Bool()
        bool.Init(buf, pos)
        return cls.InitFromObj(bool)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, bool):
        x = BoolT()
        x._UnPack(bool)
        return x

    # BoolT
    def _UnPack(self, bool):
        if bool is None:
            return
        self.val = bool.Val()

    # BoolT
    def Pack(self, builder):
        return CreateBool(builder, self.val)