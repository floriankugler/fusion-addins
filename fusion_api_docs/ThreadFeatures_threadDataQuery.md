# ThreadFeatures.threadDataQuery Property

Parent Object: [ThreadFeatures](ThreadFeatures.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Property that returns the ThreadDataQuery object. When creating a thread, the type and size of the thread is specified by referencing thread information defined in one of the XML files in the ThreadData folder. The ThreadDataQuery is an object that supports methods to query the existing threads defined in these files.

## Remarks

This method has been replaced by the ThreadDataQuery.create method.

## Syntax

"threadFeatures_var" is a variable referencing a ThreadFeatures object.  

```python
# Get the value of the property.
propertyValue = threadFeatures_var.threadDataQuery
```

## Property Value

This is a read only property whose value is a [ThreadDataQuery](ThreadDataQuery.md).

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  
Retired in version September 2025  

