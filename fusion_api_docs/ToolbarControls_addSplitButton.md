# ToolbarControls.addSplitButton Method

Parent Object: [ToolbarControls](ToolbarControls.md)  

## Description

Adds a split button to the controls in a toolbar. A split button has two active areas that the user can click; the main button portion and the drop-down arrow. Clicking the main button, executes the displayed command. Clicking the drop-down displays the drop-down with additional commands.  

The split button itself does not fire any events, but the buttons within it will fire events to their associated command definitions.

## Syntax

"toolbarControls_var" is a variable referencing a [ToolbarControls](ToolbarControls.md) object.

```python
# Uses no optional arguments.
returnValue = toolbarControls_var.addSplitButton(defaultDefinition, additionalDefinitions, showLastUsed)

# Uses optional arguments.
returnValue = toolbarControls_var.addSplitButton(defaultDefinition, additionalDefinitions, showLastUsed, id, positionID, isBefore)
```

## Return Value

| Type | Description |
|----|----|
| [SplitButtonControl](SplitButtonControl.md) | Returns the newly created SplitButtonControl object or null if the creation fails. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| defaultDefinition | [CommandDefinition](CommandDefinition.md) | A command definition that will be used to create the main button. A button will also be created in the drop-down for this definition. |
| additionalDefinitions | CommandDefinition[] | An array of command definitions that will be used to create the buttons on the drop-down. |
| showLastUsed | boolean | Specifies if the split button should have the behavior where the command shown on the main button changes to the last executed command. |
| id | string | Optional unique ID for the control. It must be unique with respect to other controls in this collection. If the default empty string is provided, Fusion will create a unique ID. This is an optional argument whose default value is "". |
| positionID | string | Specifies the reference id of the control to position this control relative to. Not setting this value indicates that the control will be created at the end of all other controls in toolbar. The isBefore parameter specifies whether to place the control before or after the reference control. This is an optional argument whose default value is "". |
| isBefore | boolean | Specifies whether to place the control before or after the reference control specified by the positionID parameter. This argument is ignored is positionID is not specified This is an optional argument whose default value is True. |

## Version

Introduced in version August 2014  

