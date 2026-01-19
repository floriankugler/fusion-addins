# ArrangeFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

The ArrangeFeatureInput object is the base class for the different types of input objects used to create an arrange feature.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangeFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [set3DEnvelope](ArrangeFeatureInput_set3DEnvelope.md) | Defines a 3D envelope input. Only a single envelope input can exist at time. Calling this method will cause any existing envelope input object to be invalid. |
| [setPlaneEnvelope](ArrangeFeatureInput_setPlaneEnvelope.md) | Defines an envelope input defined by a plane for the arrange feature. Only a single envelope input can exist at a time. Calling this method will cause any existing envelope object input that has been created for this input to be invalid. |
| [setProfileOrFaceEnvelope](ArrangeFeatureInput_setProfileOrFaceEnvelope.md) | Defines an envelope defined by one or more profiles or planar faces. Only a single envelope input can exist at time. Calling this method will cause any existing envelope input object to be invalid. |

## Properties

| Name | Description |
| --- | --- |
| [arrangeComponents](ArrangeFeatureInput_arrangeComponents.md) | Returns the ArrangeComponents object associated with this input. Use this to add and define the components that will be arranged. |
| [definition](ArrangeFeatureInput_definition.md) | Returns a definition input object that provides access to the information to define an arrange feature. This will return different types of definition inputs depending on the solver type specified when creating the input. |
| [isValid](ArrangeFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ArrangeFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [solverType](ArrangeFeatureInput_solverType.md) | Returns the arrange feature solver type defined by this input. |

## Accessed From

[ArrangeFeatures.createInput](ArrangeFeatures_createInput.md)

## Version

Introduced in version January 2025  

