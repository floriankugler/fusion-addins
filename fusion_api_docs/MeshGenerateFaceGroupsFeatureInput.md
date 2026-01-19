
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

This class defines the methods and properties that pertain to the definition of a mesh generate face groups feature.

## Methods

| Name | Description |
|----|----|
| [classType](MeshGenerateFaceGroupsFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [angleThreshold](MeshGenerateFaceGroupsFeatureInput_angleThreshold.md) | Controls the angle threshold during the face group generation. The values can range between 0 and pi/2. The default value is 0.436. Only valid if meshGenerateFaceGroupsMethodType is FastGenerateFaceGroupsType. |
| [boundaryTolerance](MeshGenerateFaceGroupsFeatureInput_boundaryTolerance.md) | Gets and sets tolerance to define face group. This value is used during the fitting of the primitives. The values can range between 0 and 0.01. The default value is 0.001. Only valid if meshGenerateFaceGroupsMethodType is AccurateGenerateFaceGroupsType. |
| [isValid](MeshGenerateFaceGroupsFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [mesh](MeshGenerateFaceGroupsFeatureInput_mesh.md) | Gets and sets the input mesh body. |
| [meshGenerateFaceGroupsMethodType](MeshGenerateFaceGroupsFeatureInput_meshGenerateFaceGroupsMethodType.md) | Gets and sets the type of mesh generate face groups, default value is FastGenerateFaceGroupsType. |
| [minimumFaceGroupSize](MeshGenerateFaceGroupsFeatureInput_minimumFaceGroupSize.md) | Gets and sets the fraction of the overall mesh area which determines the smallest face group. The value can range between 0 and 1. The default value is 0.02. Only valid if meshGenerateFaceGroupsMethodType is FastGenerateFaceGroupsType. |
| [objectType](MeshGenerateFaceGroupsFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [targetBaseFeature](MeshGenerateFaceGroupsFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[MeshGenerateFaceGroupsFeatures.createInput](MeshGenerateFaceGroupsFeatures_createInput.md)

## Version

Introduced in version January 2025  

