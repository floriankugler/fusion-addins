# CustomFeatureParameter.isVisible Property

Parent Object: [CustomFeatureParameter](CustomFeatureParameter.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets if this parameter is visible in the parameters dialog. By default, all new parameters are visible.  

This can be useful in cases where the feature can be edited to be in different states where a parameter is only valid in a certain state. You can change the visibility based on the current state of the feature and if that parameter should be available for edit. This implies that you create all the parameters that might be needed and then change their visibility based on the current state of the feature. The parameters that are not visible will not be returned by the ModelParameters collection and are only available through the custom feature they're associated with.

## Syntax

"customFeatureParameter_var" is a variable referencing a CustomFeatureParameter object.  

```python
# Get the value of the property.
propertyValue = customFeatureParameter_var.isVisible

# Set the value of the property.
customFeatureParameter_var.isVisible = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2021  

