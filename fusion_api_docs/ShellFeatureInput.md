# ShellFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a shell feature.

## Methods

| Name | Description |
|----|----|
| [classType](ShellFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [creationOccurrence](ShellFeatureInput_creationOccurrence.md) | In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the shell is created based on geometry (e.g. a profile and/or face(s)) in another component AND (the shell) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI |
| [inputEntities](ShellFeatureInput_inputEntities.md) | Gets and sets the input faces/bodies. If IsTangentChain is true, all the faces that are tangentially connected to the input faces (if any) will also be included. Fails if any faces are input, and the owning bodies of the faces are also input. |
| [insideThickness](ShellFeatureInput_insideThickness.md) | Gets and sets the inside thickness. |
| [isTangentChain](ShellFeatureInput_isTangentChain.md) | Gets and sets if any faces that are tangentially connected to any of the input faces will also be included in setting InputEntities. It defaults to true. |
| [isValid](ShellFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ShellFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [outsideThickness](ShellFeatureInput_outsideThickness.md) | Gets and sets the outside thickness. |
| [shellType](ShellFeatureInput_shellType.md) | The shell type used when creating a shell. The default value is SharpOffsetShellType. |
| [targetBaseFeature](ShellFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[ShellFeatures.createInput](ShellFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Shell Feature API Sample](ShellFeatureSample_Sample.md) | Demonstrates creating a new shell feature. |

## Version

Introduced in version November 2014  

