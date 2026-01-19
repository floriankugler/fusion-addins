# DataProjects.itemById Method

Parent Object: [DataProjects](DataProjects.md)  

## Description

Returns the project specified using the ID of the project.

## Syntax

"dataProjects_var" is a variable referencing a [DataProjects](DataProjects.md) object.

```python
returnValue = dataProjects_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [DataProject](DataProject.md) | Returns the project or null if a project with the specified ID is not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The ID of the project to return. This is the same ID used by the APS Data Management API. |

## Version

Introduced in version December 2020  

