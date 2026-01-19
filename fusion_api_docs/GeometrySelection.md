# GeometrySelection Object

Derived from: [Base](Base.md) Object  

## Description

Base parent class for all selection classes. All selections are currently restricted to B-Rep entities or sketches.

## Methods

| Name | Description |
|----|----|
| [classType](GeometrySelection_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [error](GeometrySelection_error.md) | Gets the last warning string encountered after the selection was applied to a parent. |
| [hasError](GeometrySelection_hasError.md) | Gets if errors were encountered when applying the selection to a a parent. |
| [hasWarning](GeometrySelection_hasWarning.md) | Gets if warnings were encountered when applying the selection to a parent. |
| [isValid](GeometrySelection_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](GeometrySelection_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [value](GeometrySelection_value.md) | Returns the resulting value of the selection. In general, this returns the input selection, but child classes can override the return value if needed. Refer to the child classes comments for further details. The collection may contain duplicates. For OperationInputs, the return value may not be the same as for Operations, as additional geometry selected by child classes is not evaluated for OperationInputs. |
| [warning](GeometrySelection_warning.md) | Gets the last warning string encountered after the selection was applied to a parent. |

## Derived Classes

[ArrangeSelection](ArrangeSelection.md), [CurveSelection](CurveSelection.md), [MachineAvoidSelectionBase](MachineAvoidSelectionBase.md)

## Version

Introduced in version April 2023  

