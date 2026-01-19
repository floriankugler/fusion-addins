# Materials.itemByName Method

Parent Object: [Materials](Materials.md)  

## Description

Returns the specified Material using the name as seen in the user interface. This often isn't a reliable way of accessing a specific material because materials are not required to be unique.

## Syntax

"materials_var" is a variable referencing a [Materials](Materials.md) object.

```python
returnValue = materials_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Material](Material.md) | Returns the specified material or null if there isn't a matching name. |

## Parameters

| Name | Type   | Description                          |
|------|--------|--------------------------------------|
| name | string | The name of the material to return,. |

## Version

Introduced in version August 2014  

