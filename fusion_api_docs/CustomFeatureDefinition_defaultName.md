# CustomFeatureDefinition.defaultName Property

Parent Object: [CustomFeatureDefinition](CustomFeatureDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the default name of the feature. Fusion will use this name and append a number to each feature instance as it's created. For example, if this is "Dovetail" the first custom feature created will be named "Dovetail1" and the second will be "Dovetail2".  

If you want to localize this name you can use the Application.Preferences.generalPreferences.userLanguage property to determine what language the user has chosen and use the corresponding name for that language.

## Syntax

"customFeatureDefinition_var" is a variable referencing a CustomFeatureDefinition object.  

```python
# Get the value of the property.
propertyValue = customFeatureDefinition_var.defaultName

# Set the value of the property.
customFeatureDefinition_var.defaultName = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2021  

