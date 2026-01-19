# Operations.item Method

Parent Object: [Operations](Operations.md)  

## Description

Function that returns the specified operation using an index into the collection.

## Syntax

"operations_var" is a variable referencing an [Operations](Operations.md) object.

```python
returnValue = operations_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Operation](Operation.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [Generate Setup Sheets API Sample](GenerateSetupSheets_Sample_Sample.md) | Demonstrates generating the setup sheets for an existing toolpath.. |
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |

## Version

Introduced in version January 2016  

