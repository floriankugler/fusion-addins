# CustomFeatureParameter.value Property

Parent Object: [CustomFeatureParameter](CustomFeatureParameter.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the real value (a double) of the parameter in database units. Setting this property will set/reset the expression value for this parameter.  

This property is only valid for numeric parameters and will fail for text parameters. You can determine the value type of the parameter by using the valueType property. Use the textValue property to get and set the value of text parameters.

## Syntax

"customFeatureParameter_var" is a variable referencing a CustomFeatureParameter object.  

```python
# Get the value of the property.
propertyValue = customFeatureParameter_var.value

# Set the value of the property.
customFeatureParameter_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2021  

