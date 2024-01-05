# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class FieldInfo(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FieldInfo()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsFieldInfo(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # FieldInfo
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FieldInfo
    def BoostPads(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from rlbot.flat.BoostPad import BoostPad
            obj = BoostPad()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FieldInfo
    def BoostPadsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # FieldInfo
    def BoostPadsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # FieldInfo
    def Goals(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from rlbot.flat.GoalInfo import GoalInfo
            obj = GoalInfo()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FieldInfo
    def GoalsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # FieldInfo
    def GoalsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def FieldInfoStart(builder):
    builder.StartObject(2)

def Start(builder):
    FieldInfoStart(builder)

def FieldInfoAddBoostPads(builder, boostPads):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(boostPads), 0)

def AddBoostPads(builder, boostPads):
    FieldInfoAddBoostPads(builder, boostPads)

def FieldInfoStartBoostPadsVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartBoostPadsVector(builder, numElems):
    return FieldInfoStartBoostPadsVector(builder, numElems)

def FieldInfoAddGoals(builder, goals):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(goals), 0)

def AddGoals(builder, goals):
    FieldInfoAddGoals(builder, goals)

def FieldInfoStartGoalsVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartGoalsVector(builder, numElems):
    return FieldInfoStartGoalsVector(builder, numElems)

def FieldInfoEnd(builder):
    return builder.EndObject()

def End(builder):
    return FieldInfoEnd(builder)

import rlbot.flat.BoostPad
import rlbot.flat.GoalInfo
try:
    from typing import List
except:
    pass

class FieldInfoT(object):

    # FieldInfoT
    def __init__(self):
        self.boostPads = None  # type: List[rlbot.flat.BoostPad.BoostPadT]
        self.goals = None  # type: List[rlbot.flat.GoalInfo.GoalInfoT]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        fieldInfo = FieldInfo()
        fieldInfo.Init(buf, pos)
        return cls.InitFromObj(fieldInfo)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, fieldInfo):
        x = FieldInfoT()
        x._UnPack(fieldInfo)
        return x

    # FieldInfoT
    def _UnPack(self, fieldInfo):
        if fieldInfo is None:
            return
        if not fieldInfo.BoostPadsIsNone():
            self.boostPads = []
            for i in range(fieldInfo.BoostPadsLength()):
                if fieldInfo.BoostPads(i) is None:
                    self.boostPads.append(None)
                else:
                    boostPad_ = rlbot.flat.BoostPad.BoostPadT.InitFromObj(fieldInfo.BoostPads(i))
                    self.boostPads.append(boostPad_)
        if not fieldInfo.GoalsIsNone():
            self.goals = []
            for i in range(fieldInfo.GoalsLength()):
                if fieldInfo.Goals(i) is None:
                    self.goals.append(None)
                else:
                    goalInfo_ = rlbot.flat.GoalInfo.GoalInfoT.InitFromObj(fieldInfo.Goals(i))
                    self.goals.append(goalInfo_)

    # FieldInfoT
    def Pack(self, builder):
        if self.boostPads is not None:
            boostPadslist = []
            for i in range(len(self.boostPads)):
                boostPadslist.append(self.boostPads[i].Pack(builder))
            FieldInfoStartBoostPadsVector(builder, len(self.boostPads))
            for i in reversed(range(len(self.boostPads))):
                builder.PrependUOffsetTRelative(boostPadslist[i])
            boostPads = builder.EndVector()
        if self.goals is not None:
            goalslist = []
            for i in range(len(self.goals)):
                goalslist.append(self.goals[i].Pack(builder))
            FieldInfoStartGoalsVector(builder, len(self.goals))
            for i in reversed(range(len(self.goals))):
                builder.PrependUOffsetTRelative(goalslist[i])
            goals = builder.EndVector()
        FieldInfoStart(builder)
        if self.boostPads is not None:
            FieldInfoAddBoostPads(builder, boostPads)
        if self.goals is not None:
            FieldInfoAddGoals(builder, goals)
        fieldInfo = FieldInfoEnd(builder)
        return fieldInfo
