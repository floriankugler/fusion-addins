# CustomFeatureParameter.name Property

Parent Object: [CustomFeatureParameter](CustomFeatureParameter.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the name of the parameter. Setting the name can fail if the name is not unique with respect to all other parameters in the design.

## Syntax

"customFeatureParameter_var" is a variable referencing a CustomFeatureParameter object.  

```python
# Get the value of the property.
propertyValue = customFeatureParameter_var.name

# Set the value of the property.
customFeatureParameter_var.name = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2021  

