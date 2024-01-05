# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class PredictionSlice(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = PredictionSlice()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsPredictionSlice(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # PredictionSlice
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # The moment in game time that this prediction corresponds to.
    # This corresponds to 'secondsElapsed' in the GameInfo table.
    # PredictionSlice
    def GameSeconds(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # The predicted location and motion of the object.
    # PredictionSlice
    def Physics(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from rlbot.flat.Physics import Physics
            obj = Physics()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def PredictionSliceStart(builder):
    builder.StartObject(2)

def Start(builder):
    PredictionSliceStart(builder)

def PredictionSliceAddGameSeconds(builder, gameSeconds):
    builder.PrependFloat32Slot(0, gameSeconds, 0.0)

def AddGameSeconds(builder, gameSeconds):
    PredictionSliceAddGameSeconds(builder, gameSeconds)

def PredictionSliceAddPhysics(builder, physics):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(physics), 0)

def AddPhysics(builder, physics):
    PredictionSliceAddPhysics(builder, physics)

def PredictionSliceEnd(builder):
    return builder.EndObject()

def End(builder):
    return PredictionSliceEnd(builder)

import rlbot.flat.Physics
try:
    from typing import Optional
except:
    pass

class PredictionSliceT(object):

    # PredictionSliceT
    def __init__(self):
        self.gameSeconds = 0.0  # type: float
        self.physics = None  # type: Optional[rlbot.flat.Physics.PhysicsT]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        predictionSlice = PredictionSlice()
        predictionSlice.Init(buf, pos)
        return cls.InitFromObj(predictionSlice)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, predictionSlice):
        x = PredictionSliceT()
        x._UnPack(predictionSlice)
        return x

    # PredictionSliceT
    def _UnPack(self, predictionSlice):
        if predictionSlice is None:
            return
        self.gameSeconds = predictionSlice.GameSeconds()
        if predictionSlice.Physics() is not None:
            self.physics = rlbot.flat.Physics.PhysicsT.InitFromObj(predictionSlice.Physics())

    # PredictionSliceT
    def Pack(self, builder):
        if self.physics is not None:
            physics = self.physics.Pack(builder)
        PredictionSliceStart(builder)
        PredictionSliceAddGameSeconds(builder, self.gameSeconds)
        if self.physics is not None:
            PredictionSliceAddPhysics(builder, physics)
        predictionSlice = PredictionSliceEnd(builder)
        return predictionSlice