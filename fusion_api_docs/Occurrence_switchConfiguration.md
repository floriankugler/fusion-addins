# Occurrence.switchConfiguration Method

Parent Object: [Occurrence](Occurrence.md)  

## Description

Changes which configuration is used for this occurrence. Use the isConfiguration property to determine if this occurrence references a configuration.

## Syntax

"occurrence_var" is a variable referencing an [Occurrence](Occurrence.md) object.

```python
returnValue = occurrence_var.switchConfiguration(newRow)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the switch was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| newRow | [ConfigurationRow](ConfigurationRow.md) | The row to switch to. This row must be from the same ConfigurationTopTable as the current row. You can access the table from the parent design. |

## Version

Introduced in version January 2024  

