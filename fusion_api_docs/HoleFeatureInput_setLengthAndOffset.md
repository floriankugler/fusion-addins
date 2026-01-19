# HoleFeatureInput.setLengthAndOffset Method

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Sets the length and offset of the thread of a tapped hole.  

This method is only used when creating a tapped hole, which means the setToTappedHole method has been called. Otherwise calling this method will fail.  

By default the isFullLength property is true which means the thread is the full length of the hole and there is no offset. Calling this method will have the side effect of setting the isFullLength property to false.

## Syntax

"holeFeatureInput_var" is a variable referencing a [HoleFeatureInput](HoleFeatureInput.md) object.

```python
returnValue = holeFeatureInput_var.setLengthAndOffset(length, offset)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| length | [ValueInput](ValueInput.md) | Sets the length of the thread. |
| offset | [ValueInput](ValueInput.md) | Sets the offset of the thread from the start of the hole. A value of zero is valid for no offset. |

## Version

Introduced in version September 2025  

