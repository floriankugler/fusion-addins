# UntrimFeatureInput.setLoopsFromFaces Method

Parent Object: [UntrimFeatureInput](UntrimFeatureInput.md)  

## Description

Set the loops to be removed from a set of faces.

## Syntax

"untrimFeatureInput_var" is a variable referencing a [UntrimFeatureInput](UntrimFeatureInput.md) object.

```python
returnValue = untrimFeatureInput_var.setLoopsFromFaces(faces, untrimLoopType)
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns whether the operation was successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| faces | BRepFace\[\] | An array of BRepFace objects that will have the loops of the specified types removed. Only loops that do not have a connected face can be removed (the edges in the loop have a single face). The array can only contain faces from surface bodies, (the isSolid property of the BRepBody returns false). |
| untrimLoopType | [UntrimLoopTypes](UntrimLoopTypes.md) | The loop type to be untrimmed (AllLoopUntrimType, InternalLoopUntrimType, or ExternalLoopUntrimType). |

## Version

Introduced in version January 2021  

