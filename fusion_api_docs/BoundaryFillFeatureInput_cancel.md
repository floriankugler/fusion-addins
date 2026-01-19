# BoundaryFillFeatureInput.cancel Method

Parent Object: [BoundaryFillFeatureInput](BoundaryFillFeatureInput.md)  

## Description

To determine the possible boundaries and allow you to choose which cells to keep, the boundary fill feature does a partial compute when the input object is created. To do this it starts a boundary fill feature transaction and completes the transaction when you call the add method. If you don't call the add method to finish the transaction it leaves Fusion in a bad state and there will be undo problems and possibly a crash. If you have created a BoundFillFeatureInput object and don't want to finish the feature creation, you need to call the cancel method on the BoundaryFillFeatureInput object to safely abort the current boundary fill transaction.

## Syntax

"boundaryFillFeatureInput_var" is a variable referencing a [BoundaryFillFeatureInput](BoundaryFillFeatureInput.md) object.

```python
returnValue = boundaryFillFeatureInput_var.cancel()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Version

Introduced in version April 2019  

