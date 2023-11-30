from tktimepicker import SpinTimePickerModern
from tktimepicker import constants

class TimePicker:
    def __init__(self, parent):
        self.parent = parent
        self.time_picker = SpinTimePickerModern(self.parent)

    def get_time(self, **grid_options):
        self.time_picker.addAll(constants.HOURS24)
        self.time_picker.configureAll(height=1, width=1, font=("Times", 12))
        # self.time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040", hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
        # self.time_picker.configure_separator(bg="#404040", fg="#ffffff")
        self.time_picker.addHours24()
        self.time_picker.addMinutes()

        self.time_picker.grid(**grid_options)
        return self.time_picker

    def get_selected_time(self):
        return self.time_picker.time()

    def hide_time_picker(self):
        self.time_picker.grid_remove()

    def show_time_picker(self):
        self.time_picker.grid()
