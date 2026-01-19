# Canvases.createInput Method

Parent Object: [Canvases](Canvases.md)  

## Description

Creates a new CanvasInput object. A CanvasInput object is the logical equivalent to the command dialog when creating a canvas. It provides access to the various options when creating a canvas. Calling the add method and passing in the CanvasInput is the equivalent to clicking the OK button on the dialog to create the canvas.

## Syntax

"canvases_var" is a variable referencing a [Canvases](Canvases.md) object.

```python
returnValue = canvases_var.createInput(imageFilename, planarEntity)
```

## Return Value

| Type | Description |
|----|----|
| [CanvasInput](CanvasInput.md) | Returns a CanvasInput object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| imageFilename | string | The full filename to the image to use for the canvas. PNG, JPEG, and TIFF files are supported. |
| planarEntity | [Base](Base.md) | A planar BRepFace or a Construction plane to create the canvas on. If the canvas is being created in a base feature or in a direct modeling design, this can be a Plane object. |

## Version

Introduced in version May 2023  

