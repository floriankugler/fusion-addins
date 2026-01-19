# Material.copyTo Method

Parent Object: [Material](Material.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Copies this material to the specified target.

## Remarks

This method has been retired and replaced by the addByCopyMethod on the Materials object.

## Syntax

"material_var" is a variable referencing a [Material](Material.md) object.

```python
returnValue = material_var.copyTo(target)
```

## Return Value

| Type | Description |
|----|----|
| [Material](Material.md) | Returns the new copy of the material or null if the copy failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| target | [Base](Base.md) | The target can be a Design or MaterialFavorites object. |

## Version

Introduced in version August 2014  
Retired in version July 2023  

