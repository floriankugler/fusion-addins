# ThreadDataQuery.recommendThreadData Method

Parent Object: [ThreadDataQuery](ThreadDataQuery.md)  

## Description

Method that gets the recommended thread data for a given cylinder diameter. This method is only valid for straight threads and will fail for tapered threads.

## Syntax

"threadDataQuery_var" is a variable referencing a [ThreadDataQuery](ThreadDataQuery.md) object.  

```python
(returnValue, designation, threadClass) = threadDataQuery_var.recommendThreadData(modelDiameter, isInternal, threadType)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| modelDiameter | double | The diameter of the cylinder the thread will be placed on. The units are centimeters. |
| isInternal | boolean | Indicates if the thread is an internal or external thread. |
| threadType | string | Specifies the thread type to query the thread data. |
| designation | string | The output thread designation. |
| threadClass | string | The output thread class. |

## Version

Introduced in version January 2015  

