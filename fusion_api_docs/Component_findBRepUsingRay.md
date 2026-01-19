# Component.findBRepUsingRay Method

Parent Object: [Component](Component.md)  

## Description

Finds all the B-Rep entities that are intersected by the specified ray. This can return BRepFace, BrepEdge, and BRepVertex objects.

## Syntax

"component_var" is a variable referencing a [Component](Component.md) object.

```python
# Uses no optional arguments.
returnValue = component_var.findBRepUsingRay(originPoint, rayDirection, entityType)

# Uses optional arguments.
returnValue = component_var.findBRepUsingRay(originPoint, rayDirection, entityType, proximityTolerance, visibleEntitiesOnly, hitPoints)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns an ObjectCollection containing the entities found. The returned collection can be empty indicating nothing was found. The points are returned in an order where they are arranged based on their distance from the origin point where the closest point is first. If an entity is hit more than once, the entity is returned once for the first intersection. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| originPoint | [Point3D](Point3D.md) | Input point that defines the origin of the ray. The search for entities begins at this point. |
| rayDirection | [Vector3D](Vector3D.md) | Input vector that defines the direction of the ray. The ray is infinite so the length of the vector is ignored. |
| entityType | [BRepEntityTypes](BRepEntityTypes.md) | The type of B-Rep entity wanted. You can also take advantage of B-Rep topology to infer other intersections. For example, If you get a BRepEdge it implies that the faces the edge connects were also intersected. If a BRepVertex is returned it implies the edges that the vertex connects were intersected and the faces that the edges connect were intersected. |
| proximityTolerance | double | Optional argument that specifies the tolerance for the search. All entities within this distance from the ray and of the specified type will be returned. If not specified a default small tolerance is used. This is an optional argument whose default value is -1.0. |
| visibleEntitiesOnly | boolean | Optional argument that indicates whether or not invisible entities should be included in the search. Defaults to True indicating that invisible entities will be ignored. This is an optional argument whose default value is True. |
| hitPoints | [ObjectCollection](ObjectCollection.md) | An ObjectCollection of Point3D objects that represent the coordinates where the ray hit the found entity. There will be the same number of hit points as returned entities and they will be in the collections in the same order. In other words, hit point 1 corresponds with found entity 1, hit point 2 corresponds with found entity 2, and so on. Because of the proximity tolerance the hitPoint may not actually lie on the entity but will be within the proximity tolerance to it. It's an optional out argument, returns the hit points if an existing ObjectCollection is input. You can create a new ObjectCollection by using the static create method on the ObjectCollection class. This is an optional argument whose default value is null. |

## Version

Introduced in version December 2016  

