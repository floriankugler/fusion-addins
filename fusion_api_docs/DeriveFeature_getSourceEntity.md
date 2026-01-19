# DeriveFeature.getSourceEntity Method

Parent Object: [DeriveFeature](DeriveFeature.md)  

## Description

Method that returns the source entity for a derived entity.

## Syntax

"deriveFeature_var" is a variable referencing a [DeriveFeature](DeriveFeature.md) object.

```python
returnValue = deriveFeature_var.getSourceEntity(derivedEntity)
```

## Return Value

| Type | Description |
|----|----|
| [Base](Base.md) | Returns the source entity for the derived entity or null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| derivedEntity | [Base](Base.md) | Input an entity (e.g. a BRepBody, MeshBody, Sketch, SketchEntity, ConstructionPlane, Occurrence, Canvas etc.) that was derived by this DeriveFeature. |

## Version

Introduced in version January 2026  

