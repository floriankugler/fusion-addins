# ToolLibraries.createQuery Method

Parent Object: [ToolLibraries](ToolLibraries.md)  

## Description

Creates a new ToolQuery that is used to query the library for tools matching the query.

## Syntax

"toolLibraries_var" is a variable referencing a [ToolLibraries](ToolLibraries.md) object.

```python
returnValue = toolLibraries_var.createQuery(location)
```

## Return Value

| Type | Description |
|----|----|
| [ToolQuery](ToolQuery.md) | Returns a new ToolQuery. The query is predefined by given parameter. |

## Parameters

| Name | Type | Description |
|----|----|----|
| location | [LibraryLocations](LibraryLocations.md) | The location specifies the LibraryLocations where to search. |

## Version

Introduced in version April 2023  

