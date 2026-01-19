# SheetMetalRules.item Method

Parent Object: [SheetMetalRules](SheetMetalRules.md)  

## Description

Function that returns the specified sheet metal rule using an index into the collection.

## Syntax

"sheetMetalRules_var" is a variable referencing a [SheetMetalRules](SheetMetalRules.md) object.

```python
returnValue = sheetMetalRules_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SheetMetalRule](SheetMetalRule.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2022  

