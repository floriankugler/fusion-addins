# PrintSettingLibrary.createQuery Method

Parent Object: [PrintSettingLibrary](PrintSettingLibrary.md)  

## Description

Creates a new PrintSettingQuery that is used to query the library for PrintSettings matching the query.

## Syntax

"printSettingLibrary_var" is a variable referencing a [PrintSettingLibrary](PrintSettingLibrary.md) object.

```python
returnValue = printSettingLibrary_var.createQuery(location)
```

## Return Value

| Type | Description |
|----|----|
| [PrintSettingQuery](PrintSettingQuery.md) | Returns a new PrintSettingQuery. The query is predefined by given parameter. |

## Parameters

| Name | Type | Description |
|----|----|----|
| location | [LibraryLocations](LibraryLocations.md) | The location specifies the LibraryLocations where to search for in the PrintSetting library. |

## Version

Introduced in version April 2023  

