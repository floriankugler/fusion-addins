# Design.createInterferenceInput Method

Parent Object: [Design](Design.md)  

## Description

Creates an InterferenceInput object. This object collects the entities and options that are used when calculating interference. To analyze interference you first create an InterferenceInput supplying the entities and set any other settings and then provide this object as input to the analyzeInterference method.

## Syntax

"design_var" is a variable referencing a [Design](Design.md) object.

```python
returnValue = design_var.createInterferenceInput(entities)
```

## Return Value

| Type | Description |
|----|----|
| [InterferenceInput](InterferenceInput.md) | Returns an InterferenceInput object which you can use to set any other interference settings and then use as input to the analyzeInterference method to calculate the interference. Returns null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the BRepBody and/or Occurrence entities that will be used in the interference calculation. All entities must be in the context of the root component of the top-level design. |

## Samples

| Name | Description |
|----|----|
| [Analyze Interference API Sample](AnalyzeInterferenceSample_Sample.md) | Demonstrates analyzing the interference between components. This uses a direct modeling design because the ability to create bodies that represent the interference volume is only supported in a direct modeling design. |
| [Interference API Sample](InterferenceSample_Sample.md) | Demonstrates Interference APIs. |

## Version

Introduced in version November 2015  

