# MachineToolStation Object

Derived from: [Base](Base.md) Object  

## Description

Object representing a tool station on the machine

## Methods

| Name | Description |
|----|----|
| [classType](MachineToolStation_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [coolants](MachineToolStation_coolants.md) | The coolants that this tool station can use. See MachineToolStationCoolant for possible values. |
| [isValid](MachineToolStation_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maxToolDiameter](MachineToolStation_maxToolDiameter.md) | The maximum diameter in cm of the tool that can be held by this tool station. |
| [maxToolLength](MachineToolStation_maxToolLength.md) | The maximum length in cm of the tool that can be held by this tool station. |
| [objectType](MachineToolStation_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [toolInterface](MachineToolStation_toolInterface.md) | The type of interface that this tool station uses. (e.g. BT40, CAPTO C5, HSK A100, SK50, etc.) Note: All newline characters will be removed, and if the string contains only ASCII characters, it will be converted to uppercase. |

## Accessed From

[MachinePart.toolStation](MachinePart_toolStation.md)

## Version

Introduced in version July 2025  

