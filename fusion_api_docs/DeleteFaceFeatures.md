# DeleteFaceFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing DeleteFaceFeature features in a component and supports the ability to create new DeleteFaceFeature features.  

The SurfaceDeleteFaceFeature and DeleteFaceFeature differ in that the SurfaceDeleteFaceFeature can delete any face without any restrictions. If the body is a solid, it will become a surface when the first face is deleted. The specified face is deleted without any other changes being made to the body. The DeleteFaceFeature deletes the specified face and also modifies the other faces in the body to heal or fill in the area of the deleted face. This means that a solid body will remain solid.

## Methods

| Name | Description |
|----|----|
| [add](DeleteFaceFeatures_add.md) | Creates a new SurfaceDeleteFace feature. This deletes the specified faces from their bodies and attempts to heal the body. The method will fail if the body cannot be healed. This is equivalent to selecting and deleting faces when in the Patch workspace. |
| [classType](DeleteFaceFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](DeleteFaceFeatures_item.md) | Function that returns the specified DeleteFaceFeature object using an index into the collection. |
| [itemByName](DeleteFaceFeatures_itemByName.md) | Function that returns the specified DeleteFaceFeature object using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](DeleteFaceFeatures_count.md) | The number of DeleteFaceFeature objects in the collection. |
| [isValid](DeleteFaceFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DeleteFaceFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.deleteFaceFeatures](Features_deleteFaceFeatures.md)

## Version

Introduced in version August 2016  

