# MeshCombineFaceGroupsFeatures.objectType Property

Parent Object: [MeshCombineFaceGroupsFeatures](MeshCombineFaceGroupsFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object.  

It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType():

## Syntax

"meshCombineFaceGroupsFeatures_var" is a variable referencing a MeshCombineFaceGroupsFeatures object.  

```python
# Get the value of the property.
propertyValue = meshCombineFaceGroupsFeatures_var.objectType
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version January 2025  

