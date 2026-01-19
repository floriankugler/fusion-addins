# CustomFeature.linkedFeatures Property

Parent Object: [CustomFeature](CustomFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface.

## Syntax

"customFeature_var" is a variable referencing a CustomFeature object.  

```python
# Get the value of the property.
propertyValue = customFeature_var.linkedFeatures
```

## Property Value

This is a read only property whose value is a [FeatureList](FeatureList.md).

## Version

Introduced in version January 2021  

