# MoveFeatures.createInput Method

Parent Object: [MoveFeatures](MoveFeatures.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates a MoveFeatureInput object. Use properties and methods on this object to define the move feature you want to create and then use the Add method, passing in the MoveFeatureInput object.

## Remarks

This method is obsolete. You should use the createInput2 method instead.

## Syntax

"moveFeatures_var" is a variable referencing a [MoveFeatures](MoveFeatures.md) object.

```python
returnValue = moveFeatures_var.createInput(inputEntities, transform)
```

## Return Value

| Type | Description |
|----|----|
| [MoveFeatureInput](MoveFeatureInput.md) | Returns the newly created MoveFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| inputEntities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the entities to move. This collection can only contain BRepBody objects in parametric modeling. It can be BRep bodies, T-Spline bodies, mesh bodies mixed or faces and features mixed in non-parametric modeling. |
| transform | [Matrix3D](Matrix3D.md) | The transform to apply to the input entities. This can describe a move (translation) or a rotation. The matrix must define an orthogonal transform. That is the axes must be perpendicular to each other and there can't be any scaling or mirroring defined. |

## Version

Introduced in version March 2015  
Retired in version January 2023  

