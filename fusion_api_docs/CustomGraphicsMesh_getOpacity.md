# CustomGraphicsMesh.getOpacity Method

Parent Object: [CustomGraphicsMesh](CustomGraphicsMesh.md)  

## Description

Gets the opacity of the graphics entity.

## Syntax

"customGraphicsMesh_var" is a variable referencing a [CustomGraphicsMesh](CustomGraphicsMesh.md) object.  

```python
(returnValue, opacity, isOverride) = customGraphicsMesh_var.getOpacity()
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if getting the opacity information was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| opacity | double | The opacity value where 1.0 is completely opaque and 0.0 is completely transparent. |
| isOverride | boolean | Indicates if this entities opacity will override the opacity defined by the material. If true, it will override the material opacity and if false the opacity values will accumulate. |

## Version

Introduced in version September 2017  

