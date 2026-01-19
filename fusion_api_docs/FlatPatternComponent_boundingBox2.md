# FlatPatternComponent.boundingBox2 Method

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns the bounding box of the specified entity types within the component.

## Syntax

"flatPatternComponent_var" is a variable referencing a [FlatPatternComponent](FlatPatternComponent.md) object.

```python
returnValue = flatPatternComponent_var.boundingBox2(entityTypes)
```

## Return Value

| Type | Description |
|----|----|
| [BoundingBox3D](BoundingBox3D.md) | Returns a BoundingBox3D object if the calculation was successful and null in the case where there is no valid geometry and the bounding box is empty. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entityTypes | [BoundingBoxEntityTypes](BoundingBoxEntityTypes.md) | Bitwise value that specifies the types of entities to include in the calculation of the bounding box. |

## Version

Introduced in version January 2024  

