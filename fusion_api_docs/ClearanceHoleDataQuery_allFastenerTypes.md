# ClearanceHoleDataQuery.allFastenerTypes Method

Parent Object: [ClearanceHoleDataQuery](ClearanceHoleDataQuery.md)  

## Description

This method returns an array of all the available fastener types for the given standard. To get the available standards, use the allStandards property.

## Syntax

"clearanceHoleDataQuery_var" is a variable referencing a [ClearanceHoleDataQuery](ClearanceHoleDataQuery.md) object.

```python
returnValue = clearanceHoleDataQuery_var.allFastenerTypes(standard)
```

## Return Value

| Type | Description |
|----|----|
| string\[\] | Returns the specified fastener types or an empty array if an invalid standard is specified. |

## Parameters

| Name     | Type   | Description                    |
|----------|--------|--------------------------------|
| standard | string | The standard to search within. |

## Version

Introduced in version September 2025  

