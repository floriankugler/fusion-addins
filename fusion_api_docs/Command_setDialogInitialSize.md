# Command.setDialogInitialSize Method

Parent Object: [Command](Command.md)  

## Description

Sets the initial size of the dialog when it is first displayed. If this is not set, Fusion will use a default size for the dialog.

## Syntax

"command_var" is a variable referencing a [Command](Command.md) object.

```python
returnValue = command_var.setDialogInitialSize(width, height)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if the default size was successfully set. |

## Parameters

| Name   | Type    | Description                         |
|--------|---------|-------------------------------------|
| width  | integer | The width of the dialog in pixels.  |
| height | integer | The height of the dialog in pixels. |

## Version

Introduced in version June 2015  

