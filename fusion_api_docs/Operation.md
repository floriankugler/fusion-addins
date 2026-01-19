# Operation Object

Derived from: [OperationBase](OperationBase.md) Object  

## Description

Object that represents an operation in an existing Setup, Folder or Pattern.

## Methods

| Name | Description |
|----|----|
| [classType](Operation_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copyAfter](Operation_copyAfter.md) | Creates a duplicate of the operation in the tree after the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup. |
| [copyBefore](Operation_copyBefore.md) | Creates a duplicate of the operation in the tree before the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup. |
| [copyInto](Operation_copyInto.md) | Creates a duplicate of the operation into the given container. You can only copy into containers, such as setups or folders. Copied operation will be copied at the end of all operations already in the container. Throws an exception if a not allowed copy operation is made for example copying a setup into a setup. |
| [deleteMe](Operation_deleteMe.md) | Deletes the operation from the document. In case of a setup or folder, all containing child operations will be deleted as well. Note: Child classes may overwrite this function and throw an exception if the object cannot be deleted. |
| [duplicate](Operation_duplicate.md) | Creates a duplicate of the operation in the tree after the itself. |
| [modifyUtility](Operation_modifyUtility.md) | Get ModifyUtility for the current operation by given utility type. |
| [moveAfter](Operation_moveAfter.md) | Move operation in tree after the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup. |
| [moveBefore](Operation_moveBefore.md) | Move operation in tree before the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup. |
| [moveInto](Operation_moveInto.md) | Move operation in tree into the given container. This only works with setups, patterns and folders. Moved operation will be moved at the end of all operations already in the container. Throws an exception if a not allowed move is made for example moving a setup into a setup. |

## Properties

| Name | Description |
| --- | --- |
| [attributes](Operation_attributes.md) | Returns the collection of attributes associated with this object. |
| [error](Operation_error.md) | Returns a message corresponding to any active error associated with the value of this parameter. |
| [generatedDataCollection](Operation_generatedDataCollection.md) | Get the generated data associated with a given operation base instance. The type of data depends on the strategy type and might not be available for all strategy types. The available types can be found in GeneratedData.cs |
| [generatingProgress](Operation_generatingProgress.md) | Gets the generation progress value for this operation. |
| [hasError](Operation_hasError.md) | Gets if errors were encountered when generating the operation. |
| [hasToolpath](Operation_hasToolpath.md) | Gets if a toolpath currently exists (has been generated) for this operation. |
| [hasWarning](Operation_hasWarning.md) | Gets if problems were encountered when generating the operation. |
| [isGenerating](Operation_isGenerating.md) | Gets if the operation is being generated. |
| [isLightBulbOn](Operation_isLightBulbOn.md) | Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children so this property does not indicate if the operation is actually visible, just that it should be visible if all of its parent nodes are also visible. Use the isVisible property to determine if it's actually visible. |
| [isOptional](Operation_isOptional.md) | Gets and sets the "Optional" property value of the operation. Gets/sets true if the operation is optional. |
| [isProtected](Operation_isProtected.md) | Gets and sets the "protected" property value of the operation. Gets/sets true if the operation is protected. |
| [isSelected](Operation_isSelected.md) | Gets if this operation is selected in the 'Setups' browser. |
| [isSuppressed](Operation_isSuppressed.md) | Gets and sets the "Suppressed" property value of the operation. Gets/sets true if the operation is suppressed. |
| [isToolpathValid](Operation_isToolpathValid.md) | Gets if the toolpath for this operation is currently valid. (has not become invalidated by model changes). |
| [isValid](Operation_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](Operation_isVisible.md) | Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this operation is actually visible or not. |
| [name](Operation_name.md) | Gets and sets the name of the operation as seen in the browser. This name is unique as compared to the names of all other operations in the document. |
| [notes](Operation_notes.md) | Gets and sets the notes of the operation. |
| [objectType](Operation_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operationId](Operation_operationId.md) | Returns the id of the operation. This id is unique as compared to the ids of all other operations in the document. This id will not change when changing the order or parent of the operation. This id will remain valid when the document is saved and reloaded. |
| [operationState](Operation_operationState.md) | Gets the current state of this operation. |
| [parameters](Operation_parameters.md) | Gets the CAMParameters collection for this operation. |
| [parent](Operation_parent.md) | Returns the parent Setup, Folder or Pattern for this operation. |
| [parentSetup](Operation_parentSetup.md) | Gets the Setup this operation belongs to. |
| [strategy](Operation_strategy.md) | Gets the name of the strategy associated with this operation. |
| [strategyType](Operation_strategyType.md) | **RETIRED** Gets the strategy type for this operation. |
| [tool](Operation_tool.md) | Get or set the tool for this operation. The document's tool library will be updated accordingly. The tool instance returned is a copy and therefore is not referenced by the operation. To change the tool of the operation, the new tool must be assigned to the operation. Setting a tool will override the current preset and will fall back to the default preset of the new tool. |
| [toolPreset](Operation_toolPreset.md) | Get or set the tool preset to be used. Must be a valid preset of the already assigned tool. Returns null if the operation has no tool or preset. |
| [warning](Operation_warning.md) | Returns a message corresponding to any active warning associated with the value of this parameter. |

## Accessed From

[AdditiveSetupUtility.assignPartsToBodyPreset](AdditiveSetupUtility_assignPartsToBodyPreset.md), [DocumentToolLibrary.operationsByTool](DocumentToolLibrary_operationsByTool.md), [Operations.item](Operations_item.md), [Operations.itemByName](Operations_itemByName.md), [Operations.itemByOperationId](Operations_itemByOperationId.md)

## Samples

| Name | Description |
| --- | --- |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |

## Version

Introduced in version January 2016  

