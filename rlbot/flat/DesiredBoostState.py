# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class DesiredBoostState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsDesiredBoostState(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DesiredBoostState()
        x.Init(buf, n + offset)
        return x

    # DesiredBoostState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DesiredBoostState
    def RespawnTime(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from .Float import Float
            obj = Float()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def DesiredBoostStateStart(builder): builder.StartObject(1)
def DesiredBoostStateAddRespawnTime(builder, respawnTime): builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(respawnTime), 0)
def DesiredBoostStateEnd(builder): return builder.EndObject()
