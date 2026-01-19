# Design.analyzeInterference Method

Parent Object: [Design](Design.md)  

## Description

Calculates the interference between the input bodies and/or occurrences.

## Syntax

"design_var" is a variable referencing a [Design](Design.md) object.

```python
returnValue = design_var.analyzeInterference(input)
```

## Return Value

| Type | Description |
|----|----|
| [InterferenceResults](InterferenceResults.md) | Returns an InterferenceResults object that can be used to examine the interference results. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [InterferenceInput](InterferenceInput.md) | An InterferenceInput that defines all of the necessary input needed to calculate the interference. An InterferenceInput object is created using the createInterferenceInput method. |

## Samples

| Name | Description |
|----|----|
| [Analyze Interference API Sample](AnalyzeInterferenceSample_Sample.md) | Demonstrates analyzing the interference between components. This uses a direct modeling design because the ability to create bodies that represent the interference volume is only supported in a direct modeling design. |
| [Interference API Sample](InterferenceSample_Sample.md) | Demonstrates Interference APIs. |

## Version

Introduced in version November 2015  

