# CurveSelections Object

Derived from: [Base](Base.md) Object  

## Description

Collection for all curve selections to be passed to a CadContours2DParameterValue object. This is a read-only container. It returns the curve selections associated with the parent parameter value object, but does not write to it. To apply changes done to the collection and the selections it contains, CadContours2DParameterValue.applyCurveSelections() needs to be called.

## Methods

| Name | Description |
|----|----|
| [classType](CurveSelections_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](CurveSelections_clear.md) | Clears all entries. |
| [createNewChainSelection](CurveSelections_createNewChainSelection.md) | Creates a new chain selection and adds it to the end of the collection. |
| [createNewFaceContourSelection](CurveSelections_createNewFaceContourSelection.md) | Creates a new face contour selection and adds it to the end of the collection. |
| [createNewPocketRecognitionSelection](CurveSelections_createNewPocketRecognitionSelection.md) | Creates a new pocket recognition selection and adds it to the end of the collection. |
| [createNewPocketSelection](CurveSelections_createNewPocketSelection.md) | Creates a new pocket selection and adds it to the end of the collection. |
| [createNewSilhouetteSelection](CurveSelections_createNewSilhouetteSelection.md) | Creates a new silhouette selection and adds it to the end of the collection. |
| [createNewSketchSelection](CurveSelections_createNewSketchSelection.md) | Creates a new sketch selection and adds it to the end of the collection. |
| [item](CurveSelections_item.md) | Function that returns the specified curve selection object using an index into the collection. |
| [remove](CurveSelections_remove.md) | Function that removes the specified curve selection object using an index in the collection. |
| [removeByObject](CurveSelections_removeByObject.md) | Function that removes the specified curve selection object from the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](CurveSelections_count.md) | The number of items in the collection. |
| [isValid](CurveSelections_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CurveSelections_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CadContours2dParameterValue.getCurveSelections](CadContours2dParameterValue_getCurveSelections.md)

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

