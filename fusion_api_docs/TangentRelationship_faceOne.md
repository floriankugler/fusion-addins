# TangentRelationship.faceOne Property

Parent Object: [TangentRelationship](TangentRelationship.md)  

## Description

Gets and sets the first BRepFace object that will remain tangent to the set of specified tangent faces.  

To set this property, you need to position the timeline marker to immediately before this tangent relationship. This can be accomplished using the following code: thisTangentRelationship.timelineObject.rollTo(True)

## Syntax

"tangentRelationship_var" is a variable referencing a TangentRelationship object.  

```python
# Get the value of the property.
propertyValue = tangentRelationship_var.faceOne

# Set the value of the property.
tangentRelationship_var.faceOne = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version May 2022  

