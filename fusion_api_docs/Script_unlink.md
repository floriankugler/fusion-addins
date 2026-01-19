# Script.unlink Method

Parent Object: [Script](Script.md)  

## Description

Unlinks this script or add-in. This removes it from Fusion's list of linked scripts and add-ins, so it is no longer displayed in the dialog, and if it's an add-in, it will no longer run on startup.  

This is only valid for a script or add-in that is linked; the sourceLocation property returns LinkedScriptSourceLocation.

## Syntax

"script_var" is a variable referencing a [Script](Script.md) object.

```python
returnValue = script_var.unlink()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the unlink was successful. |

## Version

Introduced in version January 2025  

