
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

A custom feature dependency defines a dependency the custom feature has on an entity outside the custom feature. For example, a feature might be dependent on a face or a point and if those entities are modified the custom feature needs to recompute to be up to date.

## Methods

| Name | Description |
|----|----|
| [classType](CustomFeatureDependency_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](CustomFeatureDependency_deleteMe.md) | Deletes this dependency from the custom feature. |

## Properties

| Name | Description |
| --- | --- |
| [entity](CustomFeatureDependency_entity.md) | Gets and sets the entity associated with this dependency. |
| [id](CustomFeatureDependency_id.md) | Returns the ID of this custom feature dependency. |
| [isValid](CustomFeatureDependency_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomFeatureDependency_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCustomFeature](CustomFeatureDependency_parentCustomFeature.md) | Returns the custom feature this dependency is associated with. |

## Accessed From

[CustomFeatureDependencies.add](CustomFeatureDependencies_add.md), [CustomFeatureDependencies.item](CustomFeatureDependencies_item.md), [CustomFeatureDependencies.itemById](CustomFeatureDependencies_itemById.md)

## Version

Introduced in version January 2021  

