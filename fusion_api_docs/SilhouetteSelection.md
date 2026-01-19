# SilhouetteSelection Object

Derived from: [CurveSelection](CurveSelection.md) Object  

## Description

Represents a silhouette type of curve selection. Allows BRepBody selections for the input geometry. Overrides the GeometrySelection's the value property to include setup bodies if isSetupModelSelected is set to true and the selection has been applied. The results may contain duplicates.

## Methods

| Name | Description |
|----|----|
| [classType](SilhouetteSelection_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [error](SilhouetteSelection_error.md) | Gets the last warning string encountered after the selection was applied to a parent. |
| [hasError](SilhouetteSelection_hasError.md) | Gets if errors were encountered when applying the selection to a a parent. |
| [hasWarning](SilhouetteSelection_hasWarning.md) | Gets if warnings were encountered when applying the selection to a parent. |
| [inputGeometry](SilhouetteSelection_inputGeometry.md) | Get or set the value of the input geometry. If the value originates from a component instead of an occurrence, or an occurrence outside of the CAM environment, then the subpath is checked against the CAM model tree. For some child classes, this may be the same as the value property, but might also consist of fewer elements. Valid elements depend on the capabilities of the derived class. An exception is thrown if the matching fails or the given entity does not match the expected type. |
| [isSetupModelSelected](SilhouetteSelection_isSetupModelSelected.md) | Flag to include all B-Rep bodies set as the setup models. |
| [isValid](SilhouetteSelection_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [loopType](SilhouetteSelection_loopType.md) | Desired loop type. The default is AllLoops. |
| [objectType](SilhouetteSelection_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sideType](SilhouetteSelection_sideType.md) | Desired side type. The default is StartOutside. |
| [silhouetteTolerance](SilhouetteSelection_silhouetteTolerance.md) | The distance the silhouette can differ from the model. This helps in creating a silhouette in situations where one cannot be created because of open contours.Generally, the tolerance value you use should be smaller than or equal to the machining tolerance. |
| [value](SilhouetteSelection_value.md) | Returns the resulting value of the selection. In general, this returns the input selection, but child classes can override the return value if needed. Refer to the child classes comments for further details. The collection may contain duplicates. For OperationInputs, the return value may not be the same as for Operations, as additional geometry selected by child classes is not evaluated for OperationInputs. |
| [warning](SilhouetteSelection_warning.md) | Gets the last warning string encountered after the selection was applied to a parent. |

## Accessed From

[CurveSelections.createNewSilhouetteSelection](CurveSelections_createNewSilhouetteSelection.md)

## Version

Introduced in version April 2023  

