# SelectionCommandInput.addSelection Method

Parent Object: [SelectionCommandInput](SelectionCommandInput.md)  

## Description

Adds the selection to the list of selections associated with this input. This method is not valid within the commandCreated event but must be used later in the command lifetime. If you want to pre-populate the selection when the command is starting, you can use this method in the activate method of the Command. It's also valid to use in other events once the command is running, such as the validateInputs event.

## Syntax

"selectionCommandInput_var" is a variable referencing a [SelectionCommandInput](SelectionCommandInput.md) object.

```python
returnValue = selectionCommandInput_var.addSelection(selection)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if a selection to the entity was added to this input. |

## Parameters

| Name | Type | Description |
|----|----|----|
| selection | [Base](Base.md) | The entity to add a selection of to this input. The addition may fail if the entity does not match the selection filter, or adding it would exceed the limits. |

## Version

Introduced in version August 2014  

