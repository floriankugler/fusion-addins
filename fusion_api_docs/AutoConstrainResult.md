
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

### Enhancements

The only UI themes available are light gray and dark blue. (Update User Manual to cover this.)

1.  **Changes to Support Design Intent**  

    If you need access to the functionality provided by an add-in that hasn't been updated, you can always revert back to using a hybrid design.

2.  **Python Update**  
    This Fusion release updates the Python version from 3.12 to 3.14. Besides the API, Fusion uses Python for a few other things, and this Python update includes some security fixes. Most people won't notice any change. Those affected are the developers and users of any Python apps delivered as .pyc files. Previous versions of these add-ins will be broken because .pyc files are tied to the minor version of Python that was used to create them. Add-ins compiled with the current version (3.12) will not be compatible with the new release (3.14) and will fail to load. This change does not affect any add-ins where the .py source code is available.

    If you deliver apps as pyc files, you need to test your add-in and rebuild it to get new pyc files that you can make available to your users.

    If you're a user and are seeing the message shown below when you start Fusion, you have an impacted add-in and need a new version. Check the Autodesk App Store or the developer's website to download a new compatible version, install it, and continue using it as before. If you can't find an updated app, contact the app developer directly.

3.  **API Support for Derive**  
    The API now supports deriving components. This includes the ability to create, query, and edit a Derive feature and to query the entities that can be derived to determine if they were derived, and if they were, which derive feature created them.

4.  **Sketch Auto Constrain**  
    The API now supports the auto constraint functionality in sketch. This functionality is a preview, so please use it and provide feedback on what you liked or didn't like.

5.  **User Interface Themes**  

6.  **API For the New Assembly Constraint Functionality is Still in Progress**  
    The July release began introducing some of the API for the new assembly constraint functionality. It is a preview feature, and since July, the functionality in Fusion has been modified, necessitating an API change. The changes are still ongoing, so nothing has changed in the November release. However, they will change in January, so if you start using this API, be aware that your existing code will need to be updated to function correctly.

### Fixes

1.  corbin2 reported a problem on the [forum](https://forums.autodesk.com/t5/fusion-api-and-scripts-forum/intersection-fails-with-runtimeerror-2-internalvalidationerror/td-p/13854425) about a failure when using ThroughAllExtent to extrude sketch text. This has been fixed.

### Custom Features

Custom Features is a new functionality that is currently in preview. This release has nothing new for custom features, but we still encourage you to try it and let us know your thoughts. You can learn more about it in the [Custom Feature](CustomFeatures_UM.md) topic in the API User Manual. There are also two add-in samples referenced in that document that you can use to see the functionality.

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts Forum](https://forums.autodesk.com/t5/fusion-api-and-scripts-forum/bd-p/fusion-api-scripts-forum-en). However, because this previews future functionality, it may change, breaking any existing programs that use it. Therefore, you should never deliver programs that utilize any preview capabilities.

## Methods

| Name | Description |
|----|----|
| [classType](AutoConstrainResult_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [addedConstraints](AutoConstrainResult_addedConstraints.md) | Returns an array of the GeometricConstraint objects that were added to constrain the sketch. If no geometric constraints were added during the auto constrain operation, this property returns an empty array. |
| [addedDimensions](AutoConstrainResult_addedDimensions.md) | Returns an array of the SketchDimension objects that were added to constrain the sketch. If no dimensions were added during the auto constrain operation, this property returns an empty array. |
| [isFullyConstrained](AutoConstrainResult_isFullyConstrained.md) | Indicates if the auto constrain operation successfully auto constrained the sketch. Returns true if the sketch is fully constrained after the operation, false otherwise. A value of false may indicate that additional constraints are needed or that the current sketch geometry cannot be fully constrained with the current settings. |
| [isValid](AutoConstrainResult_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](AutoConstrainResult_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Sketch.autoConstrain](Sketch_autoConstrain.md)

## Version

Introduced in version January 2026  

