# SVGImportOptions.isViewFit Property

Parent Object: [SVGImportOptions](SVGImportOptions.md)  

## Description

Specifies if the camera should be adjusted to fit the geometry of the import. This defaults to true, which will cause a change in the current view. Setting this to false will leave the view as-is and just import the geometry.

## Syntax

"sVGImportOptions_var" is a variable referencing a SVGImportOptions object.  

```python
# Get the value of the property.
propertyValue = sVGImportOptions_var.isViewFit

# Set the value of the property.
sVGImportOptions_var.isViewFit = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version October 2022  

