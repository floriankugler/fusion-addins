# UntrimFeatureInput.setLoops Method

Parent Object: [UntrimFeatureInput](UntrimFeatureInput.md)  

## Description

Set the loops to be removed.

## Syntax

"untrimFeatureInput_var" is a variable referencing a [UntrimFeatureInput](UntrimFeatureInput.md) object.

```python
returnValue = untrimFeatureInput_var.setLoops(loops)
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns whether the operation was successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| loops | BRepLoop\[\] | Redefines this input to remove loops from the body. If faces were previously defined, that information will be lost. Only loops that do not have a connected face can be removed (the edges in the loop have a single face) The array can only contain loops from surface bodies, (the isSolid property of the BRepBody returns false). |

## Version

Introduced in version January 2021  

