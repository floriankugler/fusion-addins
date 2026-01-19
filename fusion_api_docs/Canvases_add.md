# Canvases.add Method

Parent Object: [Canvases](Canvases.md)  

## Description

Creates a new canvas. Use the createInput method to first create an input object and set the available options. Then, pass that input object to the add method to create the canvas.

## Syntax

"canvases_var" is a variable referencing a [Canvases](Canvases.md) object.

```python
returnValue = canvases_var.add(input)
```

## Return Value

| Type                 | Description                              |
|----------------------|------------------------------------------|
| [Canvas](Canvas.md) | Returns the newly created Canvas object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CanvasInput](CanvasInput.md) | The CanvasInput object that defines the required information needed to create a new canvas. A CanvasInput object is the logical equivalent to the command dialog when creating a canvas. It provides access to the various options when creating a canvas. Calling the add method and passing in the CanvasInput is the equivalent to clicking the OK button on the dialog to create the canvas. |

## Version

Introduced in version May 2023  

