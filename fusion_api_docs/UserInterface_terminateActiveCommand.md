# UserInterface.terminateActiveCommand Method

Parent Object: [UserInterface](UserInterface.md)  

## Description

Method that causes the currently active (running) command to be terminated

## Remarks

The terminateActiveCommand method is not supported within any of the Command related events because it results in the termination of the current command, which is your running command.

## Syntax

"userInterface_var" is a variable referencing a [UserInterface](UserInterface.md) object.

```python
returnValue = userInterface_var.terminateActiveCommand()
```

## Return Value

| Type    | Description                                                    |
|---------|----------------------------------------------------------------|
| boolean | Returns true if terminating the active command was successful. |

## Version

Introduced in version November 2015  

