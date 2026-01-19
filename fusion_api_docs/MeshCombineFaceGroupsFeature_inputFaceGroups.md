# MeshCombineFaceGroupsFeature.inputFaceGroups Property

Parent Object: [MeshCombineFaceGroupsFeature](MeshCombineFaceGroupsFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the input face groups, which should be combined. They need to belong to the same mesh body.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"meshCombineFaceGroupsFeature_var" is a variable referencing a MeshCombineFaceGroupsFeature object.  

```python
# Get the value of the property.
propertyValue = meshCombineFaceGroupsFeature_var.inputFaceGroups

# Set the value of the property.
meshCombineFaceGroupsFeature_var.inputFaceGroups = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [FaceGroup](FaceGroup.md).

## Version

Introduced in version January 2025  

