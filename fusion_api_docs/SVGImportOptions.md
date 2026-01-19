# SVGImportOptions Object

Derived from: [ImportOptions](ImportOptions.md) Object  

## Description

Defines that an SVG import is to be done and specifies the various options.

## Methods

| Name | Description |
|----|----|
| [classType](SVGImportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [filename](SVGImportOptions_filename.md) | Gets and sets the filename or URL of the file to be imported. |
| [isControlPointFrameDisplayed](SVGImportOptions_isControlPointFrameDisplayed.md) | Gets and sets if any spline curves in the SVG should be drawn with their control point frames. This property defaults to false in a newly created SVGImportOptions object. |
| [isHorizontalFlip](SVGImportOptions_isHorizontalFlip.md) | Gets and sets if the SVG is flipped along the sketch X axis. This property defaults to false in a newly created SVGImportOptions object. |
| [isValid](SVGImportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVerticalFlip](SVGImportOptions_isVerticalFlip.md) | Gets and sets if the SVG is flipped along the sketch Y axis. This property defaults to false in a newly created SVGImportOptions object. |
| [isViewFit](SVGImportOptions_isViewFit.md) | Specifies if the camera should be adjusted to fit the geometry of the import. This defaults to true, which will cause a change in the current view. Setting this to false will leave the view as-is and just import the geometry. |
| [objectType](SVGImportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [transform](SVGImportOptions_transform.md) | Gets and sets the transformation matrix that defines the position, orientation, scale, and mirroring of the imported SVG data relative to the sketch coordinate system. This property defaults to an identity matrix in a newly created SVGImportOptions object. You can define mirroring (the equivalent of horizontal or vertical flip) in the matrix. Doing this gives you more explicit control over the results. You can also use the isHorizontalFlip and isVerticalFlop properties to define the flip. These result in flipping the geometry along the center of the geometry's bounding box. |

## Accessed From

[ImportManager.createSVGImportOptions](ImportManager_createSVGImportOptions.md)

## Version

Introduced in version October 2022  

