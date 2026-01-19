# HttpRequest.create Method

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

Creates a new HttpRequest object.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.core.HttpRequest.create(url)

# Uses optional arguments.
returnValue = adsk.core.HttpRequest.create(url, method)
```

## Return Value

| Type                           | Description                         |
|--------------------------------|-------------------------------------|
| [HttpRequest](HttpRequest.md) | Returns the new HttpRequest object. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| url | string | The URL to make the request to. |
| method | [HttpMethods](HttpMethods.md) | The method to use for the request. The default is GetMethod. This is an optional argument whose default value is HttpMethods.GetMethod. |

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version January 2024  

