import pandas as pd
import ipywidgets as widgets
from IPython.display import display

class Rational_method:
    def __init__(self):
        self.C_r = None  # To store the selected coefficient of runoff
        self.coeffs = pd.ExcelFile(r"C:\Users\user\Desktop\Design Aspiration\Flood modelling\Python\Runoff Coeff.xlsx")
    
    def get_surface_types(self):
        # Return the available sheet names (rural, urban, man-made)
        return ['Select one', *self.coeffs.sheet_names]

    def load_surface_data(self, surface_type):
        # Load the sheet based on selected surface type (e.g., rural, urban, man-made)
        if surface_type in self.coeffs.sheet_names:
            return self.coeffs.parse(surface_type)
        else:
            raise ValueError(f"Surface type {surface_type} not found in the Excel file.")
    
    def get_surface_column(self, sheet_data, surface_type):
        """
        This method dynamically determines the column to use for surface types.
        It checks for commonly used column names (e.g., 'Urban Land Use', 'Surface Type').
        """
        # Adjust this list to match potential column names for surface types in your Excel sheets
        possible_columns = ['Urban Land Use', 'Surface Type', 'Rural Land Use', 'Man Made Surfaces']
        
        # Check which column exists in the sheet and use it
        for col in possible_columns:
            if col in sheet_data.columns:
                return col
        
        raise ValueError(f"No valid column for surface types found in {surface_type} sheet.")

    def select_surface(self):
        # Step 1: Dropdown for selecting surface type (rural, urban, man-made)
        surface_type_dropdown = widgets.Dropdown(
            options=self.get_surface_types(),
            description='Surface Type:',
            disabled=False,
        )
        
        display(surface_type_dropdown)
        
        def on_surface_type_change(change):
            selected_surface_type = change['new']
            sheet_data = self.load_surface_data(selected_surface_type)
            
            # Dynamically determine the correct column for surface types
            surface_column = self.get_surface_column(sheet_data, selected_surface_type)
            
            # Step 2: Display dropdown with surface types from the selected sheet
            self.display_surface_dropdown(sheet_data, surface_column, selected_surface_type)
        
        # Bind the dropdown event to change
        surface_type_dropdown.observe(on_surface_type_change, names='value')
    
    def display_surface_dropdown(self, sheet_data, surface_column, surface_type):
        # Step 3: Dropdown for selecting a surface within the selected sheet
        surface_dropdown = widgets.Dropdown(
            options=sheet_data[surface_column].tolist(),  # Use the dynamically selected column
            description='Surface:',
            disabled=False,
        )
        
        display(surface_dropdown)
        
        # Step 4: Button to confirm the selected surface and store its coefficient
        confirm_button = widgets.Button(description="Select Coefficient")
        display(confirm_button)

        # Define the button click event to store the selected runoff coefficient
        def on_button_click(b):
            selected_surface = surface_dropdown.value
            coeff_row = sheet_data[sheet_data[surface_column] == selected_surface]
            self.C_r = coeff_row['Average'].values[0]  # Storing the selected value in C_r
            a = self.C_r
            print(f"The runoff coefficient for {selected_surface} in {surface_type} is: {a}")
        # Bind the button click to the event
        confirm_button.on_click(on_button_click)
    
        

    def return_selected_coefficient(self):
        """Return the selected coefficient value."""
        if self.C_r is not None:
            return self.C_r
        else:
            print("No coefficient has been selected yet.")    
