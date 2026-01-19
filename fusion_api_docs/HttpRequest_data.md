# HttpRequest.data Property

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

Gets and sets the body data to send with this request.

## Syntax

"httpRequest_var" is a variable referencing a HttpRequest object.  

```python
# Get the value of the property.
propertyValue = httpRequest_var.data

# Set the value of the property.
httpRequest_var.data = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version January 2024  

