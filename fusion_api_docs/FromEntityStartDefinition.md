# FromEntityStartDefinition Object

Derived from: [ExtentDefinition](ExtentDefinition.md) Object  

## Description

A definition object that is used to define a feature whose start is defined by a specified construction plane or face. If a face is specified it must be large enough to completely contain the projected profile.

## Methods

| Name | Description |
|----|----|
| [classType](FromEntityStartDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](FromEntityStartDefinition_create.md) | Statically creates a new FromEntityStartDefinition object. This is used as input when create a new feature and defining the starting condition. |

## Properties

| Name | Description |
| --- | --- |
| [entity](FromEntityStartDefinition_entity.md) | Gets and sets the entity defining the start of the feature. |
| [isValid](FromEntityStartDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FromEntityStartDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offset](FromEntityStartDefinition_offset.md) | Gets the currently defined offset value. If the FromEntityStartDefinition object was created statically and is not associated with a feature, this will return a ValueInput object. if the FromEntityStartDefinition is associated with an existing feature, this will return the parameter that was created when the feature was created. To edit the offset, use properties on the parameter to change the value of the parameter. |
| [parentFeature](FromEntityStartDefinition_parentFeature.md) | Returns the parent feature that this definition is associated with. If this definition has been created statically and is not associated with a feature this property will return null. |

## Accessed From

[FromEntityStartDefinition.create](FromEntityStartDefinition_create.md)

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version November 2016  

