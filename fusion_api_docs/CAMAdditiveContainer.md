# CAMAdditiveContainer Object

Derived from: [OperationBase](OperationBase.md) Object  

## Description

Object that represents an additive container in an existing Setup. Note: All additive containers cannot be duplicated and depending on the type, some cannot be deleted.

## Methods

| Name | Description |
|----|----|
| [classType](CAMAdditiveContainer_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copyAfter](CAMAdditiveContainer_copyAfter.md) | Creates a duplicate of the operation in the tree after the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup. |
| [copyBefore](CAMAdditiveContainer_copyBefore.md) | Creates a duplicate of the operation in the tree before the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup. |
| [copyInto](CAMAdditiveContainer_copyInto.md) | Creates a duplicate of the operation into the given container. You can only copy into containers, such as setups or folders. Copied operation will be copied at the end of all operations already in the container. Throws an exception if a not allowed copy operation is made for example copying a setup into a setup. |
| [deleteMe](CAMAdditiveContainer_deleteMe.md) | Deletes the operation from the document. In case of a setup or folder, all containing child operations will be deleted as well. Note: Child classes may overwrite this function and throw an exception if the object cannot be deleted. |
| [duplicate](CAMAdditiveContainer_duplicate.md) | Creates a duplicate of the operation in the tree after the itself. |
| [modifyUtility](CAMAdditiveContainer_modifyUtility.md) | Get ModifyUtility for the current operation by given utility type. |
| [moveAfter](CAMAdditiveContainer_moveAfter.md) | Move operation in tree after the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup. |
| [moveBefore](CAMAdditiveContainer_moveBefore.md) | Move operation in tree before the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup. |
| [moveInto](CAMAdditiveContainer_moveInto.md) | Move operation in tree into the given container. This only works with setups, patterns and folders. Moved operation will be moved at the end of all operations already in the container. Throws an exception if a not allowed move is made for example moving a setup into a setup. |

## Properties

| Name | Description |
| --- | --- |
| [allOperations](CAMAdditiveContainer_allOperations.md) | Gets a collection containing all of the operations in this container. This includes all operations nested in folders and patterns. |
| [attributes](CAMAdditiveContainer_attributes.md) | Returns the collection of attributes associated with this object. |
| [error](CAMAdditiveContainer_error.md) | Returns a message corresponding to any active error associated with the value of this parameter. |
| [generatedDataCollection](CAMAdditiveContainer_generatedDataCollection.md) | Get the generated data associated with a given operation base instance. The type of data depends on the strategy type and might not be available for all strategy types. The available types can be found in GeneratedData.cs |
| [hasError](CAMAdditiveContainer_hasError.md) | Gets if errors were encountered when generating the operation. |
| [hasWarning](CAMAdditiveContainer_hasWarning.md) | Gets if problems were encountered when generating the operation. |
| [isLightBulbOn](CAMAdditiveContainer_isLightBulbOn.md) | Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children so this property does not indicate if the operation is actually visible, just that it should be visible if all of its parent nodes are also visible. Use the isVisible property to determine if it's actually visible. |
| [isOptional](CAMAdditiveContainer_isOptional.md) | Gets and sets the "Optional" property value of the operation. Gets/sets true if the operation is optional. |
| [isProtected](CAMAdditiveContainer_isProtected.md) | Gets and sets the "protected" property value of the operation. Gets/sets true if the operation is protected. |
| [isSelected](CAMAdditiveContainer_isSelected.md) | Gets if this operation is selected in the 'Setups' browser. |
| [isSuppressed](CAMAdditiveContainer_isSuppressed.md) | Gets and sets the "Suppressed" property value of the operation. Gets/sets true if the operation is suppressed. |
| [isValid](CAMAdditiveContainer_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](CAMAdditiveContainer_isVisible.md) | Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this operation is actually visible or not. |
| [name](CAMAdditiveContainer_name.md) | Gets and sets the name of the operation as seen in the browser. This name is unique as compared to the names of all other operations in the document. |
| [notes](CAMAdditiveContainer_notes.md) | Gets and sets the notes of the operation. |
| [objectType](CAMAdditiveContainer_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operationId](CAMAdditiveContainer_operationId.md) | Returns the id of the operation. This id is unique as compared to the ids of all other operations in the document. This id will not change when changing the order or parent of the operation. This id will remain valid when the document is saved and reloaded. |
| [parameters](CAMAdditiveContainer_parameters.md) | Gets the CAMParameters collection for this operation. |
| [parent](CAMAdditiveContainer_parent.md) | Returns the parent Setup. |
| [parentSetup](CAMAdditiveContainer_parentSetup.md) | Gets the Setup this operation belongs to. |
| [strategy](CAMAdditiveContainer_strategy.md) | Gets the name of the strategy associated with this operation. |
| [warning](CAMAdditiveContainer_warning.md) | Returns a message corresponding to any active warning associated with the value of this parameter. |

## Accessed From

[Setup.additiveContainerByType](Setup_additiveContainerByType.md)

## Version

Introduced in version July 2024  

