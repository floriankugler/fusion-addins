# OffsetFacesFeatures.createInput Method

Parent Object: [OffsetFacesFeatures](OffsetFacesFeatures.md)  

## Description

Creates an OffsetFacesFeatureInput object. Use properties and methods on this object to define the offset feature you want to create and then use the add method, passing in the OffsetFacesFeatureInput object to create the feature.

## Syntax

"offsetFacesFeatures_var" is a variable referencing an [OffsetFacesFeatures](OffsetFacesFeatures.md) object.

```python
returnValue = offsetFacesFeatures_var.createInput(faces, distance)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFacesFeatureInput](OffsetFacesFeatureInput.md) | Returns the newly created OffsetFacesFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| faces | BRepFace[] | An array of BRepFace objects to offset. These faces can exist on multiple bodies and in multiple components. They cannot be in an externally referenced component. |
| distance | [ValueInput](ValueInput.md) | The distance of the offset. A positive value offsets the faces in the direction of the face normal. A negative value goes in the other direction. This is a ValueInput object that can be created using either createByReal or createByString. When a real ValueInput is used, the value is centimeters. When a string ValueInput is used, it defines the expression of the parameter that will be created to control the feature and any valid expression that defines a distance can be used. |

## Version

Introduced in version November 2025  

