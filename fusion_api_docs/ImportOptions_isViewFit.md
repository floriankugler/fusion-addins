# ImportOptions.isViewFit Property

Parent Object: [ImportOptions](ImportOptions.md)  

## Description

Specifies if the camera should be adjusted to fit the geometry of the import. This defaults to true, which will cause a change in the current view. Setting this to false will leave the view as-is and just import the geometry.

## Syntax

"importOptions_var" is a variable referencing an ImportOptions object.  

```python
# Get the value of the property.
propertyValue = importOptions_var.isViewFit

# Set the value of the property.
importOptions_var.isViewFit = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version May 2017  

