# Selections.asArray Method

Parent Object: [Selections](Selections.md)  

## Description

Returns an array containing all of the current selections. This is useful in cases where you need to iterate over the set of selected entities but need to create or edit data as you process each one. Selections are fragile and creation and edit operations will clear the selections so you won't have access to the complete list after processing the first one.

## Syntax

"selections_var" is a variable referencing a [Selections](Selections.md) object.

```python
returnValue = selections_var.asArray()
```

## Return Value

| Type | Description |
|----|----|
| [Selection](Selection.md)\[\] | Returns an array of all of the current selections. Selection objects are returned so you'll need to call their entity properties to get the actual selected entity. |

## Version

Introduced in version September 2017  

