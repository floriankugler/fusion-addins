
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Settings for multi-axis retract and reconfigure.

## Methods

| Name | Description |
|----|----|
| [classType](MultiAxisRetractAndReconfigureSettings_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MultiAxisRetractAndReconfigureSettings_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MultiAxisRetractAndReconfigureSettings_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [retractPreference](MultiAxisRetractAndReconfigureSettings_retractPreference.md) | The retract preference. See MultiAxisRetractPreference values for more details. |
| [rewindPreference](MultiAxisRetractAndReconfigureSettings_rewindPreference.md) | The rewind preferece. See MultiAxisRewindPreference values for more details. |
| [safePlungeFeedrate](MultiAxisRetractAndReconfigureSettings_safePlungeFeedrate.md) | The safe plunge feedrate for plunge moves. A plunge rate is the speed at which the tool is driven down into the material when starting a cut. It varies depending on the tool and material. Plunging too fast may damage the tip of the cutter. (cm/min) |
| [safeRetractDistance](MultiAxisRetractAndReconfigureSettings_safeRetractDistance.md) | The length of the retract moves along the tool axis, to perform a rewind. |
| [safeRetractFeedrate](MultiAxisRetractAndReconfigureSettings_safeRetractFeedrate.md) | The safe retract feedrate for retract moves. (cm/min) |
| [stockExpansion](MultiAxisRetractAndReconfigureSettings_stockExpansion.md) | Defines the stock expansion for computing retract moves in rewinds. |

## Accessed From

[MultiAxisMachineElement.createRetractAndReconfigureSettings](MultiAxisMachineElement_createRetractAndReconfigureSettings.md), [MultiAxisMachineElement.retractAndReconfigureSettings](MultiAxisMachineElement_retractAndReconfigureSettings.md)

## Version

Introduced in version September 2025  

