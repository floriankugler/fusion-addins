# Occurrences.addNewExternalComponent Method

Parent Object: [Occurrences](Occurrences.md)  

## Description

Method that creates a new occurrence by creating a new external component (X-Ref) that is not saved yet. This is similar to the "New Component" command in the UI when creating an external component, where you specify a name and location but the component is created in-memory without being saved immediately. This allows programs to create and populate an external component without needing to save it first, and makes undo possible. The component will be saved automatically when the parent assembly is saved.

## Syntax

"occurrences_var" is a variable referencing an [Occurrences](Occurrences.md) object.

```python
returnValue = occurrences_var.addNewExternalComponent(componentName, targetFolder, transform)
```

## Return Value

| Type | Description |
|----|----|
| [Occurrence](Occurrence.md) | Returns the newly created occurrence or null if the creation failed. The component referenced by the occurrence can be edited but is not saved until the parent assembly is saved. |

## Parameters

| Name | Type | Description |
|----|----|----|
| componentName | string | The name for the new external component. |
| targetFolder | [DataFolder](DataFolder.md) | The DataFolder where the component will be saved when the parent assembly is saved. |
| transform | [Matrix3D](Matrix3D.md) | A transform that defines the location for the new occurrence. |

## Version

Introduced in version January 2026  

