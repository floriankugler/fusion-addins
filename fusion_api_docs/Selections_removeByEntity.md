# Selections.removeByEntity Method

Parent Object: [Selections](Selections.md)  

## Description

Removes the selections that are associated with the specified entity from the set of selected entities.

## Syntax

"selections_var" is a variable referencing a [Selections](Selections.md) object.

```python
returnValue = selections_var.removeByEntity(entity)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if the item was removed or not currently selected. |

## Parameters

| Name   | Type             | Description                         |
|--------|------------------|-------------------------------------|
| entity | [Base](Base.md) | The entity to remove selections of. |

## Version

Introduced in version August 2014  

