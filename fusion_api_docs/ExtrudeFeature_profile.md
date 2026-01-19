# ExtrudeFeature.profile Property

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Gets and sets the profiles or planar faces used to define the shape of the extrude. This property can return or be set with a single Profile, a single planar face, or an ObjectCollection consisting of multiple profiles and planar faces. When an ObjectCollection is used all of the profiles and faces must be co-planar.  

When setting this property of a surface (non-solid) extrusion, you can use the createOpenProfile and createBRepEdgeProfile methods of the Component object to create an open profile.  

This property returns null in the case where the feature is non-parametric.

## Syntax

"extrudeFeature_var" is a variable referencing an ExtrudeFeature object.  

```python
# Get the value of the property.
propertyValue = extrudeFeature_var.profile

# Set the value of the property.
extrudeFeature_var.profile = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

