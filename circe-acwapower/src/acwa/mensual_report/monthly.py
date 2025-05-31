"""
acwa.report.daily

Class to organize the daily report
"""

import os
import pathlib
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from fpdf import FPDF,XPos,YPos
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .monthly_data import get_monthly_kpi, get_monthly_ws_wf_graph, get_monthly_power_wf_graph,get_monthly_weibull, get_historical_weibull,  get_pc, freq_wind_rose, power_wind_rose

from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode

class MonthlyReportPDF(FPDF):
    
    def __init__(self, title, author, date=None, annual_mode:bool = False):
        super().__init__()
        self.title = title
        self.author = author
        # If no date is provided, use the current date
        if annual_mode:
            self.date = date.strftime("%Y") if date else datetime.today().strftime("%Y")
        else:
            self.date = date.strftime("%B %Y") if date else datetime.today().strftime("%B %Y")
        self.set_auto_page_break(auto=True, margin=15)
        # self.add_page()
    
    def header(self):
        # Rendering logo
        logo_path = pathlib.Path("assets", "ACWA_Power_logo.png")
        self.image(logo_path, 10, 5, 20)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 82, 144)  # Dark blue for main titles
        self.cell(0, 15, f'{self.title} - {self.date}', align="L")
        self.ln(15)  # line break

    def footer(self):
        # Position cursor at 1.5 cm from bottom
        self.set_y(-15)
        # Setting font: Helvetica italic 8
        self.set_font("helvetica", "I", 8)
        self.set_text_color(0, 82, 144)
        # Printing page number
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # Section helper methods
    def add_section_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 82, 144)
        self.cell(0, 10, title, align="C")
        self.ln(5)

    def add_section_header(self, header_text:str):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 82, 144)
        self.cell(0, 10, header_text, align="L")
        self.ln(7)
    
    def add_subsection_header(self, header_text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 82, 144)  # Slightly lighter color or different shade
        self.cell(0, 8, header_text, align="L")
        self.ln(5)

    def add_paragraph(self, text):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(0)
        self.multi_cell(0, 10, text)
        self.ln(1)
        

    def add_bullet_points(self, bullet_points:list):
        self.set_font("Helvetica", "", 12)
        self.set_text_color(0)
        for bullet in bullet_points:
            self.cell(10, 10, "•", 0, 0)
            self.cell(0, 10, bullet, 0, 1)
        self.ln(5)

    def add_image(self, image_path, width=100):

        # Calculate the image height based on the specified width (assuming the image aspect ratio)
        img_height = width * 0.75  # Adjust as needed for your images

        # Place the image at the current x and y positions
        current_y = self.get_y()
        if current_y + img_height > self.h - 15:  # Check if image would overflow the page
            self.add_page()  # Add a new page if needed to avoid overlap
        x_position = (self.w - width) / 2
        # Place the image at the current x and y positions
        
        y = self.get_y()
        self.image(image_path, x=x_position, y=y, w=width)

        # Update the y position to move below the image, adding a bit of spacing
        self.ln(5 + (width * 0.75))  # Adjust this factor for consistent spacing below images

        # Return the new x and y positions for reference
        return self.get_x(), self.get_y()


    def add_wf_kpi_page(self, date:datetime, id_wf:str, df_lst: list):
        
        
        grid_dict = get_monthly_kpi(date, id_wf, df_list=df_lst)

        # Define a grid structure to position elements
        grid = [
            # Column 1 (left)                         Column 2 (right)
            [("Production", f'{grid_dict["production"]} (GWh)' ),              None],
            [("Producible", f'{grid_dict["producible"]} (GWh)'),          ("Budget Production", f"P50: {grid_dict['p50']}", f"P75: {grid_dict['p75']}", f"P90: {grid_dict['p90']}", f"P99: {grid_dict['p99']}")],
            [("Availability", f'{grid_dict["availability"]} (%)' ),               ("Budget Availability", "98.00 %")],
            
            [("Producible Energy", f'{grid_dict["producible"]} (GWh)'),       ("Total Energy Loss", f'{grid_dict["total_energy_lost"]} (GWh)')],
            [("Wind Speed", f'{grid_dict["wf_windspeed"]} (m/s)'),                ("Budget Wind Speed", f'{grid_dict["lt_windspeed"]} (m/s)')],
            [("Calc. Air Density", f'{grid_dict["wf_density"]} (kg/m^3)'),       ("Long-Term Air Density", "1.15 kg/m3")],
        ]

        # Define constants for cell positions and spacing
        start_x_left = 10
        start_x_right = 100
        y_pos = self.get_y()
        row_height = 15
        

        # Loop over each row in the grid to place elements
        for i, row in enumerate(grid):
            

            for j, cell in enumerate(row):
                if cell is not None:
                    
                    text, *lst_value = cell  #[cell[1],cell[2],cell[3],cell[4]] or ""  # Ensure `value` is a string, fallback to empty if None
                    if lst_value[0] is None:
                        lst_value[0] = ''
                    color = (0, 82, 144) # cell[2] if len(cell) > 2 else (0, 0, 0)  # Default color is black unless specified

                    # Calculate x position based on column (left or right)
                    x_pos = start_x_left if j == 0 else start_x_right

                    # Set text color and font style
                    self.set_text_color(*color)
                    self.set_xy(x_pos, y_pos)
                    
                    # Draw label if it exists
                    if text:
                        self.set_font("Helvetica", "B", 10)
                        self.cell(50, 10, text, new_x=XPos.RIGHT, new_y=YPos.TOP)
                    y_max = y_pos
                    # Draw value directly below the label
                    for value in lst_value:
                        if type(value) is str and not None:
                            y_max =max(y_max,y_pos) +5
                            self.set_xy(x_pos, y_max)  # Position value slightly below text
                            self.set_font("Helvetica", "", 10)  # Regular font for values
                        
                            self.cell(50, 10, value, new_x=XPos.RIGHT, new_y=YPos.TOP)
            y_pos = y_max+ row_height

    def add_wf_bar_plot_power(self, date:datetime , id_wf: str, df_lst:list, tmp_folder: os.PathLike = '/tmp'):
        # Define the path to save the figure
        figure_tmp_path = pathlib.Path(tmp_folder, "bar_plot_power_wf_figure.png")
        get_monthly_power_wf_graph(date, id_wf,df_lst, figure_tmp_path)
        
        self.add_image(figure_tmp_path,160)
        # self.image(figure_tmp_path, 10, 25, 160)

    def add_wf_bar_plot_ws(self, date:datetime , id_wf: str, df_lst:list, tmp_folder: os.PathLike = '/tmp'):
        # Define the path to save the figure
        figure_tmp_path = pathlib.Path(tmp_folder, "bar_plot_ws_wf_figure.png")
        get_monthly_ws_wf_graph(date, id_wf,df_lst, figure_tmp_path)
        self.add_image(figure_tmp_path,160)
        # self.image(figure_tmp_path, 10, 150, 160)

    def add_weibull_dist(self, wtg_name, date, oper_10min, tmp_folder, i, wtg, annual_mode):
        
        current_y = self.get_y()
        figure_path = pathlib.Path(tmp_folder, f"{wtg_name}_weibull_monthly.png")
        img_ratio = get_monthly_weibull(path = figure_path, date = date,wtg_name=wtg_name, oper_10min=oper_10min, annual_mode=annual_mode)
        image_width = 90
        img_height = image_width * img_ratio # Adjust as needed for your images

        # Place the image at the current x and y positions
        if current_y + img_height > self.h - 15-30:  # Check if image would overflow the page. -30 corresponds to section title and subbsection header
            self.add_page()  # Add a new page if needed to avoid overlap
           
        self.add_section_header(f'2.{i} : Wind Turbine Generator {wtg}')
        self.add_subsection_header(f'2.{i}.1 : {wtg} Wind Distribution')
        if annual_mode:
            self.add_paragraph('Comparison between wind distribution histogram and fitted weibull curve for current year and historical distribution')
        else:    
            self.add_paragraph('Comparison between wind distribution histogram and fitted weibull curve for current month and historical distribution')
        
        self.image(figure_path,10, self.get_y(), image_width)

        figure_path = pathlib.Path(tmp_folder, f"{wtg_name}_weibull_historical.png")
        get_historical_weibull(figure_path,wtg_name, date, oper_10min)
        self.image(figure_path,100, self.get_y(), image_width)
         # Update the y position to move below the image, adding a bit of spacing
        self.ln(5 + img_height)  # Adjust this factor for consistent spacing below images

        # Return the new x and y positions for reference
        return self.get_x(), self.get_y()


    def add_power_curve(self, wtg_name, id_wf,date, pc_data, pc_metadata , oper_10min, densities, tmp_folder, i , wtg, annual_mode):      
        
        density = densities[(densities['id_wf']== id_wf) & (densities['main'] == True)].reset_index(drop = True).loc[0,'density']
        
        df_metadata = pc_metadata[(pc_metadata['id_wtg_complete'] == wtg_name) & (pc_metadata['density'] == f'{density}')].copy()
        df_10min = oper_10min[oper_10min['id_wtg_complete'] == wtg_name].copy()
        
        figure_path = pathlib.Path(tmp_folder, f"{wtg_name}_pc_monthly.png")
        self.ln(5)
        current_y = self.get_y()
        img_ratio = get_pc(
            path = figure_path,
            date = date,
            pc_data= pc_data,
            oper_10min= df_10min,
            df_metadata= df_metadata,
            annual_mode=annual_mode
        )
        
        image_width = 150
        x_position = (self.w - image_width) / 2
        
        img_height = image_width * img_ratio # Adjust as needed for your images

        # Place the image at the current x and y positions
        if current_y + img_height > self.h - 15-15:  # Check if image would overflow the page, second -15 corresponds to subsection header
            self.add_page()  # Add a new page if needed to avoid overlap
         
        self.add_subsection_header(f'2.{i}.2 : {wtg} Power Curve')
        if annual_mode:
            self.add_paragraph('Analyze the power against wind speed, comparing annual generated power curve and manufacturer power curve.')
        else:
            self.add_paragraph('Analyze the power against wind speed, comparing monthly generated power curve and manufacturer power curve.')


        self.image(figure_path,x = x_position, y = self.get_y(), w = image_width)
       
        
        self.ln(5 + img_height)  # Adjust this factor for consistent spacing below images

        # Return the new x and y positions for reference
        return self.get_x(), self.get_y()

    def add_wind_rose(self, date, wtg_name, oper_10min, tmp_folder, i, wtg, annual_mode):
        
        df_10min = oper_10min[oper_10min['id_wtg_complete'] == wtg_name]
        current_y = self.get_y()
        
        figure_path = pathlib.Path(tmp_folder, f"{wtg_name}_frq_wind_rose.png")
        img_ratio = freq_wind_rose(
            path = figure_path, 
            date = date, 
            data = df_10min, 
            annual_mode=annual_mode
        )
        
        image_width = 90
        img_height = image_width * img_ratio # Adjust as needed for your images

        # Place the image at the current x and y positions
        if current_y + img_height > self.h - 15-15:  # Check if image would overflow the page
            self.add_page()  # Add a new page if needed to avoid overlap
        
        self.add_subsection_header(f'2.{i}.3 : {wtg} Wind Roses')
        self.add_paragraph('Analize the power production and wind speed frequencies per sector')
        current_y = self.get_y()
        self.image(figure_path,self.get_x(), current_y, image_width)

        figure_path = pathlib.Path(tmp_folder, f"{wtg_name}_power_wind_rose.png")
        power_wind_rose(
            path = figure_path, 
            date = date, 
            data = df_10min, 
            annual_mode=annual_mode
        )
        self.image(figure_path,x = self.get_x() + image_width+5,y = current_y, w = image_width)
        
        self.ln(5 + (image_width * 1))
        return self.get_x(), self.get_y()