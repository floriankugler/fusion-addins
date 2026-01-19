# ToolbarTab.move Method

Parent Object: [ToolbarTab](ToolbarTab.md)  

## Description

Move this tab to a different position in the Toolbar in the user interface.

## Syntax

"toolbarTab_var" is a variable referencing a [ToolbarTab](ToolbarTab.md) object.

```python
returnValue = toolbarTab_var.move(positionId, isBefore)
```

## Return Value

| Type    | Description                        |
|---------|------------------------------------|
| boolean | Returns true if it was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| positionId | string | The ID of another ToolbarTab in the same Toolbar that is used to position this tab. This tab will be positioned either directly before or after it. |
| isBefore | boolean | If true, then this tab will be positioned directly before the tab indicated by positionID. If false, then this tab will be positioned after it. |

## Version

Introduced in version May 2024  

