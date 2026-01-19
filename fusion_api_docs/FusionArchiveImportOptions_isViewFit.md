# FusionArchiveImportOptions.isViewFit Property

Parent Object: [FusionArchiveImportOptions](FusionArchiveImportOptions.md)  

## Description

Specifies if the camera should be adjusted to fit the geometry of the import. This defaults to true, which will cause a change in the current view. Setting this to false will leave the view as-is and just import the geometry.

## Syntax

"fusionArchiveImportOptions_var" is a variable referencing a FusionArchiveImportOptions object.  

```python
# Get the value of the property.
propertyValue = fusionArchiveImportOptions_var.isViewFit

# Set the value of the property.
fusionArchiveImportOptions_var.isViewFit = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2017  

