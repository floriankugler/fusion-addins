# Command.beginStep Method

Parent Object: [Command](Command.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Begin a transacted step within the command's transaction. If the all of the command inputs are valid, this will trigger the execute event for the current step.

## Syntax

"command_var" is a variable referencing a [Command](Command.md) object.

```python
# Uses no optional arguments.
returnValue = command_var.beginStep()

# Uses optional arguments.
returnValue = command_var.beginStep(makeExistingStepNonUndoable)
```

## Return Value

| Type    | Description                                        |
|---------|----------------------------------------------------|
| boolean | Returns true if beginning the step was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| makeExistingStepNonUndoable | boolean | If true the current step will not be undo-able. This is an optional argument whose default value is False. |

## Version

Introduced in version January 2021  

