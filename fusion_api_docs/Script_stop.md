# Script.stop Method

Parent Object: [Script](Script.md)  

## Description

If this script or add-in is running, this method will stop it. The isRunning property can be used to determine if it is running. If the script or add-in is not running and this method is called, there is no effect.

## Syntax

"script_var" is a variable referencing a [Script](Script.md) object.

```python
returnValue = script_var.stop()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Version

Introduced in version October 2023  

