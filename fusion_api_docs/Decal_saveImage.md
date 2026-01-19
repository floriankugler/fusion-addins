# Decal.saveImage Method

Parent Object: [Decal](Decal.md)  

## Description

Saves the image associated with the decal to the specified file. This is useful in cases where the original image file is no longer available but you need the image for some other purpose.

## Syntax

"decal_var" is a variable referencing a [Decal](Decal.md) object.

```python
returnValue = decal_var.saveImage(filename)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if writing the file was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The full filename of the image to save, including the extension of the file, which controls what format the image file will be. If file extension is other than png, jpg or tiff, then by default png extension will be added to the filename. This method will fail if a file with the specified filename already exists. If you want to overwrite the file, you'll need to delete it first before calling this method. |

## Version

Introduced in version September 2024  

