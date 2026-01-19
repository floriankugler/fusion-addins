# OperationBase Object

Derived from: [Base](Base.md) Object  

## Description

Base class object representing all operations, folders, patterns and setups.

## Methods

| Name | Description |
|----|----|
| [classType](OperationBase_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copyAfter](OperationBase_copyAfter.md) | Creates a duplicate of the operation in the tree after the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup. |
| [copyBefore](OperationBase_copyBefore.md) | Creates a duplicate of the operation in the tree before the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup. |
| [copyInto](OperationBase_copyInto.md) | Creates a duplicate of the operation into the given container. You can only copy into containers, such as setups or folders. Copied operation will be copied at the end of all operations already in the container. Throws an exception if a not allowed copy operation is made for example copying a setup into a setup. |
| [deleteMe](OperationBase_deleteMe.md) | Deletes the operation from the document. In case of a setup or folder, all containing child operations will be deleted as well. Note: Child classes may overwrite this function and throw an exception if the object cannot be deleted. |
| [duplicate](OperationBase_duplicate.md) | Creates a duplicate of the operation in the tree after the itself. |
| [modifyUtility](OperationBase_modifyUtility.md) | Get ModifyUtility for the current operation by given utility type. |
| [moveAfter](OperationBase_moveAfter.md) | Move operation in tree after the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup. |
| [moveBefore](OperationBase_moveBefore.md) | Move operation in tree before the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup. |
| [moveInto](OperationBase_moveInto.md) | Move operation in tree into the given container. This only works with setups, patterns and folders. Moved operation will be moved at the end of all operations already in the container. Throws an exception if a not allowed move is made for example moving a setup into a setup. |

## Properties

| Name | Description |
| --- | --- |
| [attributes](OperationBase_attributes.md) | Returns the collection of attributes associated with this object. |
| [error](OperationBase_error.md) | Returns a message corresponding to any active error associated with the value of this parameter. |
| [generatedDataCollection](OperationBase_generatedDataCollection.md) | Get the generated data associated with a given operation base instance. The type of data depends on the strategy type and might not be available for all strategy types. The available types can be found in GeneratedData.cs |
| [hasError](OperationBase_hasError.md) | Gets if errors were encountered when generating the operation. |
| [hasWarning](OperationBase_hasWarning.md) | Gets if problems were encountered when generating the operation. |
| [isLightBulbOn](OperationBase_isLightBulbOn.md) | Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children so this property does not indicate if the operation is actually visible, just that it should be visible if all of its parent nodes are also visible. Use the isVisible property to determine if it's actually visible. |
| [isOptional](OperationBase_isOptional.md) | Gets and sets the "Optional" property value of the operation. Gets/sets true if the operation is optional. |
| [isProtected](OperationBase_isProtected.md) | Gets and sets the "protected" property value of the operation. Gets/sets true if the operation is protected. |
| [isSelected](OperationBase_isSelected.md) | Gets if this operation is selected in the 'Setups' browser. |
| [isSuppressed](OperationBase_isSuppressed.md) | Gets and sets the "Suppressed" property value of the operation. Gets/sets true if the operation is suppressed. |
| [isValid](OperationBase_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](OperationBase_isVisible.md) | Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this operation is actually visible or not. |
| [name](OperationBase_name.md) | Gets and sets the name of the operation as seen in the browser. This name is unique as compared to the names of all other operations in the document. |
| [notes](OperationBase_notes.md) | Gets and sets the notes of the operation. |
| [objectType](OperationBase_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operationId](OperationBase_operationId.md) | Returns the id of the operation. This id is unique as compared to the ids of all other operations in the document. This id will not change when changing the order or parent of the operation. This id will remain valid when the document is saved and reloaded. |
| [parameters](OperationBase_parameters.md) | Gets the CAMParameters collection for this operation. |
| [parentSetup](OperationBase_parentSetup.md) | Gets the Setup this operation belongs to. |
| [strategy](OperationBase_strategy.md) | Gets the name of the strategy associated with this operation. |
| [warning](OperationBase_warning.md) | Returns a message corresponding to any active warning associated with the value of this parameter. |

## Accessed From

[CAMFolder.createFromCAMTemplate](CAMFolder_createFromCAMTemplate.md), [CAMFolder.createFromCAMTemplate2](CAMFolder_createFromCAMTemplate2.md), [CAMFolder.createFromTemplateXML](CAMFolder_createFromTemplateXML.md), [CAMHoleRecognition.allOperations](CAMHoleRecognition_allOperations.md), [CAMPattern.createFromCAMTemplate](CAMPattern_createFromCAMTemplate.md), [CAMPattern.createFromCAMTemplate2](CAMPattern_createFromCAMTemplate2.md), [CAMPattern.createFromTemplateXML](CAMPattern_createFromTemplateXML.md), [NCProgram.filteredOperations](NCProgram_filteredOperations.md), [NCProgram.operations](NCProgram_operations.md), [NCProgramInput.operations](NCProgramInput_operations.md), [Operations.add](Operations_add.md), [Setup.createFromCAMTemplate](Setup_createFromCAMTemplate.md), [Setup.createFromCAMTemplate2](Setup_createFromCAMTemplate2.md), [Setup.createFromTemplateXML](Setup_createFromTemplateXML.md)

## Derived Classes

[CAMAdditiveContainer](CAMAdditiveContainer.md), [CAMFolder](CAMFolder.md), [CAMHoleRecognition](CAMHoleRecognition.md), [NCProgram](NCProgram.md), [Operation](Operation.md), [Setup](Setup.md)

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version January 2016  

