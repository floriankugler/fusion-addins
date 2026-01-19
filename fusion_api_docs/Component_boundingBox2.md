# Component.boundingBox2 Method

Parent Object: [Component](Component.md)  

## Description

Returns the bounding box of the specified entity types within the component.

## Syntax

"component_var" is a variable referencing a [Component](Component.md) object.

```python
returnValue = component_var.boundingBox2(entityTypes)
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

