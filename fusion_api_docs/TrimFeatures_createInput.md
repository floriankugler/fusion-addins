# TrimFeatures.createInput Method

Parent Object: [TrimFeatures](TrimFeatures.md)  

## Description

Creates a TrimFeatureInput object. Use properties and methods on this object to define the trim feature you want to create and then use the Add method, passing in the TrimFeatureInput object.  

To determine the possible boundaries and allow you to choose which cells to keep, the trim feature does a partial compute when the input object is created. To do this it starts a trim feature transaction and completes the transaction when you call the add method. If you don't call the add method to finish the transaction it leaves Fusion in a bad state and there will be undo problems and possibly a crash. If you have created a TrimFeatureInput object and don't want to finish the feature creation, you need to call the cancel method on the TrimFeatureInput object to safely abort the current boundary fill transaction.

## Syntax

"trimFeatures_var" is a variable referencing a [TrimFeatures](TrimFeatures.md) object.

```python
returnValue = trimFeatures_var.createInput(trimTool)
```

## Return Value

| Type | Description |
|----|----|
| [TrimFeatureInput](TrimFeatureInput.md) | Returns the newly created TrimFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| trimTool | [Base](Base.md) | A patch body, B-Rep face, construction plane or sketch curve that intersects the surface or surfaces to be trimmed |

## Samples

| Name | Description |
|----|----|
| [trimFeatures.add](trimFeatures_add_Sample.md) | Demonstrates the trimFeatures.add method. |
| [Trim Feature API Sample](TrimFeatureSample_Sample.md) | Demonstrates creating a new trim feature. |

## Version

Introduced in version July 2015  

