import tkinter as tk
from tkinter import ttk


class ScrollingListFrame(ttk.Frame):

    def __init__(self, parent, height, *args, **kw):
        """
        Extension of the Frame class allowing for scrolling of a dynamically populated canvas populated with frames.
        Original Code: https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
        :param parent: Parent widget in which this frame is placed
        :param args: Pass through parameters
        :param kw: Pass through parameters
        """
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        v_scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, height=height, relief="sunken",
                           yscrollcommand=v_scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        v_scrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it
        self.interior = interior = ttk.Frame(canvas, relief="sunken")
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        # Incorporate Mousewheel Scrolling
        # Result: Sort of works... Events scroll smoothly, projects not so much,
        # likely because they aren't the innermost frame structure
        # @todo ask Nicholas if he knows a way to fix this issue

        def _bound_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        interior.bind('<Enter>', _bound_to_mousewheel)

        def _unbound_to_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        interior.bind('<Leave>', _unbound_to_mousewheel)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

        def _configure_interior(event):
            """
            Updates the scrollbars to match the size of the inner frame.
            :param event: Standard Python event syntax
            :return: none
            """
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_reqwidth():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            """
            Updates the inner frame's width to fill the canvas
            :param event: Standard Python event syntax
            :return: none
            """
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
