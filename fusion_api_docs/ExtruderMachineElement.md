
Derived from: [MachineElement](MachineElement.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Machine element representing an extruder on a fused filament fabrication (FFF) machine. A machine can have multiple extruders and thus multiple ExtruderMachineElement elements.

## Methods

| Name | Description |
|----|----|
| [classType](ExtruderMachineElement_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ExtruderMachineElement_deleteMe.md) | Delete this extruder element from the machine. Throws an exception when trying to delete the last remaining element. |
| [staticTypeId](ExtruderMachineElement_staticTypeId.md) | Identifying name for all elements of this type. Pass this to the itemByType or itemById methods of MachineElements to filter to elements of this type. |

## Properties

| Name | Description |
| --- | --- |
| [elementId](ExtruderMachineElement_elementId.md) | Identifier for this element. Unique within an element type. |
| [filamentDiameter](ExtruderMachineElement_filamentDiameter.md) | Filament diameter of this extruder in cm. |
| [isFanAvailable](ExtruderMachineElement_isFanAvailable.md) | Flag indicating if a fan, whose speed is settable in the post, is available. |
| [isValid](ExtruderMachineElement_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ExtruderMachineElement_name.md) | Name of this extruder. Depending on the post, this may be output in the resulting gcode as a comment. |
| [nozzleDiameter](ExtruderMachineElement_nozzleDiameter.md) | Nozzle diameter of this extruder in cm. |
| [objectType](ExtruderMachineElement_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offset](ExtruderMachineElement_offset.md) | Offset relative to the main extruder. The first extruder has an index of 0 and usually an offset of (0,0,0). |
| [temperature](ExtruderMachineElement_temperature.md) | The maximum temperature this extruder can reach in degrees C. |
| [typeId](ExtruderMachineElement_typeId.md) | Identifier for this type of machine element. |
| [volumePerSecond](ExtruderMachineElement_volumePerSecond.md) | The maximum volume output measured in cm^3/s. |

## Version

Introduced in version January 2026  

