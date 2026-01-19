# OptimizedOrientationResults Object

Derived from: [GeneratedData](GeneratedData.md) Object  

## Description

Collection of OptimizedOrientationResult instances associated with a given optimized orientation object inside an additive setup. The number of instances is the number of results given and the initial orientation result. The initial orientation will contain the orientation matrix, but not the other values calculated by the orientation operation. Setting an OptimizedOrientationResult as the currentOrientationResult will transform the Occurrence assigned to the orientation operation.

## Methods

| Name | Description |
|----|----|
| [classType](OptimizedOrientationResults_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](OptimizedOrientationResults_item.md) | Gets the desired orientation result at the given index. The list is ordered given the orientation parameters of the parent orientation operation. |

## Properties

| Name | Description |
| --- | --- |
| [count](OptimizedOrientationResults_count.md) | The number of items in the collection. |
| [currentOrientationResult](OptimizedOrientationResults_currentOrientationResult.md) | Gets or sets the desired OrientationResult. When setting, the orientation matrix is applied to the component selected in the parent orientation operation, possibly invalidating other operations. |
| [initialOrientationResult](OptimizedOrientationResults_initialOrientationResult.md) | Gets the initial orientation of the component before any result has been applied. |
| [isValid](OptimizedOrientationResults_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](OptimizedOrientationResults_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing FFF API Sample](AdditiveFFFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive FFF manufacturing setup and generate a toolpath. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select an FFF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected FFF machine. This script will also create support structures, if required, based on the orientation of each component. Finally, the script generates the toolpath for the active setup and lets the user choose if they wish to post process the resulting toolpath or if they want to simulate it. |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |

## Version

Introduced in version July 2023  

