# MaterialLibraries.load Method

Parent Object: [MaterialLibraries](MaterialLibraries.md)  

## Description

Loads the specified existing local material library. Fusion remembers which libraries have been loaded from one session to the next so you should check to see if the local library is already loaded or not before loading it again.

## Syntax

"materialLibraries_var" is a variable referencing a [MaterialLibraries](MaterialLibraries.md) object.

```python
returnValue = materialLibraries_var.load(filename)
```

## Return Value

| Type | Description |
|----|----|
| [MaterialLibrary](MaterialLibrary.md) | Returns the MaterialLibrary object representing the opened library or null in the case of failure. |

## Parameters

| Name     | Type   | Description                                      |
|----------|--------|--------------------------------------------------|
| filename | string | The full filename of the .adsklib material file. |

## Version

Introduced in version March 2017  

