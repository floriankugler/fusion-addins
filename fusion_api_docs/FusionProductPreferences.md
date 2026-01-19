# FusionProductPreferences Object

Derived from: [ProductPreferences](ProductPreferences.md) Object  

## Description

Fusion General Design Preferences

## Methods

| Name | Description |
|----|----|
| [classType](FusionProductPreferences_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [defaultDesignType](FusionProductPreferences_defaultDesignType.md) | Gets and sets the default modeling type setting |
| [defaultWorkspace](FusionProductPreferences_defaultWorkspace.md) | Gets and sets the Default workspace setting. (Model, Sculpt or Patch) |
| [is3DSketchingAllowed](FusionProductPreferences_is3DSketchingAllowed.md) | Gets and sets the Allow 3D sketching of lines and splines option which controls if 3D sketching is allowed or if sketching is forced to be on the x-y plane of the sketch. |
| [isActiveComponentVisibilityUsed](FusionProductPreferences_isActiveComponentVisibilityUsed.md) | Gets and sets the Active Component Visibility option |
| [isAllowReferencesDuringEditInPlace](FusionProductPreferences_isAllowReferencesDuringEditInPlace.md) | Gets and sets if you can create associative references while editing external components in context. |
| [isAutoHideSketchOnFeatureCreation](FusionProductPreferences_isAutoHideSketchOnFeatureCreation.md) | Gets and sets if the sketch should be automatically hidden whenever a feature is created from it. |
| [isAutoLookAtSketch](FusionProductPreferences_isAutoLookAtSketch.md) | **RETIRED** Gets and sets if the view is re-oriented to view the newly created sketch. This property has been replaced by the isAutoLookAtSketch2 property, which provides the full capabilities. |
| [isAutoLookAtSketch2](FusionProductPreferences_isAutoLookAtSketch2.md) | Gets and sets if the view is re-oriented to view the newly created sketch, and if it is re-oriented, if the camera uses the current camera settings or is orthographic. |
| [isAutoProjectEdgesOnReference](FusionProductPreferences_isAutoProjectEdgesOnReference.md) | Gets and sets if model edges should be automatically projected when creating constraints and dimensions in the active sketch when the orientation is normal to the active sketch plane. |
| [isAutoProjectGeometry](FusionProductPreferences_isAutoProjectGeometry.md) | Gets and Sets if geometry, not in the active sketch plane, is to be automatically projected. |
| [isDimensionEditedWhenCreated](FusionProductPreferences_isDimensionEditedWhenCreated.md) | Gets and sets if dimension value is edited when the dimension is created. |
| [isEnableArrangeAndSimplifyTools](FusionProductPreferences_isEnableArrangeAndSimplifyTools.md) | Gets and sets if the Arrange, Remove Features, Remove Faces, and Replace with Primitives commands should be added to the Modify menu in the Design workspace. |
| [isFirstComponentGroundToParent](FusionProductPreferences_isFirstComponentGroundToParent.md) |  |
| [isGhostedResultBodyShown](FusionProductPreferences_isGhostedResultBodyShown.md) | Gets and sets the Show ghosted result body option |
| [isJointPreviewAnimated](FusionProductPreferences_isJointPreviewAnimated.md) | Gets and sets the Animate joint preview option |
| [isSketchScaledWithFirstDimension](FusionProductPreferences_isSketchScaledWithFirstDimension.md) | Gets and sets if the sketch geometry is automatically scaled when the first dimension is added. |
| [isValid](FusionProductPreferences_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](FusionProductPreferences_name.md) | Returns the name of this ProductPreferences object. |
| [objectType](FusionProductPreferences_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version August 2014  

