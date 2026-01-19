# Decal.faces Property

Parent Object: [Decal](Decal.md)  

## Description

Gets the faces the decal is associated with. Typically, this is an array containing a single face. If the isChainFaces property is true, this will return the primary face. If the isChainFaces property is false, the decal is limited to the faces in this list.  

If multiple faces have been provided, the first face in the list is the primary face, which is used to position and orient the decal.  

To set the faces, use the redefine method.

## Syntax

"decal_var" is a variable referencing a Decal object.  

```python
# Get the value of the property.
propertyValue = decal_var.faces
```

## Property Value

This is a read only property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version September 2024  

