# MaterialLibraries.item Method

Parent Object: [MaterialLibraries](MaterialLibraries.md)  

## Description

Method that returns the specified Material Library using an index into the collection.

## Syntax

"materialLibraries_var" is a variable referencing a [MaterialLibraries](MaterialLibraries.md) object.

```python
returnValue = materialLibraries_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [MaterialLibrary](MaterialLibrary.md) | Returns the specified material library or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the item within the collection. The first item has an index of 0. |

## Version

Introduced in version August 2014  

