# Command.setDialogMinimumSize Method

Parent Object: [Command](Command.md)  

## Description

Sets the minimum size for the dialog when resized to by the user. If this is not set, a default minimum size is used.

## Syntax

"command_var" is a variable referencing a [Command](Command.md) object.

```python
returnValue = command_var.setDialogMinimumSize(width, height)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if the minimum size was successfully set. |

## Parameters

| Name   | Type    | Description                                 |
|--------|---------|---------------------------------------------|
| width  | integer | The minimum width of the dialog in pixels.  |
| height | integer | The minimum height of the dialog in pixels. |

## Version

Introduced in version June 2015  

