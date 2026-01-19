# Arrange2DDefinition Object

Derived from: [ArrangeDefinition](ArrangeDefinition.md) Object  

## Description

This object defines all of the settings associated with a 2D arrangement. This is used for both rectangular and true shape arrangements, but some properties are ignored in some cases.

## Methods

| Name | Description |
|----|----|
| [classType](Arrange2DDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [globalQuantity](Arrange2DDefinition_globalQuantity.md) | Returns the parameter that controls the global quantity. You can modify the value by using the properties on the returned ModelParameter object. |
| [globalRotation](Arrange2DDefinition_globalRotation.md) | Gets and sets the global rotation type. |
| [grainDirection](Arrange2DDefinition_grainDirection.md) | Defines the angle of the grain direction of the envelope. An angle of 0 is in the X direction of the envelope. You can modify the value by using the properties on the returned ModelParameter object. This is only valid when the solver type is True Shape and it returns null in all other cases. |
| [isCreateCopies](Arrange2DDefinition_isCreateCopies.md) | Gets if the original components were moved to create the arrangement or copied were created. This value can only be set when creating a new arrangement. |
| [isGlobalDirectionFaceUp](Arrange2DDefinition_isGlobalDirectionFaceUp.md) | Gets and sets the global direction for selected faces. When true, the components specified by selecting a face will be oriented such that the selection face will be oriented upward in the arrangement. |
| [isPartInPartAllowed](Arrange2DDefinition_isPartInPartAllowed.md) | Gets and sets if parts can be nested within void areas of other parts. This is only used when the solver type is 2D True Shape and is ignored for 2D Rectangular solutions. |
| [isValid](Arrange2DDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Arrange2DDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [solverType](Arrange2DDefinition_solverType.md) | Gets the type of arrange feature defined by this definition. |

## Version

Introduced in version January 2025  

