# SaveImageFileOptions.create Method

Parent Object: [SaveImageFileOptions](SaveImageFileOptions.md)  

## Description

Creates a new SaveImageFileOptions object. The returned object can be used to define the various options to use when saving a viewport as an image. The object is passed into the ViewPort.saveAsImageFileWithOptions method to create an image of the viewport.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.SaveImageFileOptions.create(filename)
```

## Return Value

| Type | Description |
|----|----|
| [SaveImageFileOptions](SaveImageFileOptions.md) | Returns a SaveImageFileOptions object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The full filename, including the path, of the image file. The type of image file to be created is inferred from the extension of the filename. |

## Version

Introduced in version May 2022  

