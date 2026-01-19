# ParameterList Object

Derived from: [Base](Base.md) Object  

## Description

Transient object used to pass a set of parameters.

## Methods

| Name | Description |
|----|----|
| [add](ParameterList_add.md) | Adds a parameter to the list. This does not create a new parameter, it adds an existing parameter to the list. Note that duplicates can exist in the list. |
| [classType](ParameterList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [contains](ParameterList_contains.md) | Indicates whether or not ParameterList collection contains a specified parameter |
| [create](ParameterList_create.md) | Creates a parameter list that the client can use for various purposes. Use ParameterList.Add to add parameters to the list after creating it. |
| [find](ParameterList_find.md) | Finds the specified parameter in the list. The search can be started at a specified index rather than from the beginning of the list. If not found, -1 is returned. |
| [item](ParameterList_item.md) | Function that returns the specified parameter using an index into the collection. |
| [itemByName](ParameterList_itemByName.md) | Returns the specified parameter using the name of the parameter as it is displayed in the parameters dialog |
| [removeByIndex](ParameterList_removeByIndex.md) | Method that removes a parameter from the list using the index of the item in the list Will fail if the list is read only. |
| [removeByItem](ParameterList_removeByItem.md) | Method that removes a parameter from the list by specifying the parameter (item) to remove |

## Properties

| Name | Description |
| --- | --- |
| [count](ParameterList_count.md) | Returns the number of parameters in the collection. |
| [isReadOnly](ParameterList_isReadOnly.md) | Indicates if the list is read-only Some lists returned by API calls (instead of lists created by the user) are read only. Items cannot be added or remove from such a list. |
| [isValid](ParameterList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ParameterList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CustomFeatureParameter.dependencyParameters](CustomFeatureParameter_dependencyParameters.md), [CustomFeatureParameter.dependentParameters](CustomFeatureParameter_dependentParameters.md), [DerivedParameter.dependencyParameters](DerivedParameter_dependencyParameters.md), [DerivedParameter.dependentParameters](DerivedParameter_dependentParameters.md), [Design.allParameters](Design_allParameters.md), [FlatPatternProduct.allParameters](FlatPatternProduct_allParameters.md), [ModelParameter.dependencyParameters](ModelParameter_dependencyParameters.md), [ModelParameter.dependentParameters](ModelParameter_dependentParameters.md), [Parameter.dependencyParameters](Parameter_dependencyParameters.md), [Parameter.dependentParameters](Parameter_dependentParameters.md), [ParameterList.create](ParameterList_create.md), [UserParameter.dependencyParameters](UserParameter_dependencyParameters.md), [UserParameter.dependentParameters](UserParameter_dependentParameters.md), [VariableRadiusFilletEdgeSet.midPositions](VariableRadiusFilletEdgeSet_midPositions.md), [VariableRadiusFilletEdgeSet.midRadii](VariableRadiusFilletEdgeSet_midRadii.md), [WorkingModel.allParameters](WorkingModel_allParameters.md)

## Samples

| Name | Description |
|----|----|
| [Create Animation API Sample](CreateAnimation_Sample.md) | Creates a series of images of a design where a parameter is being changed. The series of images can be used to create an animation using other software. To run this sample, have a part open that contains a parameter named "Length". The parameter should be able to be successfully modified from 10 to 15 centimeters. Run the sample and choose or create a directory for the output. After running you should have a folder full of images that are snapshots of each parameter value. |

## Version

Introduced in version August 2014  

