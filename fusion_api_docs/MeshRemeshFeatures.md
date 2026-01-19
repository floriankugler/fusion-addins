
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Collection that provides access to all of the existing mesh re-mesh features in a component and supports the ability to create new mesh re-mesh features.

## Methods

| Name | Description |
|----|----|
| [add](MeshRemeshFeatures_add.md) | Creates a mesh re-mesh feature. |
| [classType](MeshRemeshFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](MeshRemeshFeatures_createInput.md) | Creates a MeshRemeshFeatureInput object. Use properties and methods on this object to define the mesh re-mesh you want to create and then use the add method, passing in the MeshRemeshFeatureInput object. |
| [item](MeshRemeshFeatures_item.md) | Function that returns the specified mesh re-mesh feature using an index into the collection. |
| [itemByName](MeshRemeshFeatures_itemByName.md) | Function that returns the specified MeshRemesh feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](MeshRemeshFeatures_count.md) | The number of mesh re-mesh features in the collection. |
| [isValid](MeshRemeshFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MeshRemeshFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.meshRemeshFeatures](Features_meshRemeshFeatures.md)

## Version

Introduced in version March 2024  

