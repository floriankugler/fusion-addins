# MeshCombineFaceGroupsFeature.bodies Property

Parent Object: [MeshCombineFaceGroupsFeature](MeshCombineFaceGroupsFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features.  

For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies.  

When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations.  

You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available.

## Syntax

"meshCombineFaceGroupsFeature_var" is a variable referencing a MeshCombineFaceGroupsFeature object.  

```python
# Get the value of the property.
propertyValue = meshCombineFaceGroupsFeature_var.bodies
```

## Property Value

This is a read only property whose value is a [BRepBodies](BRepBodies.md).

## Version

Introduced in version January 2025  

