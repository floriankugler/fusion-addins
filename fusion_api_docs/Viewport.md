# Viewport Object

Derived from: [Base](Base.md) Object  

## Description

A viewport within Fusion. A viewport is the window where the model is displayed.

## Methods

| Name | Description |
|----|----|
| [classType](Viewport_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [fit](Viewport_fit.md) | Forces a camera change so that all of the graphics are visible in the viewport. |
| [goHome](Viewport_goHome.md) | Sets the camera of the viewport to the defined "home" position. |
| [modelToViewSpace](Viewport_modelToViewSpace.md) | A specified point in model space returns the equivalent point in view space. |
| [refresh](Viewport_refresh.md) | Forces the view to refresh. It is sometimes useful to force a refresh to be able to see edits that have been made using the API. |
| [resetFront](Viewport_resetFront.md) | Resets the front view to be the default front view orientation. |
| [saveAsImageFile](Viewport_saveAsImageFile.md) | Saves the current view to the specified image file. The view is re-rendered to the specified size and not just scaled from the existing view. This allows you to generate higher resolution images than you could do with just a screen capture. |
| [saveAsImageFileWithOptions](Viewport_saveAsImageFileWithOptions.md) | Saves the current view to the specified image file. The view is re-rendered to the specified size and not just scaled from the existing view. This allows you to generate higher resolution images than you could do with just a screen capture. |
| [screenToView](Viewport_screenToView.md) | Converts a 2D screen point into the equivalent viewport coordinate. |
| [setCurrentAsFront](Viewport_setCurrentAsFront.md) | Sets the "front" view to be the current view orientation. |
| [setCurrentAsHome](Viewport_setCurrentAsHome.md) | Sets the "home" view to be the current view orientation. |
| [setCurrentAsTop](Viewport_setCurrentAsTop.md) | Sets the "top" view to be the current view orientation. |
| [viewToModelSpace](Viewport_viewToModelSpace.md) | A specified point in view space returns the equivalent point in model space. Because view space is 2D and model space is 3D, the depth of the point is returned is somewhat arbitrary along the eye to target point direction. |
| [viewToScreen](Viewport_viewToScreen.md) | Converts a 2D viewPort point into the equivalent screen coordinate. |

## Properties

| Name | Description |
| --- | --- |
| [camera](Viewport_camera.md) | Gets and sets the camera associated with the view. The camera returned is a copy of the current camera settings of the view. Editing the properties of the camera will have no affect on the viewport until the camera is assigned back to the viewport. |
| [frontEyeDirection](Viewport_frontEyeDirection.md) | Returns the direction of the front view as defined by the view cube. This vector defines the direction from the eye to the target for the front view. |
| [frontUpDirection](Viewport_frontUpDirection.md) | Returns the up direction of the front view as defined by the view cube. |
| [height](Viewport_height.md) | Returns the height of the viewport in pixels. |
| [isFullScreen](Viewport_isFullScreen.md) | Gets and sets if the view is in full screen mode. |
| [isValid](Viewport_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [modelToViewSpaceTransform](Viewport_modelToViewSpaceTransform.md) | Returns a transformation matrix that defines the transform from model to viewport space. |
| [objectType](Viewport_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentDocument](Viewport_parentDocument.md) | Returns the parent document of this viewport. |
| [visualStyle](Viewport_visualStyle.md) | Gets and sets the current visual style being used. |
| [width](Viewport_width.md) | Returns the width of the viewport in pixels. |

## Accessed From

[Application.activeViewport](Application_activeViewport.md), [CameraEventArgs.viewport](CameraEventArgs_viewport.md), [MouseEventArgs.viewport](MouseEventArgs_viewport.md), [RenderEventArgs.viewport](RenderEventArgs_viewport.md)

## Samples

| Name | Description |
|----|----|
| [As-Built Joint Sample](AsBuiltJointSample_Sample.md) | Demonstrates creating a new As-Built Joint. |
| [Create Animation API Sample](CreateAnimation_Sample.md) | Creates a series of images of a design where a parameter is being changed. The series of images can be used to create an animation using other software. To run this sample, have a part open that contains a parameter named "Length". The parameter should be able to be successfully modified from 10 to 15 centimeters. Run the sample and choose or create a directory for the output. After running you should have a folder full of images that are snapshots of each parameter value. |
| [Joint Origin Sample](JointOriginSample_Sample.md) | Demonstrates creating a new Joint Origin. |
| [Rigid Group API Sample](RigidGroupSample_Sample.md) | Demonstrates creating a new Rigid Group. |

## Version

Introduced in version August 2014  

