# InCanvasRendering.start Method

Parent Object: [InCanvasRendering](InCanvasRendering.md)  

## Description

Starts the process of in-canvas rendering. There are two modes when doing in-canvas rendering; advanced and fast. This is specified in the API using the isAdvanced property. When using advanced rendering, you can specify the desired quality and the rendering will stop once that quality has been reached. When using fast rendering, the rendering never stops but continues until you stop it.  

When using the API, it's generally best to use advanced rendering so you can easily control the final quality and get notified by the renderComplete event when it has finished. When using fast rendering, the renderComplete event is not fired and you have to use some other criteria like the number of iterations complete or the time taken to determine when to stop the rendering process.

## Syntax

"inCanvasRendering_var" is a variable referencing an [InCanvasRendering](InCanvasRendering.md) object.

```python
returnValue = inCanvasRendering_var.start(renderQuality)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if the rendering was successfully started. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| renderQuality | double | Specifies the desired quality of the rendering. The quality is specified using a value between 0 and 1, where 0.75 is the equivalent of "Excellent" and 1.0 is the same as "Final" in the user interface. This is ignored when using fast rendering (the isAdvanced property is False). |

## Version

Introduced in version September 2023  

