# InterferenceResults.createBodies Method

Parent Object: [InterferenceResults](InterferenceResults.md)  

## Description

Creates bodies in the model that represent the interference volumes. This is not supported in parametric modeling.

## Syntax

"interferenceResults_var" is a variable referencing an [InterferenceResults](InterferenceResults.md) object.

```python
returnValue = interferenceResults_var.createBodies(allInterferenceBodies)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns an ObjectCollection containing the bodies that were created. |

## Parameters

| Name | Type | Description |
|----|----|----|
| allInterferenceBodies | boolean | Sets if all bodies or only individual bodies will be created as bodies in the model. If False, then only interferenceResult objects whose isCreateBody property is true will be created as a model body. If true, all interface volumes will be created as a body regardless of the value of the isCreateBody property on each InterferenceResult object. |

## Samples

| Name | Description |
|----|----|
| [Analyze Interference API Sample](AnalyzeInterferenceSample_Sample.md) | Demonstrates analyzing the interference between components. This uses a direct modeling design because the ability to create bodies that represent the interference volume is only supported in a direct modeling design. |
| [Interference API Sample](InterferenceSample_Sample.md) | Demonstrates Interference APIs. |

## Version

Introduced in version November 2015  

