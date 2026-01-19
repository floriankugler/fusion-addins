# SelectionEventArgs.additionalEntities Property

Parent Object: [SelectionEventArgs](SelectionEventArgs.md)  

## Description

Gets or sets any additional entities that should be pre-highlighted and selected if the entity the mouse is over is selected. If you add an entity that is already selected, it will be unselected. The result of adding additional entities is the same as if they were selected one at a time by the user and the user can unselect each entity one at a time by picking it while it's selected.  

An example of how this might be used is that the user can select a group of tangentially connected edges by picking a single edge. You can use the BrepEdge.tangentiallyConnectedEdges to easily find the tangent edges and add them to the set of additional entities to be selected. These edges are pre-highlighted and then selected.  

If you are using this property you need to make sure that the selection limits for the SelectionCommandInput have been set appropriately. For example, a newly created SeletionCommandInput is set to only allow the selection of a single entity. By adding additional entities you'll need more than one entity because the entire set of entities will be added to the selection. Use the setSelectionLimits method of the SelectionCommandInput to change the number of allowed selections.  

The additional entities should all be valid based on the current selection filter.

## Syntax

"selectionEventArgs_var" is a variable referencing a SelectionEventArgs object.  

```python
# Get the value of the property.
propertyValue = selectionEventArgs_var.additionalEntities

# Set the value of the property.
selectionEventArgs_var.additionalEntities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version August 2014  

