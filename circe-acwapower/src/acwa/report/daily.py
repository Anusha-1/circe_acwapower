"""
acwa.report.daily

Class to organize the daily report
"""

import os
import pathlib

from fpdf import FPDF
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode

class DailyReportPDF(FPDF):

    def header(self):

        # Rendering logo:
        logo_path = pathlib.Path("assets","ACWA_Power_logo.png")
        self.image(logo_path, 10, 5, 20)

        # Performing a line break:
        self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_test_table1(self, df_data: pd.DataFrame):
        # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD",size_pt=7)
        cell_height = 3 

        # Set the width for each column in units
        col_widths = [55, 15, 15, 15]  

        # Set the position in the page
        self.set_xy(10, 16) 

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT","CENTER","CENTER","CENTER"),
            width=sum(col_widths),  # The total width of the table is the sum of all column widths
        ) as table:

            # Column headers
            self.set_font("helvetica", style="B", size=7)  # Set font to bold for headers
            self.set_fill_color(225, 241, 255)
            row = table.row()
            headers = ["Total Net Gen. [MWh]", "Day", "MTD", "YTD"]
            for header in headers:
                row.cell(header)

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)
            self.set_fill_color(255,255,255) #Back to white background
         
            # Adding rows with custom names in "Total Net Gen [MWh]" column
            row_names = [
                "Actual Production (ONEE Metering -BusBar)", "Actual Production (WTG Metering)", "Internal Consumption & Electrical Losses %", "Energy & Budget Expectation (Brut) -P50(Brut) ", "                                                                                        Actual (%)",
                "Energy Estimation by the end of Month (P90 Brut)", "                                                                                        Actual (%)", "Contractual Obligations (PPA Brut)", "                                                                                        Actual (%)",
                "Lower Estimation Production Forecast (SIROCCO)", "                                                                                        Actual (%)", "Higher Estimation Production Forecast (SIROCCO)", "                                                                                        Actual (%)"
            ]

            for i, data_row in df_data.iterrows():
            # Add a new row
                row = table.row()
                row.cell(row_names[i])  # Add the custom name in the first column
                row.cell(data_row['Day'])  # Placeholder for "Day" column
                row.cell(data_row['MTD'])  # Placeholder for "MTD" column
                row.cell(data_row['YTD'])  # Placeholder for "YTD" column

    def add_test_table2(self,df_data: pd.DataFrame):
            # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD",size_pt=7)
        cell_height = 3 

        # Set the width for each column in units
        col_widths = [55, 15, 15, 15]  

        # Set the position in the page
        self.set_xy(10, 61) 

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT","CENTER","CENTER","CENTER"),
            width=sum(col_widths),  # The total width of the table is the sum of all column widths
        ) as table:
            
            self.set_font("helvetica", style="B", size=7)  # Set font to bold for headers
            self.set_fill_color(225, 241, 255)
            row = table.row()
            row.cell("", colspan=len(col_widths))  # Combine headers into one cell spanning all columns

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)
            self.set_fill_color(255, 255, 255)
         
            # Adding rows with custom names
            row_names = [
                "Wind Speed Average (m/s)", "Wind Speed Min (m/s)", "Wind Speed Max (m/s)", "Ambient Temperature Average (ºC)" 
            ]

            for i, data_row in df_data.iterrows():
            # Add a new row
                row = table.row()
                row.cell(row_names[i])  # Add the custom name in the first column
                row.cell(data_row['Day'])  # Placeholder for "Day" column
                row.cell(data_row['MTD'])  # Placeholder for "MTD" column
                row.cell(data_row['YTD'])  # Placeholder for "YTD" column



    def add_test_table3(self,df_data: pd.DataFrame):
            # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD",size_pt=7)
        cell_height = 3 

        # Set the width for each column in units
        col_widths = [55, 15, 15, 15]  

        # Set the position in the page
        self.set_xy(10, 79) 

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT","CENTER","CENTER","CENTER"),
            width=sum(col_widths),  # The total width of the table is the sum of all column widths
        ) as table:

            self.set_font("helvetica", style="B", size=7)  # Set font to bold for headers
            self.set_fill_color(225, 241, 255)
            row = table.row()
            row.cell("Production for Each tarif Period [MWh]", colspan=len(col_widths))  # Combine headers into one cell spanning all columns

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)
            self.set_fill_color(255, 255, 255)
         
            # Adding rows with custom names
            row_names = [
                "HPL (07h - 18h)", "                                                                                        Total (%)", "HPT (18h - 23h)", "                                                                                        Total (%)", "HCR (23h - 07h)", "                                                                                        Total (%)", "Total Energy Production" 
            ]

            for i, data_row in df_data.iterrows():
            # Add a new row
                row = table.row()
                row.cell(row_names[i])  # Add the custom name in the first column
                row.cell(data_row['Day'])  # Placeholder for "Day" column
                row.cell(data_row['MTD'])  # Placeholder for "MTD" column
                row.cell(data_row['YTD'])  # Placeholder for "YTD" column

        
    def add_test_table4(self, df_data: pd.DataFrame):

        # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD",size_pt=7)
        cell_height = 3 

        # Set the width for each column in units
        col_widths = [55, 15, 15, 15]  

        # Set the position in the page
        self.set_xy(10, 106) 

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT","CENTER","CENTER","CENTER"),
            width=sum(col_widths),  # The total width of the table is the sum of all column widths
        ) as table:

            self.set_font("helvetica", style="B", size=7)  # Set font to bold for headers
            self.set_fill_color(225, 241, 255)
            row = table.row()
            row.cell("Summary Availability", colspan=len(col_widths))  # Combine headers into one cell spanning all columns

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)
            self.set_fill_color(255, 255, 255)
         
            for index, data_row in df_data.iterrows():
            # Add a new row
                row = table.row()
                row.cell(index)  # Add the index
                row.cell(data_row['Day'])  # Placeholder for "Day" column
                row.cell(data_row['MTD'])  # Placeholder for "MTD" column
                row.cell(data_row['YTD'])  # Placeholder for "YTD" column
               

    def add_test_table5(self, list_info: list):

            # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD", size_pt=7)
        cell_height = 3

        # Set the width for the single column
        col_widths = [170]  # Width for the single column

        # Set the position on the page
        self.set_xy(117, 16)

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT",),  # Align the text for the single column
            width=sum(col_widths),
        ) as table:

            self.set_font("helvetica", style="B", size=7)  # Set font to bold for headers
            self.set_fill_color(225, 241, 255)
            row = table.row()
            row.cell("Operation Maintenance and HSE highlights", align='C')  # Single column, centered text

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)
            self.set_fill_color(255, 255, 255)

            # Limiting to 5 rows
            length = len(list_info)
            if length >= 5:
                list_info = list_info[:5]
            else:
                empty_rows = [""] * (5 - length)
                list_info += empty_rows

            for text in list_info:
                # Add a new row with content in the single column
                row = table.row()
                row.cell(text)  # Add content to the single column   
        
    def add_test_table6(self, list_info: list):

            # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD", size_pt=7)
        cell_height = 3

        # Set the width for the single column
        col_widths = [170]  # Width for the single column

        # Set the position on the page
        self.set_xy(117, 36)

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT",),  # Align the text for the single column
            width=sum(col_widths),
        ) as table:

            self.set_font("helvetica", style="B", size=7)  # Set font to bold for headers
            self.set_fill_color(225, 241, 255)
            row = table.row()
            row.cell("Wind Turbines Condition Monitoring System", align='C')  # Single column, centered text

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)
            self.set_fill_color(255, 255, 255)

            # Limiting to 5 rows
            length = len(list_info)
            if length >= 5:
                list_info = list_info[:5]
            else:
                empty_rows = [""] * (5 - length)
                list_info += empty_rows

            for text in list_info:
                # Add a new row with content in the single column
                row = table.row()
                row.cell(text)  # Add content to the single column    

    def add_test_table7(self, list_input: list):

            # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD",size_pt=7)
        cell_height = 3 

        # Set the width for each column in units
        col_widths = [77 , 50, 50, 50, 50]  

        # Set the position in the page
        self.set_xy(10, 139) 

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT","CENTER","CENTER","CENTER","CENTER"),
            width=sum(col_widths),  # The total width of the table is the sum of all column widths
        ) as table:
            # Section 1: Unified Column Header
            self.set_font("helvetica", style="B", size=7)  # Set font to bold for headers
            self.set_fill_color(225, 241, 255)
            row = table.row()
            row.cell("Main Events", colspan=len(col_widths), align='C') 

            # Section 2: Column headers
            self.set_font("helvetica", style="B", size=6)  # Set font to bold for headers
            self.set_fill_color(255, 255, 255)
            row = table.row()
            headers = ["Substation & MV Underground Cable","Total Duration Downtimes [h]","Daily Energy Losses [MWh]", "MTD Energy Losses [MWh]", "YTD Energy Losses [MWh]"]
            for header in headers:
                row.cell(header)

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)          
         
            for row_data in list_input:
                row = table.row()
                for elem in row_data:
                    row.cell(elem)

    def add_test_table8(self, list_input: list):

            # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD",size_pt=5.5)
        cell_height = 3 

        # Set the width for each column in units
        col_widths = [77 , 50, 50, 50, 50]  

        # Set the position in the page
        self.set_xy(10, 151) 

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT","CENTER","CENTER","CENTER","CENTER"),
            width=sum(col_widths),  # The total width of the table is the sum of all column widths
        ) as table:

            # Section 2: Column headers
            self.set_font("helvetica", style="B", size=5)  # Set font to bold for headers
            row = table.row()
            headers = ["Acces Road","","","",""]
            for header in headers:
                row.cell(header)

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)
         

            for row_data in list_input:
                row = table.row()
                for elem in row_data:
                    row.cell(elem)     

    def add_test_table9(self, df: pd.DataFrame):

            # Landscape orientation
        self.set_font("helvetica", size=5)

        # Define table styles
        headings_style_costume = FontFace(emphasis="BOLD",size_pt=7)
        cell_height = 3 

        # Set the width for each column in units
        col_widths = [77 , 50, 50, 50, 50]  

        # Set the position in the page
        self.set_xy(10, 157) 

        # Draw the table structure
        with self.table(
            align="LEFT",
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=headings_style_costume,
            line_height=cell_height,
            text_align=("LEFT","CENTER","CENTER","CENTER","CENTER"),
            width=sum(col_widths),  # The total width of the table is the sum of all column widths
        ) as table:
            # Section 1: Unified Column Header
            self.set_font("helvetica", style="B", size=7)  # Set font to bold for headers
            self.set_fill_color(225, 241, 255)
            row = table.row()
            row.cell("WTG", colspan=len(col_widths)) 

            # Section 2: Column headers
            # self.set_font("helvetica", style="B", size=6)  # Set font to bold for headers
            # row = table.row()
            # headers = ["WTG","","", "", ""]
            # for header in headers:
            #     row.cell(header)

            # Reset the font back to normal for the rest of the rows
            self.set_font("helvetica", size=5)
            self.set_fill_color(240, 248, 255)
         
            # Section 3: Adding rows with custom names
            # row_names = [
            #     "Manufacturer Downtime ", " ","Scheduled Downtime","","","Enviromental Downtime","","Total" 
            # ]

            for index, data_row in df.iterrows():
                row = table.row()
                row.cell(index)  # Add the custom name in the first column
                row.cell(data_row['duration'])  # Placeholder for 2nd column
                row.cell(data_row['losses'])  # Placeholder for 3th column
                row.cell(data_row['monthly_losses'])  # Placeholder for 4th column
                row.cell(data_row['yearly_losses'])  # Placeholder for 5th column               
            

        # Move to the next line
        self.ln(cell_height)


    def add_test_figure(self, df: pd.DataFrame, tmp_folder: os.PathLike = '/tmp'):
        # Define the path to save the figure
        figure_tmp_path = pathlib.Path(tmp_folder, "test_figure.png")
                
        # Reshape the DataFrame to a long format for plotting with hue
        df_melted = df.melt(id_vars=['month'], value_vars=['energy', 'P50', 'P90'], 
                                    var_name='type', value_name='value')
        
         # Set the figure size (width, height) in inches
        plt.figure(figsize=(12, 5.2))  # Adjust these values to change width and height

        # Create the bar plot
        sns_plot = sns.barplot(
            data=df_melted, x='month', y='value', hue='type', palette=['skyblue', 'orange', 'grey']
        )
        
        # Set labels and rotate x-axis labels for better readability
        sns_plot.set_ylabel('ACTIVE ENERGY PRODUCTION [GWh]')
        plt.xticks(rotation=90)
        plt.legend(title='Measurement', loc='upper right')  # Set the legend title and location

        # Save the plot to the specified path
        fig = sns_plot.get_figure()
        fig.savefig(figure_tmp_path, bbox_inches='tight')  # Use bbox_inches='tight' to fit labels properly

        # Add the image to the PDF
        self.image(figure_tmp_path, 115, 56, 170)


        # Performing a line break:
        # This moves the cursor for the next element
        self.ln(80) 
           
