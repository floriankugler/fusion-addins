# ThreadInfo.create Method

Parent Object: [ThreadInfo](ThreadInfo.md)  

## Description

This method creates a new ThreadInfo object that can be used to create a thread or tapped-hole feature. The ThreadInfo object defines the type and size of the thread to create. When creating a thread, the type and size of the thread are defined by specifying the thread type, designation, and class. Fusion uses this information to look up the full details of the thread in tables delivered with Fusion. The ThreadDataQuery object can be used to determine valid input for this information.  

The thread type implicitly defines if the thread is standard or tapered. Tapered threads can only be used when creating tapped holes and are not supported for thread features.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.ThreadInfo.create(isTapered, isInternal, threadType, threadDesignation, threadClass, isRightHanded)
```

## Return Value

| Type | Description |
|----|----|
| [ThreadInfo](ThreadInfo.md) | Returns the newly created ThreadInfo object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| isTapered | boolean | Input Boolean that indicates if the thread is straight or tapered. |
| isInternal | boolean | Input Boolean that indicates if the thread is internal or external. A value of true indicates an internal thread. When the ThreadInfo is used to create a tapped hole, this value is ignored since it is always an internal thread. |
| threadType | string | Input string that defines the thread type. |
| threadDesignation | string | Input string that contains the thread designation. |
| threadClass | string | Input string that defines the thread class. This argument is ignored for tapered threads, so an empty string can be used. |
| isRightHanded | boolean | Input boolean that defines if the thread is right or left-handed. |

## Version

Introduced in version September 2025  

