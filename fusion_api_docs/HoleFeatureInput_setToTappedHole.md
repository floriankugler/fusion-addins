# HoleFeatureInput.setToTappedHole Method

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Sets the hole to be a straight or tapered tapped hole of the size specified by the ThreadInfo object.

## Syntax

"holeFeatureInput_var" is a variable referencing a [HoleFeatureInput](HoleFeatureInput.md) object.

```python
returnValue = holeFeatureInput_var.setToTappedHole(threadInfo)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if setting to a tapped hole was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| threadInfo | [ThreadInfo](ThreadInfo.md) | The ThreadInfo object that specifies the thread to use for the tapped hole. Whether it is straight or tapered tap is defined by the input ThreadInfo object. |

## Version

Introduced in version September 2025  

