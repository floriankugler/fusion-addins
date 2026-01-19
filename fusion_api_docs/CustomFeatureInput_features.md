# CustomFeatureInput.features Property

Parent Object: [CustomFeatureInput](CustomFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the features that are grouped by this custom feature. The start and end features and all of the features between them in the timeline are returned. This includes all entities represented in the timeline including modeling features, construction geometry, sketches, etc.

## Syntax

"customFeatureInput_var" is a variable referencing a CustomFeatureInput object.  

```python
# Get the value of the property.
propertyValue = customFeatureInput_var.features
```

## Property Value

This is a read only property whose value is an array of type [Base](Base.md).

## Version

Introduced in version January 2021  

