# CopyPasteBody.sourceBody Property

Parent Object: [CopyPasteBody](CopyPasteBody.md)  

## Description

Returns the bodies that were copied to create the result bodies of this feature. An ObjectCollection is returned that will contain the original bodies. It's possible that the collection can be empty or contain less than the number of bodies originally copied. This happens in the case where a body has been deleted or consumed by some other operation.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"copyPasteBody_var" is a variable referencing a CopyPasteBody object.  

```python
# Get the value of the property.
propertyValue = copyPasteBody_var.sourceBody
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Samples

| Name | Description |
|----|----|
| [Copy Paste Bodies API Sample](CopyPasteBodiesSample_Sample.md) | Demonstrates how to use Copy Paste Bodies related API. |

## Version

Introduced in version June 2017  

