# Canvas.saveImage Method

Parent Object: [Canvas](Canvas.md)  

## Description

Saves the image associated with the canvas to the specified file. This is useful in cases where the original image file is no longer available but you need the image for some other purpose.

## Syntax

"canvas_var" is a variable referencing a [Canvas](Canvas.md) object.

```python
returnValue = canvas_var.saveImage(filename)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if writing the file was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| filename | string | The full filename of the image to save, including the file extension, which controls the format of the image file. If a file extension other than png, jpg, or tiff is specified, a png extension will be added to the filename by default. This method will fail if a file with the specified filename already exists. If you want to overwrite the file, you'll need to delete it first before calling this method. |

## Version

Introduced in version May 2023  

