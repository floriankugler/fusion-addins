# ThickenFeature.setInputEntities Method

Parent Object: [ThickenFeature](ThickenFeature.md)  

## Description

Sets the faces and patch bodies to thicken.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"thickenFeature_var" is a variable referencing a [ThickenFeature](ThickenFeature.md) object.

```python
# Uses no optional arguments.
returnValue = thickenFeature_var.setInputEntities(inputFaces)

# Uses optional arguments.
returnValue = thickenFeature_var.setInputEntities(inputFaces, isChainSelection)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| inputFaces | [ObjectCollection](ObjectCollection.md) | The faces or patch bodies to thicken. Faces need not be from the same component or body, nor do they need to be connected or touching one another. |
| isChainSelection | boolean | A boolean value for setting whether or not faces that are tangentially connected to the input faces (if any) will be included in the offset. The default value is true. This is an optional argument whose default value is True. |

## Version

Introduced in version June 2015  

