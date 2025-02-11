from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt
import s_gd2
import csv

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional
    from pathlib import Path


def sgd2_node_pos(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, tuple[float, float]]:
    """Compute position for each node of a graph using the SGD2 algorithm
    (Stress-based Graph Drawing by Stochastic Gradient Descent): https://arxiv.org/abs/1710.04626
    """
    name2id = {}
    id2name = {}
    for i, name in enumerate(nodes):
        name2id[name] = i
        id2name[i] = name

    src_ids = []
    dst_ids = []
    for src_name, dst_name in edges:
        src_ids.append(name2id[src_name])
        dst_ids.append(name2id[dst_name])

    layout = s_gd2.layout(src_ids, dst_ids)
    node_pos = {id2name[i]: (layout[i, 0], layout[i, 1]) for i in range(len(layout))}
    return node_pos


class InteractiveGraphDrawingWindow:
    """Minimalist GUI for showing and editing the layout of a graph."""
    node_size = 250
    arrowsize = 20

    node_color = '#99ff99'
    edge_color = '#aaaaaa'

    font_kwargs = {'font_size': 8, 'font_family': 'sans-serif'}
    font_color = 'black'
    node_label_font_color = 'red'

    def __init__(
        self,
        node_data: dict[str, str],
        edge_data: dict[tuple[str, str], str],
        layout_input_file: Optional[Path]=None,
        layout_output_file: Optional[Path]=None,
    ) -> None:
        self.node_data = node_data
        self.edge_data = edge_data
        self.layout_output_file = layout_output_file

        self.graph = nx.DiGraph()
        for name in node_data.keys():
            self.graph.add_node(name)
        for src_name, dst_name in edge_data.keys():
            self.graph.add_edge(src_name, dst_name)

        self.node_pos: dict[str, tuple[float, float]] = {}
        self.node_label_pos: dict[str, tuple[float, float]] = {}

        if layout_input_file is not None and layout_input_file.is_file():
            self._load_layout_file(layout_input_file)
        else:
            self._auto_layout()

    def _auto_layout(self) -> None:
        """Automatically generates the graph layout."""
        for node, (x, y) in sgd2_node_pos(self.node_data.keys(), self.edge_data.keys()).items():
            self.node_pos[node] = (x, y)
            self.node_label_pos[node] = (x, y-0.075)
        print(f"INFO: automatically generated the graph layout")

    def _load_layout_file(self, layout_file: Path) -> None:
        """Loads the graph layout from a csv file."""
        try:
            with layout_file.open(mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    node, x, y = row
                    x, y = float(x), float(y)
                    self.node_pos[node] = (x, y)
                    self.node_label_pos[node] = (x, y-0.075)
        except:
            raise ValueError(f"Unable to parse the layout file {layout_file}")
        else:
            print(f"INFO: loaded the graph layout from {layout_file}")

    def _save_layout_file(self, layout_file: Path) -> None:
        """Saves the graph layout in a csv file."""
        with layout_file.open(mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(('node', 'x', 'y'))
            for node, (x, y) in self.node_pos.items():
                writer.writerow((node, x, y))
        print(f"INFO: saved the graph layout in {layout_file}")

    def _move_nearest_node(self, x: float, y: float) -> None:
        """Moves the nearest node to position (x, y)."""
        nearest_node = None
        min_distance = float('inf')
        for node, (node_x, node_y) in self.node_pos.items():
            distance = (x - node_x) ** 2 + (y - node_y) ** 2
            if distance < min_distance:
                min_distance = distance
                nearest_node = node
        if nearest_node is not None:
            self.node_pos[nearest_node] = x, y
            self.node_label_pos[nearest_node] = x, y-0.075

    def _draw(self) -> None:
        """Refresh the graph display."""
        plt.clf()
        nx.draw(
            self.graph, self.node_pos,
            with_labels=True, node_size=self.node_size, arrowsize=self.arrowsize,
            node_color=self.node_color, edge_color=self.edge_color,
            font_color=self.font_color, **self.font_kwargs
        )
        nx.draw_networkx_labels(
            self.graph, self.node_label_pos, self.node_data,
            font_color=self.node_label_font_color, **self.font_kwargs
        )
        nx.draw_networkx_edge_labels(
            self.graph, self.node_pos,
            edge_labels=self.edge_data, **self.font_kwargs
        )
        plt.draw()

    def save_output_layout_file(self) -> None:
        """Save the graph layout in the output layout file."""
        if self.layout_output_file is not None:
            self._save_layout_file(self.layout_output_file)

    def interactive_display(self) -> None:
        """Spawn the GUI."""
        def on_click(event):
            if event.button == 1:  # Left mouse button
                self._move_nearest_node(event.xdata, event.ydata)
                self.save_output_layout_file()
                self._draw()

        self._draw()
        plt.gcf().canvas.mpl_connect('button_press_event', on_click)
        plt.get_current_fig_manager().full_screen_toggle()
        plt.show()

    def save_image(self, image_file: Path) -> None:
        """Save the result."""
        plt.rcParams["figure.figsize"] = (16, 9)
        self._draw()
        plt.savefig(image_file, dpi=300)
        print(f"INFO: saved the graph image in {image_file}")


if __name__ == "__main__":
    from pathlib import Path
    from graph_file_parser import read_node_file, read_edge_file

    graph_dir = Path("game_graph")
    node_file = graph_dir.joinpath("graph-node-list.txt")
    edge_file = graph_dir.joinpath("graph-edge-list.txt")
    layout_file = graph_dir.joinpath("graph-layout.csv")
    image_file = graph_dir.joinpath("graph.png")

    gui = InteractiveGraphDrawingWindow(
        node_data=read_node_file(node_file),
        edge_data=read_edge_file(edge_file),
        layout_input_file=layout_file,
        layout_output_file=layout_file
    )

    gui.save_output_layout_file()
    gui.interactive_display()
    gui.save_image(image_file)

