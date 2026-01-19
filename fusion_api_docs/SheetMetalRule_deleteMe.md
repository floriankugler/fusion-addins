# SheetMetalRule.deleteMe Method

Parent Object: [SheetMetalRule](SheetMetalRule.md)  

## Description

Deletes the rule from the design or library. If the rule is in the library and set as the default rule, you cannot delete it. If the rule is in a design and is used by a component you cannot use it.

## Syntax

"sheetMetalRule_var" is a variable referencing a [SheetMetalRule](SheetMetalRule.md) object.

```python
returnValue = sheetMetalRule_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version November 2022  

