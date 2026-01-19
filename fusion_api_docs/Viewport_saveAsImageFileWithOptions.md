# Viewport.saveAsImageFileWithOptions Method

Parent Object: [Viewport](Viewport.md)  

## Description

Saves the current view to the specified image file. The view is re-rendered to the specified size and not just scaled from the existing view. This allows you to generate higher resolution images than you could do with just a screen capture.

## Syntax

"viewport_var" is a variable referencing a [Viewport](Viewport.md) object.

```python
returnValue = viewport_var.saveAsImageFileWithOptions(options)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| options | [SaveImageFileOptions](SaveImageFileOptions.md) | A SaveImageFileOptions object that defines the various options that define how the image should be created. The SaveImageFileOptions can be created by using the static create method on the SaveImageFileOptions class. |

## Version

Introduced in version May 2022  

