# LoftCenterLineOrRails Object

Derived from: [Base](Base.md) Object  

## Description

Defines a single centerline or one or more rails for a loft feature.

## Methods

| Name | Description |
| --- | --- |
| [addCenterLine](LoftCenterLineOrRails_addCenterLine.md) | Adds a centerline. A single centerline can be defined for a loft. If a centerline or rails have already been defined, they will be removed and the input will become the new single centerline. If this LoftCenterLineOrRails object is associated with a created feature, |
| [addRail](LoftCenterLineOrRails_addRail.md) | Add a rail to the loft definition. Multiple rails can be defined, so each call of this method adds a new rail. If this LoftCenterLineOrRails object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [classType](LoftCenterLineOrRails_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](LoftCenterLineOrRails_item.md) | Function that returns the specified LoftCenterLineOrRail using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](LoftCenterLineOrRails_count.md) | The number of centerlines or rails in the collection. |
| [isCenterLine](LoftCenterLineOrRails_isCenterLine.md) | Indicates if a centerline or rails are currently defined. |
| [isValid](LoftCenterLineOrRails_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](LoftCenterLineOrRails_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[LoftFeature.centerLineOrRails](LoftFeature_centerLineOrRails.md), [LoftFeatureInput.centerLineOrRails](LoftFeatureInput_centerLineOrRails.md)

## Version

Introduced in version August 2016  

