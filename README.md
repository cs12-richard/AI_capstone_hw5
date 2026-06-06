# AI Capstone Homework 5 - Group 09

This repository contains the ontology-based semantic mapping submission for AI Capstone Homework 5, including the ontology, inferred results, SPARQL queries, and the project report.

## Contents

- `ontology/imports/course-affordance.ttl`: The shared course ontology, containing the foundational vocabulary required for `cap:GraspableObject`.
- `ontology/imports/course-alignment.ttl`: Course-level SKOS alignment specifications.
- `ontology/group-ontology.ttl`: The custom ontology modeled by Group 09. It includes the OWL equivalent class definitions for `cap:GraspableObject` and `g09:PressableObject`, object individuals, affordance individuals, task individuals, and group-specific properties.
- `ontology/inferred-results.ttl`: The inferred membership relations for `cap:GraspableObject` and `g09:PressableObject`.
- `queries/graspable_objects.rq`: The SPARQL query used to retrieve inferred graspable objects.
- `queries/pressable_objects.rq`: The SPARQL query used to retrieve inferred pressable objects.
- `results/graspable_objects_output.txt`: The query output results for graspable objects.
- `results/pressable_objects_output.txt`: The query output results for pressable objects.
- `src/reason_and_export.py`: A Python materializer used to infer `cap:GraspableObject` and `g09:PressableObject` and export the results.
- `report.md`: The project report.

## Group 09 Modeling Content

Group 09 covers the three basic tasks from the assignment:

- Cup Stacking: `blueCup01`, `pinkCup01`
- Cutlery Arrangement: `knife01`, `fork01`, `plate01`
- Toy Block Collection: `block01`, `basket01`

Additionally, one advanced-level object has been supplemented:
- Pump Bottle Pressing: `pumpBottle01`

Our group ontology uses the namespace `https://hcis.io/ontology/aicapstone/2026/group09/` with the prefix `g09:`. Shared course vocabulary, such as `cap:Cup`, `cap:Knife`, `cap:GraspingAffordance`, and `cap:GraspableObject`, remains under the `cap:` namespace.

## Object and Affordance Mapping Table

| Object | Type | Task Role | Affordance | Graspable (Inferred) | Pressable (Inferred) |
| --- | --- | --- | --- | --- | --- |
| `g09:blueCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | ✅ Yes | ❌ No |
| `g09:pinkCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | ✅ Yes | ❌ No |
| `g09:knife01` | `cap:Knife` | `cap:TargetObject` | grasping | ✅ Yes | ❌ No |
| `g09:fork01` | `cap:Fork` | `cap:TargetObject` | grasping | ✅ Yes | ❌ No |
| `g09:plate01` | `cap:Plate` | `cap:ReferenceObject` | support | ❌ No | ❌ No |
| `g09:block01` | `cap:ToyBlock` | `cap:CollectableObject` | grasping | ✅ Yes | ❌ No |
| `g09:basket01` | `cap:Basket` | `cap:ContainerTarget` | containment | ❌ No | ❌ No |
| `g09:pumpBottle01` | `g09:PumpBottle` | `cap:TargetObject` | pressing | ❌ No | ✅ Yes |

## Reasoning Pattern

`cap:GraspableObject` is defined in `ontology/group-ontology.ttl` using an OWL `owl:equivalentClass` definition as follows:

$cap:GraspableObject \equiv cap:PhysicalObject \sqcap \exists cap:hasAffordance.cap:GraspingAffordance$


This means that if a physical object has at least one `cap:hasAffordance` and the type of that affordance is `cap:GraspingAffordance`, it will be inferred as a `cap:GraspableObject`.

Our group ontology establishes grasping affordance individuals for the cups, knife, fork, and toy block, so these objects are inferred as `cap:GraspableObject`. The advanced-level `pumpBottle01` is only configured with a group-specific pressing affordance; therefore, it does not appear in the graspable-object query but is instead inferred as `g09:PressableObject`. The plate and basket are only configured with support and containment affordances, so they do not appear in the graspable object query results either.

## Namespace Explanation

- Shared Course Vocabulary: `cap:` = `https://hcis.io/ontology/aicapstone/2026/`
- Group 09 Vocabulary: `g09:` = `https://hcis.io/ontology/aicapstone/2026/group09/`

The Group 09 ontology places local object individuals, affordance individuals, gripper individuals, task individuals, and group-specific properties (`g09:usedInTask`, `g09:hasGripWidthMM`) under `g09:`. Shared classes and properties are maintained under `cap:`. The OWL equivalent class definition for `cap:GraspableObject` is also placed in the group ontology, as it was not provided in the course ontology.

## SPARQL Queries

The SPARQL queries are located in `queries/graspable_objects.rq` and `queries/pressable_objects.rq`, and should be executed on the "inferred graph containing both the course ontology and the group ontology".

Example query:

```sparql
PREFIX cap: [https://hcis.io/ontology/aicapstone/2026/](https://hcis.io/ontology/aicapstone/2026/)
PREFIX rdf: [http://www.w3.org/1999/02/22-rdf-syntax-ns#](http://www.w3.org/1999/02/22-rdf-syntax-ns#)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)

SELECT DISTINCT ?obj ?label ?role
WHERE {
  ?obj a cap:GraspableObject .
  OPTIONAL { ?obj rdfs:label ?label . }
  OPTIONAL { ?obj cap:hasTaskRole ?role . }
}
ORDER BY ?obj
```
## Expected Results
The expected inferred results are as follows:
* `g09:blueCup01`
* `g09:pinkCup01`
* `g09:knife01`
* `g09:fork01`
* `g09:block01`

plate01, basket01, and pumpBottle01 should not appear in the graspable results, as they are not modeled with grasping affordance.

The object expected to be inferred as a pressable object is:
* `g09:pumpBottle01`

`pumpBottle01` is derived from the advanced-level `pump_bottle_press` design, where the task description is `press the pump bottle once.`. In HW5, our group retains this task naming and uses a `pressing affordance` along with `g09:PressableObject` to semantically express that it is a pressable target object in an advanced task. We also retain semantic information useful for the assignment ontology, such as `hasObjectLabel` and` hasPoseFrame`.

## Generation and Validation Instructions
`ontology/inferred-results.ttl` records the `cap:GraspableObject` and `g09:PressableObject` members inferred by Group 09.This file is the inference output generated by the Python workflow and is submitted alongside the two query results.

## Reasoning Mechanism
This assignment utilizes a reproducible Python workflow based on RDFLib to materialize `cap:GraspableObject` and `g09:PressableObject`.

Both `cap:GraspableObject` and `g09:PressableObject` have formal OWL owl:equivalentClass definitions in `ontology/group-ontology.ttl`. Because RDFLib does not support full OWL-DL reasoning, the script checks two conditions for each candidate object:

1. The object is a `cap:PhysicalObject`, or a subclass thereof.
2. The object has at least one `cap:hasAffordance`, and the type of that affordance matches the affordance type required by the target inferred class.

If both conditions are met, `?obj a cap:GraspableObject` or `?obj a g09:PressableObject` is added to the inferred graph.

This reasoning logic faithfully reflects the semantics of `owl:equivalentClass` in the ontology. The assignment allows the use of an RDFLib-based workflow, provided the additional reasoning mechanisms used are clearly explained.

## How to Run
### Method A: Create and Activate venv
If you do not have a virtual environment yet, you can create one:
```PowerShell
python -m venv .venv
```
Activate it in Windows PowerShell:
```PowerShell
.\.venv\Scripts\Activate.ps1
```
If PowerShell restricts script execution, run this 
first:
```PowerShell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
### Method B: Install Packages and Execute Inference
```PowerShell
python -m pip install -r requirements.txt
python src/reason_and_export.py
```
## How to Validate
1. Confirm that `ontology/inferred-results.ttl` has been regenerated.
2. Confirm that `results/graspable_objects_output.txt` contains the 5 expected results.
3. Confirm that `results/pressable_objects_output.txt`contains the 1 expected result.
4. If necessary, re-run both SPARQL queries to ensure the query results match.
5. If using Widoco, confirm that `docs/group09/doc/index-en.html` has been successfully generated and that the page contains sections for classes, properties, and named individuals.
## Widoco Documentation Generation and Viewing
If you need to regenerate the ontology documentation, you can use Widoco to generate HTML files for `ontology/group-ontology.ttl.`

Prerequisite: You must have Java 17 installed on your computer, as Widoco requires a Java Runtime Environment.

Example execution command:
```PowerShell
java -jar "widoco-1.4.25-jar-with-dependencies_JDK-17.jar" -ontFile "ontology/group-ontology.ttl" -outFolder "docs/group09" -rewriteAll -uniteSections
```
Once generation is complete, the main page will be located at:
* `docs/group09/doc/index-en.html`

To view it locally, you can start a simple server in the `docs/group09/doc` directory:
```PowerShell
cd docs/group09/doc
python -m http.server 8000
```
Then open your browser to:
* http://localhost:8000/index-en.html
Or open the file directly in your browser (no server required):
```PowerShell
start docs/group09/doc/index-en.html
```
### How to Verify the Widoco Documentation

After opening `index-en.html`, please verify that the page contains the following sections:

1. **Title**: The top of the page should display "AI Capstone 2026 Group 09 Ontology" with a Release Date of 2026-05-27.
2. **Overview**: You should see the ontology URI `https://hcis.io/ontology/aicapstone/2026/group09/` and the `owl:imports` links.
3. **Cross-reference**: The following items should be listed:
   * **Class**: `graspable object` (`cap:GraspableObject`), which should include the `owl:equivalentClass` definition.
   * **Object Property**: `used in task` (`g09:usedInTask`), displaying its domain and range.
   * **Data Property**: `has grip width in millimeters` (`g09:hasGripWidthMM`), displaying its domain and range.
4. **Named Individuals**: All individuals should be listed, including:
   * **Objects**: blue cup 01, pink cup 01, knife 01, fork 01, plate 01, toy block 01, basket 01.
   * **Tasks**: cup stacking task, cutlery arrangement task, toy block collection task.
   * **Others**: group 09 gripper, and the affordance individuals for each object.

If the page is blank or missing any of these sections, please re-run the Widoco command.

---

### File Links

| File | Description |
| --- | --- |
| `group-ontology.ttl` | Group 09 Ontology (including GraspableObject definition) |
| `inferred-results.ttl` | Inferred Results |
| `course-affordance.ttl` | Shared Course Ontology (imported) |
| `course-alignment.ttl` | SKOS Alignment (imported) |
| `graspable_objects.rq` | SPARQL Query |
| `pressable_objects.rq` | SPARQL Query |
| `graspable_objects_output.txt` | Query Output |
| `pressable_objects_output.txt` | Query Output |
| `reason_and_export.py` | Reasoning Script |
| `report.md` | Project Report |

---

### Reproducible Workflow

* **Requirements**: Python 3.8+, `rdflib`, and a local `venv` (recommended).
* **Execution**: First activate the `venv`, then run `python -m pip install -r requirements.txt` followed by `python src/reason_and_export.py`.
* **Output**: This will regenerate `ontology/inferred-results.ttl`, `results/graspable_objects_output.txt`, and `results/pressable_objects_output.txt`.

---

### Team Members

* Member 1: 徐柏安 
* Member 2: 鄭家齊 
* Member 3: 許維也 
* Member 4: 顏名柔 
* Member 5: 鄒政昇 
* Member 6: 黃柏翔 


