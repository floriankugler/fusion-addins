# SVGImportOptions.transform Property

Parent Object: [SVGImportOptions](SVGImportOptions.md)  

## Description

Gets and sets the transformation matrix that defines the position, orientation, scale, and mirroring of the imported SVG data relative to the sketch coordinate system. This property defaults to an identity matrix in a newly created SVGImportOptions object.  

You can define mirroring (the equivalent of horizontal or vertical flip) in the matrix. Doing this gives you more explicit control over the results. You can also use the isHorizontalFlip and isVerticalFlop properties to define the flip. These result in flipping the geometry along the center of the geometry's bounding box.

## Syntax

"sVGImportOptions_var" is a variable referencing a SVGImportOptions object.  

```python
# Get the value of the property.
propertyValue = sVGImportOptions_var.transform

# Set the value of the property.
sVGImportOptions_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version October 2022  

