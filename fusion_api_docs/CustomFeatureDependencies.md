
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

A collection of dependencies associated with a particular custom feature. These are the entities that the custom feature is dependent on. If these entities are modified, it will cause the custom feature to recompute so it can be up to date. These dependencies are saved with the custom feature and can be accessed at a later time, typically during the compute, to access and use the entities.

## Methods

| Name | Description |
|----|----|
| [add](CustomFeatureDependencies_add.md) | Adds an entity or parameter that this feature is dependent on. This is used by Fusion to know when to recompute this feature and to control the behavior of the feature's node in the timeline. |
| [classType](CustomFeatureDependencies_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteAll](CustomFeatureDependencies_deleteAll.md) | Deletes all of the current dependencies. This method is for convenience and is equivalent to iterating through the collection and deleting them one at a time. |
| [item](CustomFeatureDependencies_item.md) | Function that returns the specified custom dependency using an index into the collection. |
| [itemById](CustomFeatureDependencies_itemById.md) | Function that returns the specified custom dependency given its ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](CustomFeatureDependencies_count.md) | The number of CustomFeatureParameter objects in the collection. |
| [isValid](CustomFeatureDependencies_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomFeatureDependencies_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CustomFeature.dependencies](CustomFeature_dependencies.md)

## Version

Introduced in version January 2021  

