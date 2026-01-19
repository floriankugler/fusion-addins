# MeshCombineFaceGroupsFeature.entityToken Property

Parent Object: [MeshCombineFaceGroupsFeature](MeshCombineFaceGroupsFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature.  

When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them.

## Syntax

"meshCombineFaceGroupsFeature_var" is a variable referencing a MeshCombineFaceGroupsFeature object.  

```python
# Get the value of the property.
propertyValue = meshCombineFaceGroupsFeature_var.entityToken
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version January 2025  

