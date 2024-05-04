import tkinter as tk
from tkinter import ttk


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_components()

    def init_components(self):
        title_label = tk.Label(self, text="World Happiness Explorer", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=(20, 10))

        subtitle_label = tk.Label(self, text="Visualize and Analyze Happiness Trends Across the Globe",
                                  font=("Helvetica", 14))
        subtitle_label.pack(pady=10)

        explore_button = ttk.Button(self, text="Explore Now", command=self.controller.show_explore)
        explore_button.pack(pady=20)

        # Placeholder for world map image
        map_image = tk.Label(self, text="Placeholder for world map", bg="lightgray", width=400, height=200)
        map_image.pack(pady=20)


class ExplorePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_components()

    def init_components(self):
        filters_frame = ttk.Frame(self)
        filters_frame.pack(pady=20)

        year_label = ttk.Label(filters_frame, text="Year:")
        year_label.grid(row=0, column=0, padx=5, pady=5)

        year_combobox = ttk.Combobox(filters_frame, values=["2015", "2016", "2017", "2018", "2019"])
        year_combobox.grid(row=0, column=1, padx=5, pady=5)

        region_label = ttk.Label(filters_frame, text="Region:")
        region_label.grid(row=0, column=2, padx=5, pady=5)

        region_combobox = ttk.Combobox(filters_frame, values=["Region 1", "Region 2", "Region 3"])
        region_combobox.grid(row=0, column=3, padx=5, pady=5)

        country_label = ttk.Label(filters_frame, text="Country:")
        country_label.grid(row=0, column=4, padx=5, pady=5)

        country_entry = ttk.Entry(filters_frame)
        country_entry.grid(row=0, column=5, padx=5, pady=5)

        graphs_frame = ttk.Frame(self)
        graphs_frame.pack(pady=20)

        line_chart_button = ttk.Button(graphs_frame, text="Line Chart")
        line_chart_button.grid(row=0, column=0, padx=5, pady=5)

        bubble_chart_button = ttk.Button(graphs_frame, text="Bubble Chart")
        bubble_chart_button.grid(row=0, column=1, padx=5, pady=5)

        choropleth_map_button = ttk.Button(graphs_frame, text="Choropleth Map")
        choropleth_map_button.grid(row=0, column=2, padx=5, pady=5)

        stats_frame = ttk.Frame(self)
        stats_frame.pack(pady=20)

        stats_label = ttk.Label(stats_frame, text="Descriptive Statistics:")
        stats_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Placeholder for statistics display
        stats_text = tk.Text(stats_frame, width=50, height=5)
        stats_text.grid(row=1, column=0, padx=5, pady=5)


class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_components()

    def init_components(self):
        about_label = tk.Label(self, text="About Page", font=("Helvetica", 16))
        about_label.pack(pady=20)
