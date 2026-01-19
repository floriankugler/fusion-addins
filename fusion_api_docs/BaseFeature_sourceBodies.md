# BaseFeature.sourceBodies Property

Parent Object: [BaseFeature](BaseFeature.md)  

## Description

Returns the B-Rep bodies owned by the base feature.  

When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. The result bodies can be obtained by using the bodies property of the BaseFeature object.  

You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available.

## Syntax

"baseFeature_var" is a variable referencing a BaseFeature object.  

```python
# Get the value of the property.
propertyValue = baseFeature_var.sourceBodies
```

## Property Value

This is a read only property whose value is an array of type [BRepBody](BRepBody.md).

## Version

Introduced in version October 2022  

