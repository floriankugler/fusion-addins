# Decal.imageFilename Property

Parent Object: [Decal](Decal.md)  

## Description

Gets and sets the filename of the image used for the decal. When getting this property, the filename returned is the file that was used when the decal was initially created. it's possible the file may no longer exist.  

When setting this property, it is the full filename to the image to use for the decal. PNG, JPEG, and TIFF files are supported.

## Syntax

"decal_var" is a variable referencing a Decal object.  

```python
# Get the value of the property.
propertyValue = decal_var.imageFilename

# Set the value of the property.
decal_var.imageFilename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2024  

