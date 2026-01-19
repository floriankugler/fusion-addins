# SheetMetalRules.addByCopy Method

Parent Object: [SheetMetalRules](SheetMetalRules.md)  

## Description

Creates a new sheet metal rule by copying an existing rule. The new rule can then be edited to define the rule characteristics you want.

## Syntax

"sheetMetalRules_var" is a variable referencing a [SheetMetalRules](SheetMetalRules.md) object.

```python
returnValue = sheetMetalRules_var.addByCopy(existingSheetMetalRule, name)
```

## Return Value

| Type | Description |
|----|----|
| [SheetMetalRule](SheetMetalRule.md) | Returns the new SheetMetalRule object or will assert in the case where it fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| existingSheetMetalRule | [SheetMetalRule](SheetMetalRule.md) | The existing SheetMetalRule object you want to copy. This can be a rule from the library or the design. |
| name | string | The name to assign to the new sheet metal rule. This name must be unique with respect to other sheet metal rules in the design or library it's created in. |

## Version

Introduced in version November 2022  

