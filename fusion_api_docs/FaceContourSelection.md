# FaceContourSelection Object

Derived from: [CurveSelection](CurveSelection.md) Object  

## Description

Represents a face type of curve selection. It allows BRepFace objects for the input geometry. Overrides the GeometrySelection's value method to include other faces if the isSelectingSamePlaneFaces property is true and the selection has been applied. The result of the value property call may contain duplicates.

## Methods

| Name | Description |
|----|----|
| [classType](FaceContourSelection_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [error](FaceContourSelection_error.md) | Gets the last warning string encountered after the selection was applied to a parent. |
| [hasError](FaceContourSelection_hasError.md) | Gets if errors were encountered when applying the selection to a a parent. |
| [hasWarning](FaceContourSelection_hasWarning.md) | Gets if warnings were encountered when applying the selection to a parent. |
| [inputGeometry](FaceContourSelection_inputGeometry.md) | Get or set the value of the input geometry. If the value originates from a component instead of an occurrence, or an occurrence outside of the CAM environment, then the subpath is checked against the CAM model tree. For some child classes, this may be the same as the value property, but might also consist of fewer elements. Valid elements depend on the capabilities of the derived class. An exception is thrown if the matching fails or the given entity does not match the expected type. |
| [isSelectingSamePlaneFaces](FaceContourSelection_isSelectingSamePlaneFaces.md) | Property to get and set if all planar faces lying in the same plane as the selected face should be automatically selected as well. |
| [isValid](FaceContourSelection_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [loopType](FaceContourSelection_loopType.md) | Property to get and set the desired loop type. The default is AllLoops. |
| [objectType](FaceContourSelection_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sideType](FaceContourSelection_sideType.md) | Property to get and set the desired side type. The default is StartOutside. |
| [value](FaceContourSelection_value.md) | Returns the resulting value of the selection. In general, this returns the input selection, but child classes can override the return value if needed. Refer to the child classes comments for further details. The collection may contain duplicates. For OperationInputs, the return value may not be the same as for Operations, as additional geometry selected by child classes is not evaluated for OperationInputs. |
| [warning](FaceContourSelection_warning.md) | Gets the last warning string encountered after the selection was applied to a parent. |

## Accessed From

[CurveSelections.createNewFaceContourSelection](CurveSelections_createNewFaceContourSelection.md)

## Version

Introduced in version April 2023  

