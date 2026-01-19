# Command.getCursor Method

Parent Object: [Command](Command.md)  

## Description

Gets the custom cursor information currently being used.

## Syntax

"command_var" is a variable referencing a [Command](Command.md) object.  

```python
(returnValue, cursorImage, xHotSpot, yHotSpot) = command_var.getCursor()
```

## Return Value

| Type    | Description                                                    |
|---------|----------------------------------------------------------------|
| boolean | Returns true if getting the cursor information was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| cursorImage | string | The full path to the png image that is being displayed as the cursor. |
| xHotSpot | integer | Gets the position of the x pixel within the image that is the "hot" spot or the point that is used as the mouse point. A value of zero indicates the left of the image. |
| yHotSpot | integer | Gets the position of the y pixel within the image that is the "hot" spot or the point that is used as the mouse point. A value of zero indicates the top of the image. |

## Version

Introduced in version April 2019  

