# CustomFeature.customNamedValues Property

Parent Object: [CustomFeature](CustomFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the set of custom named values associated with this custom feature. These are a set of named values that are saved with this feature that you can use to save any additional information that is useful for you in managing the custom feature. For example, you might have a setting like an option for different shapes that the user chooses when creating the feature that are not represented as a parameter. You can use this to save the chosen value so when the feature is computed or edited you can use the value originally chosen. During an edit, you might allow the user to edit this setting and you can update the saved custom value.

## Syntax

"customFeature_var" is a variable referencing a CustomFeature object.  

```python
# Get the value of the property.
propertyValue = customFeature_var.customNamedValues
```

## Property Value

This is a read only property whose value is a [CustomNamedValues](CustomNamedValues.md).

## Version

Introduced in version July 2021  

