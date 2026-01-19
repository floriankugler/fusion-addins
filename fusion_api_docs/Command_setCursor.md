# Command.setCursor Method

Parent Object: [Command](Command.md)  

## Description

Specifies the cursor to display at the mouse.

## Syntax

"command_var" is a variable referencing a [Command](Command.md) object.

```python
returnValue = command_var.setCursor(cursorImage, xHotSpot, yHotSpot)
```

## Return Value

| Type    | Description                                        |
|---------|----------------------------------------------------|
| boolean | Returns true if setting the cursor was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| cursorImage | string | The path to the PNG image to display as the cursor. This can either be a relative path from the py, dll, or dylib file of the full path. Specifying an empty string will set the cursor back to the default cursor. |
| xHotSpot | integer | Specifies the position of the x pixel within the image that is the "hot" spot or the point that is used as the mouse point. A value of zero indicates the far left of the image. If an empty string is used as the cursorImage, this value is ignored. |
| yHotSpot | integer | Specifies the position of the y pixel within the image that is the "hot" spot or the point that is used as the mouse point. A value of zero indicates the top of the image. If an empty string is used as the cursorImage, this value is ignored. |

## Version

Introduced in version April 2019  

