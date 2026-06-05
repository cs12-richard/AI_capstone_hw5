from __future__ import annotations

from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS


BASE_DIR = Path(__file__).resolve().parents[1]
CAP = Namespace("https://hcis.io/ontology/aicapstone/2026/")
G09 = Namespace("https://hcis.io/ontology/aicapstone/2026/group09/")


def load_graph() -> Graph:
    graph = Graph()
    course_path = BASE_DIR / "course-affordance.ttl"
    if not course_path.exists():
        course_path = BASE_DIR / "ontology" / "imports" / "course-affordance.ttl"
    paths = [course_path, BASE_DIR / "ontology" / "group-ontology.ttl"]
    for path in paths:
        graph.parse(path.as_uri(), format="turtle")
    graph.bind("cap", CAP)
    return graph


def superclasses(graph: Graph, class_uri):
    seen = set()
    stack = [class_uri]
    while stack:
        current = stack.pop()
        for parent in graph.objects(current, RDFS.subClassOf):
            if parent not in seen:
                seen.add(parent)
                stack.append(parent)
    return seen


def is_subclass_of(graph: Graph, class_uri, target_class) -> bool:
    return class_uri == target_class or target_class in superclasses(graph, class_uri)


def materialize_by_affordance(graph: Graph, affordance_class, inferred_class) -> Graph:
    inferred = Graph()
    inferred.bind("cap", CAP)
    inferred.bind("g09", G09)

    for subject, _, affordance in graph.triples((None, CAP.hasAffordance, None)):
        affordance_types = list(graph.objects(affordance, RDF.type))
        if not any(is_subclass_of(graph, affordance_type, affordance_class) for affordance_type in affordance_types):
            continue

        subject_types = list(graph.objects(subject, RDF.type))
        if any(is_subclass_of(graph, subject_type, CAP.PhysicalObject) for subject_type in subject_types):
            inferred.add((subject, RDF.type, inferred_class))

    return inferred


def run_query(merged_graph: Graph, query_name: str):
    query_path = BASE_DIR / "queries" / query_name
    query_text = query_path.read_text(encoding="utf-8")
    return list(merged_graph.query(query_text))


def term_to_text(graph: Graph, term) -> str:
    if term is None:
        return ""
    try:
        return str(term)
    except Exception:
        return repr(term)


def main() -> None:
    base_graph = load_graph()
    graspable_inferred_graph = materialize_by_affordance(base_graph, CAP.GraspingAffordance, CAP.GraspableObject)
    pressable_inferred_graph = materialize_by_affordance(base_graph, G09.PressingAffordance, G09.PressableObject)

    inferred_graph = Graph()
    inferred_graph.bind("cap", CAP)
    inferred_graph.bind("g09", G09)
    for triple in graspable_inferred_graph:
        inferred_graph.add(triple)
    for triple in pressable_inferred_graph:
        inferred_graph.add(triple)

    merged_graph = Graph()
    for triple in base_graph:
        merged_graph.add(triple)
    for triple in inferred_graph:
        merged_graph.add(triple)
    merged_graph.bind("cap", CAP)
    merged_graph.bind("g09", G09)

    inferred_path = BASE_DIR / "ontology" / "inferred-results.ttl"
    inferred_path.write_text(inferred_graph.serialize(format="turtle"), encoding="utf-8")

    graspable_results = run_query(merged_graph, "graspable_objects.rq")
    graspable_results_path = BASE_DIR / "results" / "graspable_objects_output.txt"
    graspable_lines = ["obj\tlabel\trole"]
    for row in graspable_results:
        graspable_lines.append(
            "\t".join([
                term_to_text(merged_graph, row.obj),
                term_to_text(merged_graph, row.label),
                term_to_text(merged_graph, row.role),
            ])
        )
    graspable_results_path.write_text("\n".join(graspable_lines) + "\n", encoding="utf-8")

    pressable_results = run_query(merged_graph, "pressable_objects.rq")
    pressable_results_path = BASE_DIR / "results" / "pressable_objects_output.txt"
    pressable_lines = ["obj\tlabel\trole"]
    for row in pressable_results:
        pressable_lines.append(
            "\t".join([
                term_to_text(merged_graph, row.obj),
                term_to_text(merged_graph, row.label),
                term_to_text(merged_graph, row.role),
            ])
        )
    pressable_results_path.write_text("\n".join(pressable_lines) + "\n", encoding="utf-8")

    print(f"Inferred triples: {len(inferred_graph)}")
    print(f"Graspable query rows: {len(graspable_results)}")
    for row in graspable_results:
        print(f"- {term_to_text(merged_graph, row.obj)} | {term_to_text(merged_graph, row.label)} | {term_to_text(merged_graph, row.role)}")
    print(f"Pressable query rows: {len(pressable_results)}")
    for row in pressable_results:
        print(f"- {term_to_text(merged_graph, row.obj)} | {term_to_text(merged_graph, row.label)} | {term_to_text(merged_graph, row.role)}")


if __name__ == "__main__":
    main()
