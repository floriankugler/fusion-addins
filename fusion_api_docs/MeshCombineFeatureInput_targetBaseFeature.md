# MeshCombineFeatureInput.targetBaseFeature Property

Parent Object: [MeshCombineFeatureInput](MeshCombineFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature.  

Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it.

## Syntax

"meshCombineFeatureInput_var" is a variable referencing a MeshCombineFeatureInput object.  

```python
# Get the value of the property.
propertyValue = meshCombineFeatureInput_var.targetBaseFeature

# Set the value of the property.
meshCombineFeatureInput_var.targetBaseFeature = propertyValue
```

## Property Value

This is a read/write property whose value is a [BaseFeature](BaseFeature.md).

## Version

Introduced in version January 2025  

