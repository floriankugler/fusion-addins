# CustomGraphicsEntity.setOpacity Method

Parent Object: [CustomGraphicsEntity](CustomGraphicsEntity.md)  

## Description

Sets the opacity of the graphics entity. By default, when a new entity is it is completely opaque and does not override the opacity defined by the material.

## Syntax

"customGraphicsEntity_var" is a variable referencing a [CustomGraphicsEntity](CustomGraphicsEntity.md) object.

```python
returnValue = customGraphicsEntity_var.setOpacity(opacity, isOverride)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if setting the opacity information was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| opacity | double | The opacity value where 1.0 is completely opaque and 0.0 is completely transparent. |
| isOverride | boolean | Indicates if this entities opacity will override the opacity defined by the material. If true, it will override the material opacity and if false the opacity values will accumulate. |

## Version

Introduced in version September 2017  

