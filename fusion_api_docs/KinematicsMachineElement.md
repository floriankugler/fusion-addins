# KinematicsMachineElement Object

Derived from: [MachineElement](MachineElement.md) Object  

## Description

Machine element representing the machine's kinematics tree.

## Methods

| Name | Description |
|----|----|
| [classType](KinematicsMachineElement_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [staticTypeId](KinematicsMachineElement_staticTypeId.md) | Identifying name for all elements of this type. Pass this to the itemByType or itemById methods of MachineElements to filter to elements of this type. |

## Properties

| Name | Description |
| --- | --- |
| [elementId](KinematicsMachineElement_elementId.md) | Identifier for this element. Unique within an element type. |
| [isValid](KinematicsMachineElement_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](KinematicsMachineElement_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parts](KinematicsMachineElement_parts.md) | Get the root parts collection. |
| [typeId](KinematicsMachineElement_typeId.md) | Identifier for this type of machine element. |

## Version

Introduced in version April 2023  

