# CustomFeatureDefinition.editCommandId Property

Parent Object: [CustomFeatureDefinition](CustomFeatureDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets which command will be invoked when the feature is edited. This is the id of the CommandDefinition object that you have created to do the edit of the feature.

## Syntax

"customFeatureDefinition_var" is a variable referencing a CustomFeatureDefinition object.  

```python
# Get the value of the property.
propertyValue = customFeatureDefinition_var.editCommandId

# Set the value of the property.
customFeatureDefinition_var.editCommandId = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2021  

