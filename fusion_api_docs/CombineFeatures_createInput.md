# CombineFeatures.createInput Method

Parent Object: [CombineFeatures](CombineFeatures.md)  

## Description

Creates a CombineFeatureInput object. Use properties and methods on this object to define the combine you want to create and then use the Add method, passing in the CombineFeatureInput object.

## Syntax

"combineFeatures_var" is a variable referencing a [CombineFeatures](CombineFeatures.md) object.

```python
returnValue = combineFeatures_var.createInput(targetBody, toolBodies)
```

## Return Value

| Type | Description |
|----|----|
| [CombineFeatureInput](CombineFeatureInput.md) | Returns the newly created CombineFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| targetBody | [BRepBody](BRepBody.md) | A BRep body that represents the blank body. |
| toolBodies | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing one or more BRep bodies that represent tool bodies. |

## Samples

| Name | Description |
|----|----|
| [combineFeatures.add](combineFeatures_add_Sample.md) | Demonstrates the combineFeatures.add method. To use this sample, have a design open that contains at least two bodies. When you run the sample, you will be prompted to select the bodies and they will joined. |

## Version

Introduced in version November 2014  

