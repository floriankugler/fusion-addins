# MachineAvoidGroups Object

Derived from: [Base](Base.md) Object  

## Description

Collection of all the mutually exclusive surface groups to be passed to a toolpath with stock to leave and avoid clearances associated to them. This is a read-only container that gets passed to CadMachineAvoidGroupsParameterValue object. It returns the groups associated with the parent parameter value object, but does not write to it. To apply changes done to the collection and the selections it contains, CadMachineAvoidGroupsParameterValue.applyMachineAvoidGroups() needs to be called.

## Methods

| Name | Description |
|----|----|
| [classType](MachineAvoidGroups_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](MachineAvoidGroups_clear.md) | Clears all entries. |
| [createNewMachineAvoidDirectSelectionGroup](MachineAvoidGroups_createNewMachineAvoidDirectSelectionGroup.md) | Creates a new machine avoid group and adds it to the end of the collection. |
| [defaultGroup](MachineAvoidGroups_defaultGroup.md) | Function that returns the specified machine/avoid default group selection object using the group type. Default groups contain surfaces that have a specific meaning within the toolpath operation, for example Model, Fixture, Drive etc. |
| [item](MachineAvoidGroups_item.md) | Function that returns the specified machine/avoid group selection object using an index into the collection. |
| [remove](MachineAvoidGroups_remove.md) | Function that removes the specified group object using an index in the collection. |
| [removeByObject](MachineAvoidGroups_removeByObject.md) | Function that removes the specified group object from the collection. |
| [sync](MachineAvoidGroups_sync.md) | Function that synchronizes the selections and properties of the default groups from the current operation. This is needed when there are changes made to parameters that drive the default groups (e.g. Setup model or fixture selection changes to be reflected in the MachineAvoidGroups object on the API side). WARNING: This function must not be called before applyMachineAvoidGroups, because temporary group settings and selections will not have been stored in the operation object and will be overwritten. |

## Properties

| Name | Description |
| --- | --- |
| [count](MachineAvoidGroups_count.md) | The number of items in the collection. |
| [isValid](MachineAvoidGroups_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MachineAvoidGroups_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CadMachineAvoidGroupsParameterValue.getMachineAvoidGroups](CadMachineAvoidGroupsParameterValue_getMachineAvoidGroups.md)

## Samples

| Name | Description |
| --- | --- |
| [Avoid Machine Surface Settings API Sample](AvoidMachineSurfaceSettings_Sample.md) | This sample script demonstrates how to use Machine/Avoid/Gouge/Fixture functionality. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a curved surface with a through slot, a countersunk hole and a raised, circular and filleted upstand from the surface. The model is supported by two rectangular blocks, themselves mounted on a fixture plate. A setup is included with a single operation running a 3-axis diagonal raster over the model, supports and fixture. The operation machines the fixture, the supporting blocks, the upper surface of the upstand and the area within the slot and hole, something we would like to avoid. The script duplicates the original operation and then proceeds to create a series of MachineAvoidGroups. These are labelled as either Machine in the case of 2 cap surfaces for the slot and hole, Fixture for the fixture plate, Gouge for the supporting blocks and Avoid for the top face of the upstand. Additionally, both AxialOffset and RadialOffset can be specified for the Machine, Avoid and Fixture passes. |
| [Create Engravings Selection Sets API Sample](CreateEngravingsSelectionSets_Sample.md) | This sample script demonstrates how to find and machine engravings in the Z+ direction using pocket recognition. The script will first open an example model via its URN. Using pocket recognition, it will identify pockets that may be engravings based on their dimensions. We assume here that an engraving pocket is: Made with a flat bottom face and no fillet. A closed pocket. Have a Z height less than 2 mm We demonstrate creating selection sets in both design and manufacture workspaces and use one of the selection sets as an operation geometry selection input to generate an engraving operation. The engraving toolpath can be seen by expanding the setup and selecting the operation. |

## Version

Introduced in version September 2024  

