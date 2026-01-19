# Selections.add Method

Parent Object: [Selections](Selections.md)  

## Description

Adds the entity to the set of currently selected entities. The user will see the entity become selected in the user interface.

## Syntax

"selections_var" is a variable referencing a [Selections](Selections.md) object.

```python
returnValue = selections_var.add(entity)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | The entity to select and add to this selection set. |

## Version

Introduced in version August 2014  

