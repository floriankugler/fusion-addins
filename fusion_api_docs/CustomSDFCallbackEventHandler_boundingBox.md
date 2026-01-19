# CustomSDFCallbackEventHandler.boundingBox Method

Parent Object: [CustomSDFCallbackEventHandler](CustomSDFCallbackEventHandler.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

This method should be implemented in the subclass of the handler to return the bounding box of the Signed Distance Field that it can provide. This method will be called infrequently by the system.

## Syntax

"customSDFCallbackEventHandler_var" is a variable referencing a [CustomSDFCallbackEventHandler](CustomSDFCallbackEventHandler.md) object.

```python
returnValue = customSDFCallbackEventHandler_var.boundingBox(bboxOut)
```

## Return Value

| Type    | Description                            |
|---------|----------------------------------------|
| boolean | True if there is a valid bounding box. |

## Parameters

| Name | Type | Description |
|----|----|----|
| bboxOut | [BoundingBox3D](BoundingBox3D.md) | This is a return parameter. The values of this should be set by the client implementation. |

## Version

Introduced in version May 2025  

