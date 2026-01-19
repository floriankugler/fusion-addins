# WorkingModel.analyzeInterference Method

Parent Object: [WorkingModel](WorkingModel.md)  

## Description

Calculates the interference between the input bodies and/or occurrences.

## Syntax

"workingModel_var" is a variable referencing a [WorkingModel](WorkingModel.md) object.

```python
returnValue = workingModel_var.analyzeInterference(input)
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

Introduced in version January 2024  

