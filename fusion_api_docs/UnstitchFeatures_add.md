# UnstitchFeatures.add Method

Parent Object: [UnstitchFeatures](UnstitchFeatures.md)  

## Description

Creates a new Unstitch feature.

## Syntax

"unstitchFeatures_var" is a variable referencing a [UnstitchFeatures](UnstitchFeatures.md) object.

```python
# Uses no optional arguments.
returnValue = unstitchFeatures_var.add(faces)

# Uses optional arguments.
returnValue = unstitchFeatures_var.add(faces, isChainSelection)
```

## Return Value

| Type | Description |
|----|----|
| [UnstitchFeature](UnstitchFeature.md) | Returns the newly created UnstitchFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| faces | [ObjectCollection](ObjectCollection.md) | The faces and/or bodies to Unstitch. Individual faces can be unstitched from solid and/or patch bodies. The faces being unstitched need not all come from the same body. |
| isChainSelection | boolean | A boolean value for setting whether or not faces that are connected and adjacent to the input faces will be included in the selection. The default value is true. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [Unstitch Feature API Sample](UnstitchFeatureSample_Sample.md) | Demonstrates creating a new unstitch feature |

## Version

Introduced in version July 2015  

