# Scripts.itemsByName Method

Parent Object: [Scripts](Scripts.md)  

## Description

Function that returns an array of scripts that have the specified name. In most cases this will return an array containing a single script, but it's possible to have more than one script with the same name in the case where the scripts are in different folders.

## Syntax

"scripts_var" is a variable referencing a [Scripts](Scripts.md) object.

```python
returnValue = scripts_var.itemsByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Script](Script.md)\[\] | Returns the scripts with the specified name or an empty array if there aren't any scripts with that name. |

## Parameters

| Name | Type   | Description                    |
|------|--------|--------------------------------|
| name | string | The script name to search for. |

## Version

Introduced in version July 2024  

