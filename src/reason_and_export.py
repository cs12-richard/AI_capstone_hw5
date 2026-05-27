from __future__ import annotations

from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS


BASE_DIR = Path(__file__).resolve().parents[1]
CAP = Namespace("https://hcis.io/ontology/aicapstone/2026/")


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


def materialize_graspable_objects(graph: Graph) -> Graph:
    inferred = Graph()
    inferred.bind("cap", CAP)

    for subject, _, affordance in graph.triples((None, CAP.hasAffordance, None)):
        affordance_types = list(graph.objects(affordance, RDF.type))
        if not any(is_subclass_of(graph, affordance_type, CAP.GraspingAffordance) for affordance_type in affordance_types):
            continue

        subject_types = list(graph.objects(subject, RDF.type))
        if any(is_subclass_of(graph, subject_type, CAP.PhysicalObject) for subject_type in subject_types):
            inferred.add((subject, RDF.type, CAP.GraspableObject))

    return inferred


def run_query(merged_graph: Graph):
    query_path = BASE_DIR / "queries" / "graspable_objects.rq"
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
    inferred_graph = materialize_graspable_objects(base_graph)

    merged_graph = Graph()
    for triple in base_graph:
        merged_graph.add(triple)
    for triple in inferred_graph:
        merged_graph.add(triple)
    merged_graph.bind("cap", CAP)

    inferred_path = BASE_DIR / "ontology" / "inferred-results.ttl"
    inferred_path.write_text(inferred_graph.serialize(format="turtle"), encoding="utf-8")

    results = run_query(merged_graph)
    results_path = BASE_DIR / "results" / "graspable_objects_output.txt"
    lines = ["obj\tlabel\trole"]
    for row in results:
        lines.append(
            "\t".join([
                term_to_text(merged_graph, row.obj),
                term_to_text(merged_graph, row.label),
                term_to_text(merged_graph, row.role),
            ])
        )
    results_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Inferred triples: {len(inferred_graph)}")
    print(f"Query rows: {len(results)}")
    for row in results:
        print(f"- {term_to_text(merged_graph, row.obj)} | {term_to_text(merged_graph, row.label)} | {term_to_text(merged_graph, row.role)}")


if __name__ == "__main__":
    main()
