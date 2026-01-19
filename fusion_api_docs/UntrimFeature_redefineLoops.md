# UntrimFeature.redefineLoops Method

Parent Object: [UntrimFeature](UntrimFeature.md)  

## Description

Set the loops to be removed.

## Syntax

"untrimFeature_var" is a variable referencing a [UntrimFeature](UntrimFeature.md) object.

```python
returnValue = untrimFeature_var.redefineLoops(loops)
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns whether the operation was successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| loops | BRepLoop\[\] | Input the entities that define loops to remove. Only loops that do not have a connected face can be removed (the edges in the loop have a single face) The array can only contain loops from surface bodies, (the isSolid property of the BRepBody returns false). |

## Version

Introduced in version January 2021  

