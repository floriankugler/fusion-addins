# Viewport.saveAsImageFile Method

Parent Object: [Viewport](Viewport.md)  

## Description

Saves the current view to the specified image file. The view is re-rendered to the specified size and not just scaled from the existing view. This allows you to generate higher resolution images than you could do with just a screen capture.

## Syntax

"viewport_var" is a variable referencing a [Viewport](Viewport.md) object.

```python
returnValue = viewport_var.saveAsImageFile(filename, width, height)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The full filename, including the path, of the image file. The type of image file to be created is inferred from the extension of the filename. |
| width | integer | The width in pixels of the output image. A value of zero indicates that the current width of the viewport is to be used. |
| height | integer | The height in pixels of the output image. A value of zero indicates that the current height of the viewport is to be used. |

## Samples

| Name | Description |
|----|----|
| [Create Animation API Sample](CreateAnimation_Sample.md) | Creates a series of images of a design where a parameter is being changed. The series of images can be used to create an animation using other software. To run this sample, have a part open that contains a parameter named "Length". The parameter should be able to be successfully modified from 10 to 15 centimeters. Run the sample and choose or create a directory for the output. After running you should have a folder full of images that are snapshots of each parameter value. |

## Version

Introduced in version August 2014  

