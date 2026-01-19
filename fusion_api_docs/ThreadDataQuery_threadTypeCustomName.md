# ThreadDataQuery.threadTypeCustomName Method

Parent Object: [ThreadDataQuery](ThreadDataQuery.md)  

## Description

Method that returns the custom name for a given thread type. The custom name is the localized name of the thread type using the current language specified for Fusion.

## Syntax

"threadDataQuery_var" is a variable referencing a [ThreadDataQuery](ThreadDataQuery.md) object.

```python
returnValue = threadDataQuery_var.threadTypeCustomName(threadType)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns the specified custom name or an empty string if an invalid thread type was specified. |

## Parameters

| Name       | Type   | Description                                          |
|------------|--------|------------------------------------------------------|
| threadType | string | The thread type you want to get the custom name for. |

## Version

Introduced in version January 2015  

