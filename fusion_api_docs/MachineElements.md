# MachineElements Object

Derived from: [Base](Base.md) Object  

## Description

Collection of machine elements. These elements contain the properties that define the machine.

## Methods

| Name | Description |
|----|----|
| [addElement](MachineElements_addElement.md) | Add a new machine element to the machine. |
| [classType](MachineElements_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [countByType](MachineElements_countByType.md) | Number of elements of specified type. |
| [createMachineElementInput](MachineElements_createMachineElementInput.md) | Create a new MachineElementInput object for the specified type. This is intedned to be used to create/add new machine elements. |
| [defaultItemByType](MachineElements_defaultItemByType.md) | Returns the default item of the given type. In most cases this will be the element with an element ID of "default". |
| [item](MachineElements_item.md) | Get the element at a particular index in the collection. |
| [itemById](MachineElements_itemById.md) | Gets an element of a specific type by ID. |
| [itemsByType](MachineElements_itemsByType.md) | Gets the element of specified type. |

## Properties

| Name | Description |
| --- | --- |
| [count](MachineElements_count.md) | Total number of elements in collection. |
| [isValid](MachineElements_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MachineElements_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Machine.elements](Machine_elements.md)

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |

## Version

Introduced in version April 2023  

