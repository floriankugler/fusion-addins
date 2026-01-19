# ThreadDataQuery.allSizes Method

Parent Object: [ThreadDataQuery](ThreadDataQuery.md)  

## Description

Returns an array/list of all the available thread sizes for a given thread type. You can use the allThreadTypes property to get the available thread types.

## Syntax

"threadDataQuery_var" is a variable referencing a [ThreadDataQuery](ThreadDataQuery.md) object.

```python
returnValue = threadDataQuery_var.allSizes(threadType)
```

## Return Value

| Type | Description |
|----|----|
| string\[\] | Returns the specified thread sizes or an empty array/list if an invalid thread type was specified. |

## Parameters

| Name       | Type   | Description              |
|------------|--------|--------------------------|
| threadType | string | Specify the thread type. |

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  

