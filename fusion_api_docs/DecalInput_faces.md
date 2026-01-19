# DecalInput.faces Property

Parent Object: [DecalInput](DecalInput.md)  

## Description

Gets and sets the faces the decal will be associated with. Typically, this will be an array containing a single face and the isChainFaces property on the input will be true. The position and orientation of the decal is based on this face and the decal can wrap onto other faces in the body.  

If the isChainFace property is false, the decal will only be applied to the provided faces where the first face is used to calculate the position and orientation of the decal.

## Syntax

"decalInput_var" is a variable referencing a DecalInput object.  

```python
# Get the value of the property.
propertyValue = decalInput_var.faces

# Set the value of the property.
decalInput_var.faces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version September 2024  

