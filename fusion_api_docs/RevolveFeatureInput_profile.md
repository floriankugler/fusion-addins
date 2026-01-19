# RevolveFeatureInput.profile Property

Parent Object: [RevolveFeatureInput](RevolveFeatureInput.md)  

## Description

Gets and sets the profiles or planar faces used to define the shape of the revolve. This property can return or be set with a single Profile, a single planar face, or an ObjectCollection consisting of multiple profiles and planar faces. When an ObjectCollection is used all of the profiles and faces must be co-planar. This property returns null in the case where the feature is non-parametric.  

To create a surface (non-solid) revolution, you can use the createOpenProfile and createBRepEdgeProfile methods of the Component object to create an open profile. The isSolid property of the RevolveFeatureInput property must also be False.

## Syntax

"revolveFeatureInput_var" is a variable referencing a RevolveFeatureInput object.  

```python
# Get the value of the property.
propertyValue = revolveFeatureInput_var.profile

# Set the value of the property.
revolveFeatureInput_var.profile = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

