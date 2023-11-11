from mesa.visualization.modules import ChartModule

def get_chart_modules():
    chart_collisions = ChartModule(
        [{"Label": "Number of Collisions", "Color": "Black"}],
        data_collector_name='datacollector',
        canvas_height=250,
        canvas_width=500
    )

    chart_speed = ChartModule(
        [{"Label": "Average Speed", "Color": "Red"}],
        data_collector_name='datacollector',
        canvas_height=250,
        canvas_width=500
    )

    chart_movements = ChartModule(
        [{"Label": "Total Movements", "Color": "Blue"}],
        data_collector_name='datacollector',
        canvas_height=250,
        canvas_width=500
    )

    return [chart_collisions, chart_speed, chart_movements]