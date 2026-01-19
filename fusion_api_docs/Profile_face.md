# Profile.face Property

Parent Object: [Profile](Profile.md)  

## Description

Returns a temporary BRepFace object that is the same shape as the profile. The geometry of the returned face is defined in the 3D space of the parent sketch of the profile.  

This can be useful when wanting to use a profile in conjunction with the TemporaryBRepManager object to create B-Rep objects.

## Syntax

"profile_var" is a variable referencing a Profile object.  

```python
# Get the value of the property.
propertyValue = profile_var.face
```

## Property Value

This is a read only property whose value is a [BRepFace](BRepFace.md).

## Version

Introduced in version March 2024  

