# MoveFeatures.createInput2 Method

Parent Object: [MoveFeatures](MoveFeatures.md)  

## Description

Creates a MoveFeatureInput object. Use properties and methods on this object to define how the move is defined and then use the MoveFeatues.add method, passing in the MoveFeatureInput object to create a move feature.

## Syntax

"moveFeatures_var" is a variable referencing a [MoveFeatures](MoveFeatures.md) object.

```python
returnValue = moveFeatures_var.createInput2(inputEntities)
```

## Return Value

| Type | Description |
|----|----|
| [MoveFeatureInput](MoveFeatureInput.md) | Returns the newly created MoveFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| inputEntities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the objects to move. For a parametric model, the collection can contain BRepBody or BRepFace objects but not a combination of both. |

## Samples

| Name | Description |
|----|----|
| [moveFeatures.add](moveFeatures_add_Sample.md) | Demonstrates the moveFeatures.add method. |
| [Move Feature API Sample](MoveFeatureSample_Sample.md) | Demonstrates creating a new move feature. |

## Version

Introduced in version January 2023  

