# Feature.faces Property

Parent Object: [Feature](Feature.md)  

## Description

Returns the faces that were created by this feature. This works for both parametric and non-parametric features.  

Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available.

## Syntax

"feature_var" is a variable referencing a Feature object.  

```python
# Get the value of the property.
propertyValue = feature_var.faces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version August 2014  

