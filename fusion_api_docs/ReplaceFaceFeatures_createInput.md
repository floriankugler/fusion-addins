# ReplaceFaceFeatures.createInput Method

Parent Object: [ReplaceFaceFeatures](ReplaceFaceFeatures.md)  

## Description

Creates a ReplaceFaceFeatureInput object. Use properties and methods on this object to define the replace face you want to create and then use the Add method, passing in the ReplaceFaceFeatureInput object.

## Syntax

"replaceFaceFeatures_var" is a variable referencing a [ReplaceFaceFeatures](ReplaceFaceFeatures.md) object.

```python
returnValue = replaceFaceFeatures_var.createInput(sourceFaces, isTangentChain, targetFaces)
```

## Return Value

| Type | Description |
|----|----|
| [ReplaceFaceFeatureInput](ReplaceFaceFeatureInput.md) | Returns the newly created ReplaceFaceFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sourceFaces | [ObjectCollection](ObjectCollection.md) | Input the entities that define the source faces (the faces to be replaced). The collection can contain the faces from a solid and/or features. All the faces must be on the same body. |
| isTangentChain | boolean | A boolean value for setting whether or not faces that are tangentially connected to the input faces (if any) will also be included. A value of true indicates that tangent faces will be included. |
| targetFaces | [Base](Base.md) | Input the entities that define the target faces. The new faces must completely intersect the part. The collection can contain the surface faces, surface bodies and construction planes. |

## Samples

| Name | Description |
|----|----|
| [replaceFaceFeatures.add](replaceFaceFeatures_add_Sample.md) | Demonstrate the remove replaceFaceFeatures.add method. |
| [ReplaceFace Feature](ReplaceFaceFeatureSample_Sample.md) | Demonstrates creating a new replaceface feature. |

## Version

Introduced in version March 2015  

