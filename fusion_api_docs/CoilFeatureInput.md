# CoilFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a coil feature.

## Methods

| Name | Description |
|----|----|
| [classType](CoilFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setToHeightAndPitchCoil](CoilFeatureInput_setToHeightAndPitchCoil.md) | Sets the coil type to HeightAndPitchCoilType. |
| [setToRevolutionAndHeight](CoilFeatureInput_setToRevolutionAndHeight.md) | Sets the coil type to RevolutionsAndHeightCoilType. |
| [setToRevolutionsAndPitch](CoilFeatureInput_setToRevolutionsAndPitch.md) | Sets the coil type to RevolutionsAndPitchCoilType. |
| [setToSpiral](CoilFeatureInput_setToSpiral.md) | Sets the coil type to SpiralCoilType. |

## Properties

| Name | Description |
| --- | --- |
| [angle](CoilFeatureInput_angle.md) | Gets the angle. Returns null in the case where the coilType property returns SpiralCoilType. |
| [basePlane](CoilFeatureInput_basePlane.md) | Gets and sets the base plane. |
| [coilSectionPosition](CoilFeatureInput_coilSectionPosition.md) | Gets the section position of the coil. It defaults to InsideCoilSectionPosition. |
| [coilSectionType](CoilFeatureInput_coilSectionType.md) | Gets the section type of the coil. It defaults to CircularCoilSectionType. |
| [coilType](CoilFeatureInput_coilType.md) | Gets the type of the coil. |
| [diameter](CoilFeatureInput_diameter.md) | Gets and sets the diameter. |
| [height](CoilFeatureInput_height.md) | Gets the height. Returns null in the case where the coilType property returns RevolutionsAndPitchCoilType. |
| [isClockwiseRotation](CoilFeatureInput_isClockwiseRotation.md) | Gets and sets whether the rotation is clockwise or counter-clockwise. A value of true indicates clockwise rotation. It defaults to true. |
| [isSolid](CoilFeatureInput_isSolid.md) | Specifies if the coil should be created as a solid or surface. This is initialized to true so a solid will be created if it's not changed. It only can be set to false in non-parametric modeling. |
| [isValid](CoilFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CoilFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](CoilFeatureInput_operation.md) | Gets and sets the type of operation performed by the coil. |
| [pitch](CoilFeatureInput_pitch.md) | Gets the pitch. Returns null in the case where the coilType property returns RevolutionsAndHeightCoilType or SpiralCoilType. |
| [revolutions](CoilFeatureInput_revolutions.md) | Gets the revolutions number. Returns null in the case where the coilType property returns HeightAndPitchCoilType. |
| [sectionSize](CoilFeatureInput_sectionSize.md) | Gets and sets the section size. |
| [targetBaseFeature](CoilFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Version

Introduced in version March 2016  

