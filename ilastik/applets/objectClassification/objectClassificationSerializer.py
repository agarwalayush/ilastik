import warnings

from ilastik.applets.base.appletSerializer import \
  AppletSerializer, SerialSlot, SerialDictSlot, \
  SerialClassifierSlot, SerialListSlot

class SerialDictSlotWithoutDeserialization(SerialDictSlot):
    
    def __init__(self, slot, mainOperator, **kwargs):
        super(SerialDictSlotWithoutDeserialization, self).__init__(slot, **kwargs)
        self.mainOperator = mainOperator
    
    def serialize(self, group):
        #if self.slot.ready() and self.mainOperator._predict_enabled:
        return SerialDictSlot.serialize(self, group)
    
    def deserialize(self, group):
        # Do not deserialize this slot
        pass


class ObjectClassificationSerializer(AppletSerializer):
    # FIXME: predictions can only be saved, not loaded, because it
    # would call setValue() on a connected slot

    def __init__(self, topGroupName, operator):
        serialSlots = [
            SerialDictSlot(operator.SelectedFeatures, transform=str),
            SerialListSlot(operator.LabelNames,
                           transform=str),
            SerialListSlot(operator.LabelColors, transform=lambda x: tuple(x.flat)),
            SerialListSlot(operator.PmapColors, transform=lambda x: tuple(x.flat)),
            SerialDictSlot(operator.LabelInputs, transform=int),
            SerialClassifierSlot(operator.Classifier,
                                 operator.classifier_cache,
                                 name="ClassifierForests",
                                 subname="Forest{:04d}"),
            SerialDictSlot(operator.CachedProbabilities,
                           operator.InputProbabilities,
                           transform=int),
            #SerialDictSlotWithoutDeserialization(operator.Probabilities, operator, transform=str)
        ]

        super(ObjectClassificationSerializer, self ).__init__(topGroupName,
                                                              slots=serialSlots,
                                                              operator=operator)
