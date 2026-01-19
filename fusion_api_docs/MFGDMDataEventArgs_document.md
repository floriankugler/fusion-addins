# MFGDMDataEventArgs.document Property

Parent Object: [MFGDMDataEventArgs](MFGDMDataEventArgs.md)  

## Description

Provides access to the document that the event is relative to.

## Syntax

"mFGDMDataEventArgs_var" is a variable referencing a MFGDMDataEventArgs object.  

```python
# Get the value of the property.
propertyValue = mFGDMDataEventArgs_var.document
```

## Property Value

This is a read only property whose value is a [Document](Document.md).

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version July 2025  

