# NCProgram Object

Derived from: [OperationBase](OperationBase.md) Object  

## Description

Object that represents an existing NC program.

## Methods

| Name | Description |
|----|----|
| [classType](NCProgram_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copyAfter](NCProgram_copyAfter.md) | Creates a duplicate of the operation in the tree after the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup. |
| [copyBefore](NCProgram_copyBefore.md) | Creates a duplicate of the operation in the tree before the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup. |
| [copyInto](NCProgram_copyInto.md) | Creates a duplicate of the operation into the given container. You can only copy into containers, such as setups or folders. Copied operation will be copied at the end of all operations already in the container. Throws an exception if a not allowed copy operation is made for example copying a setup into a setup. |
| [deleteMe](NCProgram_deleteMe.md) | Deletes the operation from the document. In case of a setup or folder, all containing child operations will be deleted as well. Note: Child classes may overwrite this function and throw an exception if the object cannot be deleted. |
| [duplicate](NCProgram_duplicate.md) | Creates a duplicate of the operation in the tree after the itself. |
| [modifyUtility](NCProgram_modifyUtility.md) | Get ModifyUtility for the current operation by given utility type. |
| [moveAfter](NCProgram_moveAfter.md) | Move operation in tree after the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup. |
| [moveBefore](NCProgram_moveBefore.md) | Move operation in tree before the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup. |
| [moveInto](NCProgram_moveInto.md) | Move operation in tree into the given container. This only works with setups, patterns and folders. Moved operation will be moved at the end of all operations already in the container. Throws an exception if a not allowed move is made for example moving a setup into a setup. |
| [postProcess](NCProgram_postProcess.md) | Creates machine-specific NC code for this NC program. |
| [updatePostParameters](NCProgram_updatePostParameters.md) | Overrides the default post parameters of this NC program with the given user's input. |

## Properties

| Name | Description |
| --- | --- |
| [attributes](NCProgram_attributes.md) | Returns the collection of attributes associated with this object. |
| [error](NCProgram_error.md) | Returns a message corresponding to any active error associated with the value of this parameter. |
| [filteredOperations](NCProgram_filteredOperations.md) | Gets all valid operations derived from the operations property. The list is ordered with respect to the nc_program_oderByTool parameter and considers the number of instances in a setup. |
| [fusionHubFolder](NCProgram_fusionHubFolder.md) | Gets and sets the DataFolder to which the exported files should be uploaded to if the parameter nc_program_postToFusionTeam is set to true. When a DataFolder is set, nc_program_postToFusionTeam is automatically set to true. An exception will be thrown if the DataFolder to set is not valid or not accessible. Depending on the FusionHubExecutionBehaviors used for the export the design may be saved at this location as well. |
| [generatedDataCollection](NCProgram_generatedDataCollection.md) | Get the generated data associated with a given operation base instance. The type of data depends on the strategy type and might not be available for all strategy types. The available types can be found in GeneratedData.cs |
| [hasError](NCProgram_hasError.md) | Gets if errors were encountered when generating the operation. |
| [hasWarning](NCProgram_hasWarning.md) | Gets if problems were encountered when generating the operation. |
| [isLightBulbOn](NCProgram_isLightBulbOn.md) | Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children so this property does not indicate if the operation is actually visible, just that it should be visible if all of its parent nodes are also visible. Use the isVisible property to determine if it's actually visible. |
| [isOptional](NCProgram_isOptional.md) | Gets and sets the "Optional" property value of the operation. Gets/sets true if the operation is optional. |
| [isProtected](NCProgram_isProtected.md) | Gets and sets the "protected" property value of the operation. Gets/sets true if the operation is protected. |
| [isSelected](NCProgram_isSelected.md) | Gets if this operation is selected in the 'Setups' browser. |
| [isSuppressed](NCProgram_isSuppressed.md) | Gets and sets the "Suppressed" property value of the operation. Gets/sets true if the operation is suppressed. |
| [isValid](NCProgram_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](NCProgram_isVisible.md) | Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this operation is actually visible or not. |
| [machine](NCProgram_machine.md) | Gets and sets the machine of this NC program. When a machine is set, "use machine configuration" is automatically set to true. If this machine has a default post assigned, this post will be set for the NC program as well. |
| [name](NCProgram_name.md) | Gets and sets the name of the operation as seen in the browser. This name is unique as compared to the names of all other operations in the document. |
| [notes](NCProgram_notes.md) | Gets and sets the notes of the operation. |
| [objectType](NCProgram_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operationId](NCProgram_operationId.md) | Returns the id of the operation. This id is unique as compared to the ids of all other operations in the document. This id will not change when changing the order or parent of the operation. This id will remain valid when the document is saved and reloaded. |
| [operations](NCProgram_operations.md) | Gets and sets the operations which will be included in the NC program. Valid input contains any number of operations, setups or folders. For setups and folders all child operations will be added. Operations will be post processed in setup order, with operations from the same setup grouped together. Setting the nc_program_orderByTool BooleanParameterValue on the parameters property to true will reorder operations across multiple setups to reduce the number of tool changes. |
| [parameters](NCProgram_parameters.md) | Gets the CAMParameters collection for this operation. |
| [parentSetup](NCProgram_parentSetup.md) | Gets the Setup this operation belongs to. |
| [postConfiguration](NCProgram_postConfiguration.md) | Gets and sets the post configuration of this NC program. |
| [postParameters](NCProgram_postParameters.md) | Gets the post parameters of this NC program. |
| [strategy](NCProgram_strategy.md) | Gets the name of the strategy associated with this operation. |
| [warning](NCProgram_warning.md) | Returns a message corresponding to any active warning associated with the value of this parameter. |

## Accessed From

[NCPrograms.add](NCPrograms_add.md), [NCPrograms.item](NCPrograms_item.md), [NCPrograms.itemByName](NCPrograms_itemByName.md), [NCPrograms.itemByOperationId](NCPrograms_itemByOperationId.md)

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

