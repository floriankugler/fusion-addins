# OffsetFeature.setInputEntities Method

Parent Object: [OffsetFeature](OffsetFeature.md)  

## Description

Sets the faces and sheet bodies to offset.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"offsetFeature_var" is a variable referencing an [OffsetFeature](OffsetFeature.md) object.

```python
# Uses no optional arguments.
returnValue = offsetFeature_var.setInputEntities(entities)

# Uses optional arguments.
returnValue = offsetFeature_var.setInputEntities(entities, isChainSelection)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| entities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the BRepFace objects to offset. Additional faces may be automatically used depending on the value of the isChainSelection argument. Input faces need not be from the same body. |
| isChainSelection | boolean | A boolean value for setting whether or not faces that are tangentially connected to the input faces (if any) will also be offset. The default value is true. This is an optional argument whose default value is True. |

## Version

Introduced in version June 2015  

