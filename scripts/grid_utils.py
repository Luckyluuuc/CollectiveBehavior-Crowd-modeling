from mesa.space import MultiGrid

class MultiGridWithProperties(MultiGrid):
    def __init__(self, width, height, torus):
        super().__init__(width, height, torus)
        self.cell_properties = {(x, y): {} for x in range(width) for y in range(height)}

    def set_cell_property(self, pos, property_name, value):
        self.cell_properties[pos][property_name] = value

    def get_cell_property(self, pos, property_name):
        return self.cell_properties[pos].get(property_name)

    def get_cells_with_property(self, property_name, value):
        return [pos for pos, properties in self.cell_properties.items() if properties.get(property_name) == value]
