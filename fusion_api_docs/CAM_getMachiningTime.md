# CAM.getMachiningTime Method

Parent Object: [CAM](CAM.md)  

## Description

Get the machining time for the specified objects.

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
returnValue = cAM_var.getMachiningTime(operations, feedScale, rapidFeed, toolChangeTime)
```

## Return Value

| Type | Description |
|----|----|
| [MachiningTime](MachiningTime.md) | Returns a MachiningTime object that has properties holding the calculation results. |

## Parameters

| Name | Type | Description |
|----|----|----|
| operations | [Base](Base.md) | An Operation, Setup, Folder, or Pattern object. You can also use an ObjectCollection to specify multiple objects of any of the supported types. |
| feedScale | double | The feed scale value (%) to use. |
| rapidFeed | double | The rapid feed rate in centimeters per second. |
| toolChangeTime | double | The tool change time in seconds. |

## Version

Introduced in version September 2017  

