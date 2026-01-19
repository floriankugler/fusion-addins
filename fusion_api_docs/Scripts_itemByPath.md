# Scripts.itemByPath Method

Parent Object: [Scripts](Scripts.md)  

## Description

Function that returns the script that is located in the specified folder.

## Syntax

"scripts_var" is a variable referencing a [Scripts](Scripts.md) object.

```python
returnValue = scripts_var.itemByPath(folderPath)
```

## Return Value

| Type | Description |
|----|----|
| [Script](Script.md) | Returns the specified script or null if there isn't a script at the specified path. |

## Parameters

| Name | Type | Description |
|----|----|----|
| folderPath | string | The full path to the folder that contains the script. This does not include the name of the script, but only the path. For example "C:\Scripts\MyScript" is valid where "C:\Scripts\MyScripts\MyScript.py" is not. |

## Version

Introduced in version July 2024  

