# MaterialLibraries.itemByName Method

Parent Object: [MaterialLibraries](MaterialLibraries.md)  

## Description

Returns the specified Material Library using the name as seen in the user interface.

## Syntax

"materialLibraries_var" is a variable referencing a [MaterialLibraries](MaterialLibraries.md) object.

```python
returnValue = materialLibraries_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [MaterialLibrary](MaterialLibrary.md) | Returns the specified material library or null if there's no match on the name. |

## Parameters

| Name | Type   | Description                        |
|------|--------|------------------------------------|
| name | string | The name of the library to return. |

## Version

Introduced in version August 2014  

