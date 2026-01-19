# Materials.addByCopy Method

Parent Object: [Materials](Materials.md)  

## Description

Add a Material to a Design by copying an existing Material from Favorites, a Library or from the Materials stored in the Design. This method currently only applies to the Materials collection from a Design and cannot be used to copy a Material to a library.

## Syntax

"materials_var" is a variable referencing a [Materials](Materials.md) object.

```python
returnValue = materials_var.addByCopy(materialToCopy, name)
```

## Return Value

| Type | Description |
|----|----|
| [Material](Material.md) | Returns the newly created Material or null if the copy operation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| materialToCopy | [Material](Material.md) | The Material you want to copy. The Material to copy can be from Favorites, a Library or from the materials stored in the Design. |
| name | string | The Material name to apply to the copy. |

## Version

Introduced in version January 2016  

