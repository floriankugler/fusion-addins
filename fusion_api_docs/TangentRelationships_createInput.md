# TangentRelationships.createInput Method

Parent Object: [TangentRelationships](TangentRelationships.md)  

## Description

Creates a TangentRelationshipInput object, which is the API equivalent to the Tangent Relationship command dialog. You use methods and properties on the returned class to set the desired options, similar to providing input in the Tangent Relationship command dialog. Once the settings are defined you call the TangentRelationships.add method passing in the TangentRelationshipInput object to create the actual TangentRelationship.

## Syntax

"tangentRelationships_var" is a variable referencing a [TangentRelationships](TangentRelationships.md) object.

```python
returnValue = tangentRelationships_var.createInput(faceOne, tangentFaces)
```

## Return Value

| Type | Description |
|----|----|
| [TangentRelationshipInput](TangentRelationshipInput.md) | Returns the TangentRelationshipInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| faceOne | [BRepFace](BRepFace.md) | A BRepFace object that will remain tangent to the set of specified tangent faces. |
| tangentFaces | [Base](Base.md) | A single BRepFace object that is part of the body that faceOne will remain tangent to. All of the faces of the body will be used when computing the tangent relationship. |

## Version

Introduced in version May 2022  

