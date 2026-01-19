# ThreadDataQuery.allDesignations Method

Parent Object: [ThreadDataQuery](ThreadDataQuery.md)  

## Description

returns an array/list of all the available thread designations for a thread type of a given size. Valid thread types and sizes and be obtained by using the allThreadTypes and allSizes functions.

## Syntax

"threadDataQuery_var" is a variable referencing a [ThreadDataQuery](ThreadDataQuery.md) object.

```python
returnValue = threadDataQuery_var.allDesignations(threadType, size)
```

## Return Value

| Type | Description |
|----|----|
| string\[\] | Returns the specified thread designations or empty array/list if an invalid thread type or size was specified. |

## Parameters

| Name       | Type   | Description                                  |
|------------|--------|----------------------------------------------|
| threadType | string | The thread type of the designation you want. |
| size       | string | The thread size of the designation you want. |

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  

