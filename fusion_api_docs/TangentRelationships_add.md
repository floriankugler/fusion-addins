# TangentRelationships.add Method

Parent Object: [TangentRelationships](TangentRelationships.md)  

## Description

Creates a new tangent relationship between two components.

## Syntax

"tangentRelationships_var" is a variable referencing a [TangentRelationships](TangentRelationships.md) object.

```python
returnValue = tangentRelationships_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [TangentRelationship](TangentRelationship.md) | Returns the newly created TangentRelationship or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [TangentRelationshipInput](TangentRelationshipInput.md) | The TangentRelationshipInput object that defines the geometry and various inputs that fully define a tangent relationship. A TangentRelationshipInput object is created using the TangentRelationships.createInput method. |

## Version

Introduced in version May 2022  

