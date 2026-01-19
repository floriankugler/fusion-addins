# ToolbarControlList.itemById Method

Parent Object: [ToolbarControlList](ToolbarControlList.md)  

## Description

Returns the ToolbarControl at the specified ID.

## Syntax

"toolbarControlList_var" is a variable referencing a [ToolbarControlList](ToolbarControlList.md) object.

```python
returnValue = toolbarControlList_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarControl](ToolbarControl.md) | Returns the ToolbarControl with the specified ID or null if no control has this ID. |

## Parameters

| Name | Type   | Description                                            |
|------|--------|--------------------------------------------------------|
| id   | string | The ID of the control within the collection to return. |

## Version

Introduced in version August 2014  

