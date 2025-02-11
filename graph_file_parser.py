from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pathlib import Path
    from typing import Generator


def _node_interpretor(node_declaration: str) -> tuple[str, str]:
    name, _, attribute = node_declaration.partition(':')
    return name.strip().lower(), attribute.strip().lower()


def _edge_interpretor(edge_declaration: str) -> tuple[str, str, str]:
    edge_text, _, attribute = edge_declaration.partition(':')
    src_name, _, dst_name = edge_text.partition(',')
    return src_name.strip().lower(), dst_name.strip().lower(), attribute.strip().lower()


def _iter_declarations(file: Path) -> Generator[str]:
    with file.open(mode='r') as f:
        for row in f:
            row = row.strip()
            if len(row) > 0 and not row.startswith('#'):
                yield row


def read_node_file(node_file: Path) -> dict[str, str]:
    node_data = {}
    for node_declaration in _iter_declarations(node_file):
        name, attribute = _node_interpretor(node_declaration)
        node_data[name] = attribute
    return node_data


def read_edge_file(edge_file: Path) -> dict[tuple[str, str], str]:
    edge_data = {}
    for edge_declaration in _iter_declarations(edge_file):
        src_name, dst_name, attribute = _edge_interpretor(edge_declaration)
        edge_data[(src_name, dst_name)] = attribute
    return edge_data
