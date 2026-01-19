# ClearanceHoleDataQuery.standardCustomName Method

Parent Object: [ClearanceHoleDataQuery](ClearanceHoleDataQuery.md)  

## Description

Method that returns the custom name for a given standard. The custom name is the localized name of the standard using the current language specified for Fusion.

## Syntax

"clearanceHoleDataQuery_var" is a variable referencing a [ClearanceHoleDataQuery](ClearanceHoleDataQuery.md) object.

```python
returnValue = clearanceHoleDataQuery_var.standardCustomName(standard)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns the specified custom name or an empty string if an invalid standard is specified. |

## Parameters

| Name     | Type   | Description                                       |
|----------|--------|---------------------------------------------------|
| standard | string | The standard you want to get the custom name for. |

## Version

Introduced in version September 2025  

