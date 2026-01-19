# UnstitchFeature.setInputFaces Method

Parent Object: [UnstitchFeature](UnstitchFeature.md)  

## Description

Sets the faces and/or bodies to be unstitched.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"unstitchFeature_var" is a variable referencing a [UnstitchFeature](UnstitchFeature.md) object.

```python
# Uses no optional arguments.
returnValue = unstitchFeature_var.setInputFaces(faces)

# Uses optional arguments.
returnValue = unstitchFeature_var.setInputFaces(faces, isChainSelection)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| faces | [ObjectCollection](ObjectCollection.md) | The faces and/or bodies to Unstitch. Individual faces can be unstitched from solids and/or patch bodies. The faces being unstitched need not all come from the same body. |
| isChainSelection | boolean | A boolean value for setting whether or not faces that are connected and adjacent to the input faces will be included in the selection. The default value is true. This is an optional argument whose default value is True. |

## Version

Introduced in version July 2015  

