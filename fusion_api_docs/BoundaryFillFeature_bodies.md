# BoundaryFillFeature.bodies Property

Parent Object: [BoundaryFillFeature](BoundaryFillFeature.md)  

## Description

Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features.  

For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies.  

When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations.  

You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available.

## Syntax

"boundaryFillFeature_var" is a variable referencing a BoundaryFillFeature object.  

```python
# Get the value of the property.
propertyValue = boundaryFillFeature_var.bodies
```

## Property Value

This is a read only property whose value is a [BRepBodies](BRepBodies.md).

## Version

Introduced in version June 2015  

