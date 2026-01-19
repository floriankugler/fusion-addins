# CustomFeatureParameter.textValue Property

Parent Object: [CustomFeatureParameter](CustomFeatureParameter.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the value of the parameter when it is a text parameter. This can be determined by checking the valueType property. Setting this value will cause the current expression to be overwritten. If the parameter is not a text parameter, the value of this property should be ignored and setting will fail.

## Syntax

"customFeatureParameter_var" is a variable referencing a CustomFeatureParameter object.  

```python
# Get the value of the property.
propertyValue = customFeatureParameter_var.textValue

# Set the value of the property.
customFeatureParameter_var.textValue = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2025  

