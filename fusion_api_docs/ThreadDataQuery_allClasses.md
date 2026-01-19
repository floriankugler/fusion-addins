# ThreadDataQuery.allClasses Method

Parent Object: [ThreadDataQuery](ThreadDataQuery.md)  

## Description

Returns and array/list of all the available classes for a thread type of a given thread designation.

## Syntax

"threadDataQuery_var" is a variable referencing a [ThreadDataQuery](ThreadDataQuery.md) object.

```python
returnValue = threadDataQuery_var.allClasses(isInternal, threadType, designation)
```

## Return Value

| Type | Description |
|----|----|
| string\[\] | Returns the specified thread classes or empty array/list if an invalid thread type or designation was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| isInternal | boolean | Indicates if the thread is an internal or external thread. |
| threadType | string | The thread type of the thread class you want. |
| designation | string | The thread designation of the thread class you want. |

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  

