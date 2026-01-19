
Derived from: [EventHandler](EventHandler.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

API clients can implement subclasses of this handler to enable custom Signed Distance Field geometries.

## Methods

| Name | Description |
|----|----|
| [boundingBox](CustomSDFCallbackEventHandler_boundingBox.md) | This method should be implemented in the subclass of the handler to return the bounding box of the Signed Distance Field that it can provide. This method will be called infrequently by the system. |
| [signedDistanceAt](CustomSDFCallbackEventHandler_signedDistanceAt.md) | This method should be implemented in the subclass of the handler to return the Signed Distance value at the given coordinates within the bounding box. This method will be called very frequently and potentially from several differrent threads, it should be made as fast as possible |

## Version

Introduced in version May 2025  

