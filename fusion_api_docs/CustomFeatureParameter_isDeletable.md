# CustomFeatureParameter.isDeletable Property

Parent Object: [CustomFeatureParameter](CustomFeatureParameter.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets if this parameter can be deleted. Parameters that have dependents cannot be deleted, and model parameters typically cannot be deleted. However, there is the possibility in uncommon workflows where a model parameter no longer has any dependents, and it was not automatically deleted. In this case, this property will return true, and the deleteMe method can delete the parameter.

## Syntax

"customFeatureParameter_var" is a variable referencing a CustomFeatureParameter object.  

```python
# Get the value of the property.
propertyValue = customFeatureParameter_var.isDeletable
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2021  

