# ClearanceHoleDataQuery.allSizes Method

Parent Object: [ClearanceHoleDataQuery](ClearanceHoleDataQuery.md)  

## Description

This method returns an array of all the sizes for the given standard and fastener type. Valid standards and fastener types can be obtained using the allStandards and allFastenerTypes functions.

## Syntax

"clearanceHoleDataQuery_var" is a variable referencing a [ClearanceHoleDataQuery](ClearanceHoleDataQuery.md) object.

```python
returnValue = clearanceHoleDataQuery_var.allSizes(standard, fastenerType)
```

## Return Value

| Type | Description |
|----|----|
| string\[\] | Returns the specified sizes or empty array if an invalid standard or fastener type is specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| standard | string | The standard to search within. |
| fastenerType | string | The fastener type in the specified standard to search within. |

## Version

Introduced in version September 2025  

