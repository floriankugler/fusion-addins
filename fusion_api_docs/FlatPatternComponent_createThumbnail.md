# FlatPatternComponent.createThumbnail Method

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Creates a thumbnail for this component. This can be a root component to get a thumbnail that represents the associated file, or it can be any sub component to get a thumbnail of a subset of the complete assembly or individual parts.

## Syntax

"flatPatternComponent_var" is a variable referencing a [FlatPatternComponent](FlatPatternComponent.md) object.

```python
# Uses no optional arguments.
returnValue = flatPatternComponent_var.createThumbnail()

# Uses optional arguments.
returnValue = flatPatternComponent_var.createThumbnail(width, height, imageType)
```

## Return Value

| Type | Description |
|----|----|
| [DataObject](DataObject.md) | Returns a DataObject that you can use to save the thumbnail to a file or to access the binary data of the bitmap directly. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| width | integer | Optional argument to define the width of the thumbnail in pixels. A default width of 256 pixels is used if no width is specified. This is an optional argument whose default value is 256. |
| height | integer | Optional argument to define the height of the thumbnail in pixels. A default height of 256 pixels is used if no height is specified. This is an optional argument whose default value is 256. |
| imageType | string | Optional argument to define the type of image data to create. The default of PNG is used if no type is specified. Valid types include "PNG", "JPG", "TIF", and "BMP". This is an optional argument whose default value is "PNG". |

## Version

Introduced in version November 2024  

