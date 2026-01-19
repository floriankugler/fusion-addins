# ThreadInfo.redefine Method

Parent Object: [ThreadInfo](ThreadInfo.md)  

## Description

Method that redefines an existing ThreadInfo object. This is typically used to change the thread of an existing thread or tapped hole.  

The ThreadInfo object defines the type and size of a thread by specifying the thread type, designation, and class. Fusion uses this information to look up the full details of the thread in tables delivered with Fusion. The ThreadDataQuery object can be used to determine valid input for this information.  

Tapered threads can only be used when creating or editing tapped holes and are not supported for thread features.

## Syntax

"threadInfo_var" is a variable referencing a [ThreadInfo](ThreadInfo.md) object.

```python
returnValue = threadInfo_var.redefine(isTapered, isInternal, threadType, threadDesignation, threadClass, isRightHanded)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if the redefinition was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| isTapered | boolean | Input Boolean that indicates if the thread is straight or tapered. |
| isInternal | boolean | Input Boolean that indicates if the thread is internal or external. A value of true indicates an internal thread. This value is ignored when the ThreadInfo is used for a tapped hole since they are always internal. |
| threadType | string | Input string that defines the thread type. |
| threadDesignation | string | Input string that defines the thread designation. |
| threadClass | string | Input string that defines the thread class. This argument is ignored for tapered threads. |
| isRightHanded | boolean | Input Boolean that specifies if the thread is straight or tapered. |

## Version

Introduced in version September 2025  

