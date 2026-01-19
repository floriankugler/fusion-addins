# Selections.removeBySelection Method

Parent Object: [Selections](Selections.md)  

## Description

Removes the specified selection from the set of selected entities.

## Syntax

"selections_var" is a variable referencing a [Selections](Selections.md) object.

```python
returnValue = selections_var.removeBySelection(selection)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if the item was removed or not currently selected. |

## Parameters

| Name      | Type                       | Description              |
|-----------|----------------------------|--------------------------|
| selection | [Selection](Selection.md) | The selection to remove. |

## Version

Introduced in version August 2014  

