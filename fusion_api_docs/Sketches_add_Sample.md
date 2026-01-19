# Sketches.add

## Description

Demonstrates the Sketches.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Sketches_add(rootComp: adsk.fusion.Design.rootComponent):
    # Get the X-Y base construction plane. 
    xYPlane = rootComp.xYConstructionPlane
    
    # Create a sketch on the indicated plane.
    sketches = rootComp.sketches
    sketch = sketches.add(xYPlane)
```

