# SectionAnalysisInput Object

Derived from: [Base](Base.md) Object  

## Description

Provides access the all of the settings available when creating a section analysis. This object is the API equivalent of the command dialog that contains the inputs to create a section analysis. Use this object to define the settings you need and then pass this into the add method to create the section analysis.

## Methods

| Name | Description |
|----|----|
| [classType](SectionAnalysisInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [flip](SectionAnalysisInput_flip.md) | A property that flips which side of the part is cut away by the section. This is a convenience method that results in flipping the Z axis of the transform while maintaining a valid rectangular coordinate system. You can directly manipulate the transform matrix to have the same effect. |

## Properties

| Name | Description |
| --- | --- |
| [cutPlaneEntity](SectionAnalysisInput_cutPlaneEntity.md) | A property that gets and sets the planar entity used to define the cut plane and can be either a planar BRepFace or a ConstructionPlane object. |
| [initialPosition](SectionAnalysisInput_initialPosition.md) | Returns the matrix that describes the initial position and orientation of the specified cut plane entity. Any additional offsets or rotations are defined by a transformation matrix that is applied to this initial position matrix. That matrix is obtained and set using the transform property. |
| [isHatchShown](SectionAnalysisInput_isHatchShown.md) | A property that gets and sets if a hatch pattern should be shown on the section. This property defaults to true when the input is created. |
| [isValid](SectionAnalysisInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SectionAnalysisInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sectionColor](SectionAnalysisInput_sectionColor.md) | A property that gets and sets the color of the section. This property defaults to null, indicating that the component color should be used. The opacity value of the color is ignored. |
| [transform](SectionAnalysisInput_transform.md) | The initial position of the section plane is defined by the specified cut plane entity. Any offsets or rotations are defined by a transformation matrix that is applied to the initial position. This property allows you to get and set the transformation matrix. |

## Accessed From

[SectionAnalyses.createInput](SectionAnalyses_createInput.md)

## Version

Introduced in version January 2023  

