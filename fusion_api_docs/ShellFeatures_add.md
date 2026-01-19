# ShellFeatures.add Method

Parent Object: [ShellFeatures](ShellFeatures.md)  

## Description

Creates a new shell feature.

## Syntax

"shellFeatures_var" is a variable referencing a [ShellFeatures](ShellFeatures.md) object.

```python
returnValue = shellFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ShellFeature](ShellFeature.md) | Returns the newly created ShellFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ShellFeatureInput](ShellFeatureInput.md) | A ShellFeatureInput object that defines the desired shell. Use the createInput method to create a new ShellFeatureInput object and then use methods on it (the ShellFeatureInput object) to define the shell. |

## Samples

| Name | Description |
|----|----|
| [shellFeatures.add](shelFeatures_add_Sample.md) | Demonstrates creating a shell feature. |
| [Shell Feature API Sample](ShellFeatureSample_Sample.md) | Demonstrates creating a new shell feature. |

## Version

Introduced in version November 2014  

