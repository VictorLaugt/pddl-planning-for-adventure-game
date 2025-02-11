from __future__ import annotations

from abc import ABC, abstractmethod
import re
import itertools

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Sequence, Generator


TRANSLATION_TABLE = {
    ord(' '): '_', ord("'"): '_',
    ord('é'): 'e', ord('è'): 'e',
    ord('à'): 'a'
}
def to_object_name(string: str) -> str:
    return string.strip().translate(TRANSLATION_TABLE)


class Statement(ABC):
    def __repr__(self) -> str:
        field_repr = ', '.join(f"{name}={value}" for name, value in vars(self).items())
        return f"{type(self).__name__}({field_repr})"

    @abstractmethod
    def compile_objects(self) -> Generator[str]:
        pass

    @abstractmethod
    def compile_facts(self) -> Generator[str]:
        pass


class NodeStatement(Statement):
    @classmethod
    def iter_from_node_data(cls, node: str, attribute: str) -> Generator[NodeStatement]:
        yield from EmptyNode.iter_from_node_data(node, attribute)
        yield from ItemCollect.iter_from_node_data(node, attribute)
        yield from ItemUniqueChoice.iter_from_node_data(node, attribute)


class EmptyNode(NodeStatement):
    """At `location`, there is no item to collect."""
    @classmethod
    def iter_from_node_data(cls, node: str, attribute: str) -> Generator[EmptyNode]:
        location = to_object_name(node)
        if len(attribute) == 0:
            yield EmptyNode(location)

    def __init__(self, location: str) -> None:
        self.loc = location

    def compile_objects(self) -> Generator[str]:
        yield f"{self.loc} - location"

    def compile_facts(self) -> Generator[str]:
        return
        yield


class ItemCollect(NodeStatement):
    """At `location`, the player can collect `item` if he has all the `required_items`."""
    attribute_regex: re.Pattern = re.compile(r"(\?.+?\s*=>\s*)?\+.+")

    @classmethod
    def iter_from_node_data(cls, node: str, attribute: str) -> Generator[ItemCollect]:
        if cls.attribute_regex.fullmatch(attribute) is None:
            return
        location = to_object_name(node)
        parts = attribute.split('=>', maxsplit=1)

        if len(parts) == 1:
            req_dnf = [[]]
        else:
            requirement = parts[0].strip()[1:]
            req_dnf = [
                [to_object_name(item) for item in conj.split('&')]
                for conj in requirement.split('|')
            ]

        items = parts[-1].strip()[1:]
        if '|' in items or '^' in items:
            return
        for required_items, item in itertools.product(req_dnf, items.split('&')):
            yield ItemCollect(location, to_object_name(item), required_items)

    def __init__(self, location: str, item: str, required_items: Sequence[str]) -> None:
        self.loc = location
        self.item = item
        self.reqs = required_items
        print(self)

    def compile_objects(self) -> Generator[str]:
        yield f"{self.loc} - location"
        yield f"{self.item} - item"
        for item in self.reqs:
            yield f"{item} - item"

    def compile_facts(self) -> Generator[str]:
        if len(self.reqs) == 0:
            yield f"(possible_collect {self.loc} {self.item})"
        elif len(self.reqs) == 1:
            yield f"(possible_collect_if {self.loc} {self.item} {self.reqs[0]})"
        elif len(self.reqs) == 2:
            yield f"(possible_collect_if_2 {self.loc} {self.item} {self.reqs[0]} {self.reqs[1]})"
        else:
            raise ValueError(f"Excpected 0, 1, or 2 required items for {type(self).__name__}: got {len(self.reqs)}")


class ItemUniqueChoice(NodeStatement):
    """At `location`, the player can collect only one the `available_items`."""
    attribute_regex: re.Pattern = re.compile(r"\+[^\^]*\^.*")

    @classmethod
    def iter_from_node_data(cls, node: str, attribute: str) -> Generator[ItemUniqueChoice]:
        if cls.attribute_regex.fullmatch(attribute) is None:
            return

        location = to_object_name(node)
        available_items = [to_object_name(item) for item in attribute[1:].split('^')]
        yield ItemUniqueChoice(location, available_items)

    def __init__(self, location: str, available_items: Sequence[str]) -> None:
        self.loc = location
        self.available = available_items
        self.name = f"choice_{self.loc}"
        print(self)

    def compile_objects(self) -> Generator[str]:
        yield f"{self.loc} - location"
        yield f"{self.name} - choice"
        for item in self.available:
            yield f"{item} - item"

    def compile_facts(self) -> Generator[str]:
        yield f"(possible_choice {self.loc} {self.name})"
        for item in self.available:
            yield f"(offers {self.name} {item})"


class EdgeStatement(Statement):
    @classmethod
    def iter_from_edge_data(cls, src: str, dst: str, attribute: str) -> Generator[EdgeStatement]:
        src = to_object_name(src)
        dst = to_object_name(dst)
        if attribute.startswith('?'):
            for conj in attribute[1:].split('|'):
                required_items = [to_object_name(item) for item in conj.split('&')]
                yield EdgeStatement(src, dst, required_items)
        else:
            yield EdgeStatement(src, dst, ())

    def __init__(self, src: str, dst: str, required_items: Sequence[str]) -> None:
        self.src = src
        self.dst = dst
        self.reqs = required_items
        print(self)

    def compile_objects(self) -> Generator[str]:
        yield f"{self.src} - location"
        yield f"{self.dst} - location"
        for item in self.reqs:
            yield f"{item} - item"

    def compile_facts(self) -> Generator[str]:
        if len(self.reqs) == 0:
            yield f"(connected {self.src} {self.dst})"
        elif len(self.reqs) == 1:
            yield f"(connected_if {self.src} {self.dst} {self.reqs[0]})"
        else:
            raise ValueError(f"Expected 0 or 1 required item for {type(self).__name__}: got {len(self.reqs)}")


class GraphToPddlCompiler:
    def __init__(self) -> None:
        self.objects: set[str] = set()
        self.facts: set[str] = set()

    def feed(
        self,
        node_data: dict[str, str],
        edge_data: dict[tuple[str, str], str]
    ) -> None:
        for node, attribute in node_data.items():
            for node_action in NodeStatement.iter_from_node_data(node, attribute):
                self.objects.update(node_action.compile_objects())
                self.facts.update(node_action.compile_facts())

        for (src, dst), attribute in edge_data.items():
            for connection in EdgeStatement.iter_from_edge_data(src, dst, attribute):
                self.objects.update(connection.compile_objects())
                self.facts.update(connection.compile_facts())

    def digest(self, initial_node: str, final_node: str) -> str:
        initial_node = to_object_name(initial_node)
        final_node = to_object_name(final_node)
        self.objects.add(f"{initial_node} - location")
        self.objects.add(f"{final_node} - location")
        objects = '\n        '.join(self.objects)
        facts = '\n        '.join(self.facts)
        return (
            f"(define (problem map) (:domain exploration-game)\n"
            f"    (:objects\n"
            f"        p - player\n"
            f"        {objects}\n"
            f"    )\n"
            f"\n"
            f"    (:init\n"
            f"        (is_at p {initial_node})\n"
            f"        {facts}\n"
            f"    )\n"
            f"\n"
            f"    (:goal (and\n"
            f"        (is_at p {final_node})\n"
            f"    ))\n"
            f")\n"
        )


if __name__ == "__main__":
    from pathlib import Path
    from graph_file_parser import read_node_file, read_edge_file

    graph_dir = Path("game_graph")
    node_file = graph_dir.joinpath("graph-node-list.txt")
    edge_file = graph_dir.joinpath("graph-edge-list.txt")

    pddl_dir = Path("game_pddl")
    problem_file = pddl_dir.joinpath("problem.pddl")

    compiler = GraphToPddlCompiler()
    compiler.feed(
        node_data=read_node_file(node_file),
        edge_data=read_edge_file(edge_file)
    )
    problem_pddl_code = compiler.digest(
        initial_node="feu de camp",
        final_node="bunker"
    )

    with problem_file.open(mode="w") as file:
        file.write(problem_pddl_code)
