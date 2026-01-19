# TangentRelationship.tangentFaces Property

Parent Object: [TangentRelationship](TangentRelationship.md)  

## Description

Gets and sets a single BRepFace object that is part of the body that faceOne will remain tangent to. All of the faces of the body will be used when computing the tangent relationship.  

To set this property, you need to position the timeline marker to immediately before this tangent relationship. This can be accomplished using the following code: thisTangentRelationship.timelineObject.rollTo(True)

## Syntax

"tangentRelationship_var" is a variable referencing a TangentRelationship object.  

```python
# Get the value of the property.
propertyValue = tangentRelationship_var.tangentFaces

# Set the value of the property.
tangentRelationship_var.tangentFaces = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version May 2022  

