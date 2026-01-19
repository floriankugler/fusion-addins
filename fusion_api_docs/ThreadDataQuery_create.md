# ThreadDataQuery.create Method

Parent Object: [ThreadDataQuery](ThreadDataQuery.md)  

## Description

Static method to create a new ThreadDataQuery object. The ThreadDataQuery object is a utility object that provides methods to query for the valid thread definitions defined in Fusion. This object provides similar functionality as the Thread and Hole command dialogs to find valid thread types, designations and classes which can be used to create thread and tapped hole features.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.fusion.ThreadDataQuery.create()

# Uses optional arguments.
returnValue = adsk.fusion.ThreadDataQuery.create(isTapered)
```

## Return Value

| Type                                   | Description                       |
|----------------------------------------|-----------------------------------|
| [ThreadDataQuery](ThreadDataQuery.md) | Returns a ThreadDataQuery object. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| isTapered | boolean | Specifies if you want to query for standard or tapered holes. This is an optional argument whose default value is False. |

## Version

Introduced in version September 2025  

