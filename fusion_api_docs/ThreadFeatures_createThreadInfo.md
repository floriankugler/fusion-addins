# ThreadFeatures.createThreadInfo Method

Parent Object: [ThreadFeatures](ThreadFeatures.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Method that creates a new ThreadInfo object that can be used in creating thread features. The ThreadInfo object that defines the type and size of the thread to create. When creating a thread, the type and size of the thread is specified by referencing thread information defined in one of the XML files in the ThreadData folder within the Fusion install folder. You can use the ThreadDataQuery object to query these XML files to find the specific thread you want to create. The ThreadDataQuery object can be obtained by using the ThreadFeatures.threadDataQuery property.

## Remarks

This method has been replaced by the ThreadInfo.create method.

## Syntax

"threadFeatures_var" is a variable referencing a [ThreadFeatures](ThreadFeatures.md) object.

```python
returnValue = threadFeatures_var.createThreadInfo(isInternal, threadType, threadDesignation, threadClass)
```

## Return Value

| Type | Description |
|----|----|
| [ThreadInfo](ThreadInfo.md) | Returns the newly created ThreadInfo object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| isInternal | boolean | Input Boolean that indicates if the thread is an internal or external thread. A value of true indicates an internal thread. |
| threadType | string | Input string that defines the thread type. |
| threadDesignation | string | Input string that contains the thread designation. This is input as the full thread designation that will be used in a drawing for the thread call-out. The nominal size and pitch information are extracted from the designation. |
| threadClass | string | Input string that defines the thread class. |

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  
Retired in version September 2025  

