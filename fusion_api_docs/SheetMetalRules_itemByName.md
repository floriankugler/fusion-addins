# SheetMetalRules.itemByName Method

Parent Object: [SheetMetalRules](SheetMetalRules.md)  

## Description

Function that returns the specified sheet metal rule using the name of the rule.

## Syntax

"sheetMetalRules_var" is a variable referencing a [SheetMetalRules](SheetMetalRules.md) object.

```python
returnValue = sheetMetalRules_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SheetMetalRule](SheetMetalRule.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the rule within the collection to return. This is the name seen in the Sheet Metal Rules dialog. |

## Version

Introduced in version November 2022  

