# ThreadFeature.setThreadOffsetLength Method

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Sets the thread offset, length and location. Calling this method will cause the isFullLength property to be set to false.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"threadFeature_var" is a variable referencing a [ThreadFeature](ThreadFeature.md) object.

```python
returnValue = threadFeature_var.setThreadOffsetLength(threadOffset, threadLength, threadLocation)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| threadOffset | [ValueInput](ValueInput.md) | A ValueInput object that defines the thread offset. |
| threadLength | [ValueInput](ValueInput.md) | A ValueInput object that defines the thread length. |
| threadLocation | [ThreadLocations](ThreadLocations.md) | Indicates where the thread length is measured from. |

## Version

Introduced in version January 2015  

