# Occurrences.addFromConfiguration Method

Parent Object: [Occurrences](Occurrences.md)  

## Description

Method that inserts a configuration from a configured design. The insert will fail if the configured design being used is not from the same project as the file it is being inserted into.

## Syntax

"occurrences_var" is a variable referencing an [Occurrences](Occurrences.md) object.

```python
returnValue = occurrences_var.addFromConfiguration(configurationRow, transform)
```

## Return Value

| Type | Description |
|----|----|
| [Occurrence](Occurrence.md) | Returns the newly created occurrence or null if the add failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| configurationRow | [ConfigurationRow](ConfigurationRow.md) | The row that specifies which configuration to use. |
| transform | [Matrix3D](Matrix3D.md) | A transform that defines the location for the new occurrence. |

## Version

Introduced in version January 2024  

