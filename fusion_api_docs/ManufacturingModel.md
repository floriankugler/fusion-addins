# ManufacturingModel Object

Derived from: [Base](Base.md) Object  

## Description

Represents a ManufacturingModel within a CAM design. A Manufacturing Model is a derive of the Design scene, which can be augmented without any effects of the original Design.

## Methods

| Name | Description |
|----|----|
| [activate](ManufacturingModel_activate.md) | Makes the ManufacturingModel the active edit target in the user interface. This is the same as enabling the radio button next to the occurrence in the browser. |
| [classType](ManufacturingModel_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ManufacturingModel_deleteMe.md) | Deletes this ManufacturingModel. If this is part of a setup, the reference to this will be lost. The deletion makes that reference invalid. |
| [duplicate](ManufacturingModel_duplicate.md) | Creates and returns a copy of the ManufacturingModel, within its parent collection. The newly created ManufacturingModel will have a new unique name assigned. |
| [syncManufacturingModel](ManufacturingModel_syncManufacturingModel.md) | Checks whether changes to the original design have been made. If so, the given manufacturing model is synchronized with its source. |

## Properties

| Name | Description |
| --- | --- |
| [id](ManufacturingModel_id.md) | Gets the unique identifier of the ManufacturingModel within the document. |
| [isActive](ManufacturingModel_isActive.md) | Gets whether this ManufacturingModel is active in the user interface. This is the same as checking the state of the radio button next to the ManufacturingModel in the browser. To activate the ManufacturingModel use the Activate method. |
| [isValid](ManufacturingModel_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ManufacturingModel_name.md) | Gets or sets the display name of the ManufacturingModel. This is the name that will be shown in the browser and other locations. |
| [objectType](ManufacturingModel_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrence](ManufacturingModel_occurrence.md) | Returns the occurrence for that ManufacturingModel. |

## Accessed From

[ManufacturingModel.duplicate](ManufacturingModel_duplicate.md), [ManufacturingModels.add](ManufacturingModels_add.md), [ManufacturingModels.item](ManufacturingModels_item.md), [ManufacturingModels.itemById](ManufacturingModels_itemById.md), [ManufacturingModels.itemByName](ManufacturingModels_itemByName.md)

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |

## Version

Introduced in version April 2023  

