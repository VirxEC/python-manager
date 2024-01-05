# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# Notification when the local player is spectating another player.
class PlayerSpectate(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = PlayerSpectate()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsPlayerSpectate(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # PlayerSpectate
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # index of the player that is being spectated. Will be -1 if not spectating anyone.
    # PlayerSpectate
    def PlayerIndex(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def PlayerSpectateStart(builder):
    builder.StartObject(1)

def Start(builder):
    PlayerSpectateStart(builder)

def PlayerSpectateAddPlayerIndex(builder, playerIndex):
    builder.PrependInt32Slot(0, playerIndex, 0)

def AddPlayerIndex(builder, playerIndex):
    PlayerSpectateAddPlayerIndex(builder, playerIndex)

def PlayerSpectateEnd(builder):
    return builder.EndObject()

def End(builder):
    return PlayerSpectateEnd(builder)


class PlayerSpectateT(object):

    # PlayerSpectateT
    def __init__(self):
        self.playerIndex = 0  # type: int

    @classmethod
    def InitFromBuf(cls, buf, pos):
        playerSpectate = PlayerSpectate()
        playerSpectate.Init(buf, pos)
        return cls.InitFromObj(playerSpectate)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, playerSpectate):
        x = PlayerSpectateT()
        x._UnPack(playerSpectate)
        return x

    # PlayerSpectateT
    def _UnPack(self, playerSpectate):
        if playerSpectate is None:
            return
        self.playerIndex = playerSpectate.PlayerIndex()

    # PlayerSpectateT
    def Pack(self, builder):
        PlayerSpectateStart(builder)
        PlayerSpectateAddPlayerIndex(builder, self.playerIndex)
        playerSpectate = PlayerSpectateEnd(builder)
        return playerSpectate
