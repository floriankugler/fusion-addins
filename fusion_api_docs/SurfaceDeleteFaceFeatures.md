# SurfaceDeleteFaceFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing SurfaceDeleteFaceFeature features in a component and supports the ability to create new SurfaceDeleteFaceFeature features.  

The SurfaceDeleteFaceFeature and DeleteFaceFeature differ in that the SurfaceDeleteFaceFeature can delete any face without any restrictions. If the body is a solid, it will become a surface when the first face is deleted. The specified face is deleted without any other changes being made to the body. The DeleteFaceFeature deletes the specified face and also modifies the other faces in the body to heal or fill in the area of the deleted face. This means that a solid body will remain solid.

## Methods

| Name | Description |
|----|----|
| [add](SurfaceDeleteFaceFeatures_add.md) | Creates a new SurfaceDeleteFaceFeature feature. This deletes the specified faces from their bodies without any attempt to heal the openings. This is equivalent to selecting and deleting faces when in the Patch workspace. |
| [classType](SurfaceDeleteFaceFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SurfaceDeleteFaceFeatures_item.md) | Function that returns the specified SurfaceDeleteFaceFeature object using an index into the collection. |
| [itemByName](SurfaceDeleteFaceFeatures_itemByName.md) | Function that returns the specified SurfaceDeleteFaceFeature object using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](SurfaceDeleteFaceFeatures_count.md) | The number of SurfaceDeleteFaceFeature objects in the collection. |
| [isValid](SurfaceDeleteFaceFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SurfaceDeleteFaceFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.surfaceDeleteFaceFeatures](Features_surfaceDeleteFaceFeatures.md)

## Samples

| Name | Description |
|----|----|
| [DeleteFace Feature API Sample](DeleteFaceFeatureSample_Sample.md) | Demonstrates creating a new deleteFace feature. |

## Version

Introduced in version August 2016  

