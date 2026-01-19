# DataProjects.add Method

Parent Object: [DataProjects](DataProjects.md)  

## Description

Creates a new project in the parent hub.

## Syntax

"dataProjects_var" is a variable referencing a [DataProjects](DataProjects.md) object.

```python
# Uses no optional arguments.
returnValue = dataProjects_var.add(name)

# Uses optional arguments.
returnValue = dataProjects_var.add(name, purpose, contributors)
```

## Return Value

| Type | Description |
|----|----|
| [DataProject](DataProject.md) | Returns the created DataProject object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name of the project. This is the name visible to the user. |
| purpose | string | Optional description of the purpose of the project. An empty string can be used to not specify a purpose. This is an optional argument whose default value is "". |
| contributors | string | Optional list of contributors where the list consists of email addresses separated by a comma. An empty string can be used to not specify any contributors. This is an optional argument whose default value is "". |

## Version

Introduced in version September 2016  

