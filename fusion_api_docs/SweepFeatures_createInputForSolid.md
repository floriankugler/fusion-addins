# SweepFeatures.createInputForSolid Method

Parent Object: [SweepFeatures](SweepFeatures.md)  

## Description

Creates a SweepFeatureInput object for defining a simple sweep feature from a B-Rep solid with a path. Use properties and methods on this object to define the sweep you want to create, and then use the Add method, passing in the SweepFeatureInput object.

## Syntax

"sweepFeatures_var" is a variable referencing a [SweepFeatures](SweepFeatures.md) object.

```python
returnValue = sweepFeatures_var.createInputForSolid(solidBody, path, operation)
```

## Return Value

| Type | Description |
|----|----|
| [SweepFeatureInput](SweepFeatureInput.md) | Returns the newly created SweepFeatureInput object or null if the creation fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| solidBody | [BRepBody](BRepBody.md) | The BRepBody object to sweep. It must be a solid body. |
| path | [Path](Path.md) | The Path object that defines the path the body will be swept along. |
| operation | [FeatureOperations](FeatureOperations.md) | The type of feature operation to perform. |

## Version

Introduced in version May 2024  

