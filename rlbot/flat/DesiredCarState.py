# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class DesiredCarState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsDesiredCarState(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DesiredCarState()
        x.Init(buf, n + offset)
        return x

    # DesiredCarState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DesiredCarState
    def Physics(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .DesiredPhysics import DesiredPhysics
            obj = DesiredPhysics()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DesiredCarState
    def BoostAmount(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from .Float import Float
            obj = Float()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DesiredCarState
    def Jumped(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from .Bool import Bool
            obj = Bool()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DesiredCarState
    def DoubleJumped(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from .Bool import Bool
            obj = Bool()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def DesiredCarStateStart(builder): builder.StartObject(4)
def DesiredCarStateAddPhysics(builder, physics): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(physics), 0)
def DesiredCarStateAddBoostAmount(builder, boostAmount): builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(boostAmount), 0)
def DesiredCarStateAddJumped(builder, jumped): builder.PrependStructSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(jumped), 0)
def DesiredCarStateAddDoubleJumped(builder, doubleJumped): builder.PrependStructSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(doubleJumped), 0)
def DesiredCarStateEnd(builder): return builder.EndObject()
