# MoveFeatureTranslateXYZDefinition Object

Derived from: [MoveFeatureDefinition](MoveFeatureDefinition.md) Object  

## Description

The MoveFeatureTranslateXYZDefinition object defines a move feature described by offsets in the X, Y, and Z directions.

## Methods

| Name | Description |
|----|----|
| [classType](MoveFeatureTranslateXYZDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isDesignSpace](MoveFeatureTranslateXYZDefinition_isDesignSpace.md) | Gets and sets if the translation is defined with respect to the design or component space. Design space is the same as the root component space. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isValid](MoveFeatureTranslateXYZDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MoveFeatureTranslateXYZDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentMoveFeature](MoveFeatureTranslateXYZDefinition_parentMoveFeature.md) | Returns the parent MoveFeature object |
| [xDistance](MoveFeatureTranslateXYZDefinition_xDistance.md) | Gets the model parameter that controls the X distance of the translation. You can use properties on the returned ModelParameter object to edit the offset distance. |
| [yDistance](MoveFeatureTranslateXYZDefinition_yDistance.md) | Gets the model parameter that controls the Y distance of the translation. You can use properties on the returned ModelParameter object to edit the offset distance. |
| [zDistance](MoveFeatureTranslateXYZDefinition_zDistance.md) | Gets the model parameter that controls the Z distance of the translation. You can use properties on the returned ModelParameter object to edit the offset distance. |

## Version

Introduced in version January 2023  

