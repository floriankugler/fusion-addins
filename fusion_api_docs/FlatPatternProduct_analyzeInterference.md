# FlatPatternProduct.analyzeInterference Method

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Calculates the interference between the input bodies and/or occurrences.

## Syntax

"flatPatternProduct_var" is a variable referencing a [FlatPatternProduct](FlatPatternProduct.md) object.

```python
returnValue = flatPatternProduct_var.analyzeInterference(input)
```

## Return Value

| Type | Description |
|----|----|
| [InterferenceResults](InterferenceResults.md) | Returns an InterferenceResults object that can be used to examine the interference results. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [InterferenceInput](InterferenceInput.md) | An InterferenceInput that defines all of the necessary input needed to calculate the interference. An InterferenceInput object is created using the createInterferenceInput method. |

## Version

Introduced in version October 2022  

