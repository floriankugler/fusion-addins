# Scripts.addExisting Method

Parent Object: [Scripts](Scripts.md)  

## Description

Fusion looks in specific folders for scripts and add-ins, but you can manually add other scripts and add-ins to the list of known scripts and add-ins so they will be listed in the "Scripts and Add-ins" dialog. This method does that.

## Syntax

"scripts_var" is a variable referencing a [Scripts](Scripts.md) object.

```python
returnValue = scripts_var.addExisting(scriptFolderPath)
```

## Return Value

| Type | Description |
|----|----|
| [Script](Script.md) | Returns the Script object that represents the script or add-in just added. Returns null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| scriptFolderPath | string | The full path to the folder that contains the script or add-in. |

## Version

Introduced in version October 2023  

