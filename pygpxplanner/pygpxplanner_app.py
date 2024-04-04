import tkinter
import tkintermapview
from helpers.ipgeolocation import getCoords

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tkintermapview.canvas_position_marker import CanvasPositionMarker


class gpxPlanner:
    def __init__(self, master=None):
        self.createGui()
        self.coords = getCoords()
        # set current widget position and zoom
        self.mapWidget.set_position(
            self.coords.latitude, self.coords.longitude
        )  # Paris, France
        self.mapWidget.set_zoom(15)
        self.mapWidget.add_right_click_menu_command(
            label="Add Marker", command=self.add_marker_event, pass_coords=True
        )
        self.markers: list[CanvasPositionMarker] = []
        self.root_tk.mainloop()

    def createGui(self):
        # create tkinter window
        self.path = None
        
        self.root_tk = tkinter.Tk()
        self.root_tk.geometry(f"{800}x{600}")
        self.root_tk.title("pygpxplanner")

        # create map widget
        self.mapWidget = tkintermapview.TkinterMapView(
            self.root_tk, width=800, height=600, corner_radius=0
        )
        self.mapWidget.pack()

        self.mapWidget.bind_all("<Delete>", self.delete_marker_event)

        self.toolbarFrame = tkinter.Frame(
            self.mapWidget, name="toolbar", height=400, width=200, bg='cyan'
        )
        self.toolbarFrame.grid(row=0, column=1)

        self.markerListWidget = tkinter.Listbox(
            self.toolbarFrame, bg="gray", name="markerList", selectmode=tkinter.EXTENDED, height=10, width=20
        )
        self.markerListWidget.grid(row=0, column=0, columnspan=2)

        self.deleteMarkerButtonWidget = tkinter.Button(
            self.toolbarFrame, text="delete", command=self.delete_marker_event
        )
        self.deleteMarkerButtonWidget.grid(row=1, column=0)

        self.routeMarkerButton_widget = tkinter.Button(
            self.toolbarFrame, text="route", command=self.route_markers
        )
        self.routeMarkerButton_widget.grid(row=1, column=1)

    def add_marker_event(self, coords):
        markername = f"Point{len(self.markers)}"
        self.markers.append(
            self.mapWidget.set_marker(coords[0], coords[1], text=markername)
        )
        self.refresh_markerList()

    def refresh_markerList(self):
        """
        This method just deletes all entries in the markerListWidget and adds all makers out of self.markers back into it
        """
        self.markerListWidget.delete(0, self.markerListWidget.size())
        for marker in self.markers:
            self.markerListWidget.insert(len(self.markers), marker.text)

    def rename_markers(self):
        for index, marker in enumerate(self.markers):
            marker.set_text(f"Point{index}")
        self.refresh_markerList()

    def delete_marker_event(self, event=None):
        selection = self.markerListWidget.curselection()[::-1]
        for markernum in selection:
            self.markers[markernum].delete()
            self.markers.pop(markernum)
            self.markerListWidget.delete(markernum)
        self.rename_markers()
        if self.path:
            self.route_markers()

    def route_markers(self):
        if self.path:
            self.path.delete()
        self.path = self.mapWidget.set_path(
            [self.markers[i].position for i in range(len(self.markers))]
        )

app = gpxPlanner()