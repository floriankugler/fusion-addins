# UntrimFeatures.createInputFromFaces Method

Parent Object: [UntrimFeatures](UntrimFeatures.md)  

## Description

Creates an UntrimFeatureInput object that defines the input needed to create an untrim feature. Use the input object to define the input to create the desired feature and then use the Add method, passing in the UntrimFeatureInput object.

## Syntax

"untrimFeatures_var" is a variable referencing a [UntrimFeatures](UntrimFeatures.md) object.

```python
# Uses no optional arguments.
returnValue = untrimFeatures_var.createInputFromFaces(faces, untrimLoopType)

# Uses optional arguments.
returnValue = untrimFeatures_var.createInputFromFaces(faces, untrimLoopType, extensionDistance)
```

## Return Value

| Type | Description |
|----|----|
| [UntrimFeatureInput](UntrimFeatureInput.md) | Returns the newly created UntrimFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| faces | BRepFace[] | An array of BRepFace objects that will have the loops of the specified type removed. Only loops that do not have a connected face can be removed (the edges in the loop have a single face). The array can only contain faces from surface bodies, (the isSolid property of the BRepBody returns false). |
| untrimLoopType | [UntrimLoopTypes](UntrimLoopTypes.md) | The loop type to be untrimmed (AllLoopUntrimType, InternalLoopUntrimType, or ExternalLoopUntrimType). |
| extensionDistance | [ValueInput](ValueInput.md) | If the untrim loop type is AllLoopUntrimType or ExternalLoopUntrimType the untrimmed faces can be extended by a specified distance. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [Untrim Feature API Sample](UntrimFeatureSample_Sample.md) | Demonstrates creating a new untrim feature. |

## Version

Introduced in version January 2021  

