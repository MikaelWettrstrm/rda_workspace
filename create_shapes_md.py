import pandas as pd
from pathlib import Path

BASE = Path(".")
ENTITIES_DIR = BASE / "entities"
SHAPES_DIR = BASE / "shapes"
DOCS_DIR = BASE / "docs"

PREFIXES = """@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix kbv:  <https://id.kb.se/vocab/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

"""

for csv_file in ENTITIES_DIR.glob("*.csv"):

    df = pd.read_csv(
        csv_file,
        sep=";",
        encoding="cp1252",
        dtype=str
        ).fillna("")

    entity = df.iloc[0]["shapeID"]

    shape_folder = SHAPES_DIR / entity
    docs_folder = DOCS_DIR / entity

    shape_folder.mkdir(parents=True, exist_ok=True)
    docs_folder.mkdir(parents=True, exist_ok=True)

    node_shape_properties = []

    for _, row in df.iterrows():

        property_id = row["propertyID"]
        property_label = row["propertyLabel"]

        mandatory = row.get("mandatory", "")
        repeatable = row.get("repeatable", "")
        value_node_type = row.get("valueNodeType", "")
        value_data_type = row.get("valueDataType", "")

        kbv_iri = row.get("kbvIRI", "")
        rda_label = row.get("rdaLabel", "")
        rda_iri = row.get("rdaIRI", "")

        mapping = row.get("mapping", "")
        status = row.get("status", "")
        severity = row.get("severity", "")
        message = row.get("message", "")
        comment = row.get("comment", "")

        print("Writing:", shape_folder / f"{property_id}.ttl")
        print("Writing:", docs_folder / f"{property_id}.md")

        if status not in ["deprecated", "deferred"]:
            node_shape_properties.append(property_id)

        # -------------------------------------
        # Property Shape
        # -------------------------------------

        ttl = PREFIXES

        ttl += f"kbv:{property_id}Shape\n"
        ttl += "    a sh:PropertyShape ;\n"
        ttl += f"    sh:path kbv:{property_id} ;\n"

        if value_node_type.upper() == "IRI":
            ttl += "    sh:nodeKind sh:IRI ;\n"

        if value_data_type:
            ttl += f"    sh:datatype {value_data_type} ;\n"

        if mandatory.upper() == "TRUE":
            ttl += "    sh:minCount 1 ;\n"

        if repeatable.upper() == "FALSE":
            ttl += "    sh:maxCount 1 ;\n"

        if mapping == "exactMatch" and rda_iri:
            ttl += f"    skos:exactMatch <{rda_iri}> ;\n"

        if mapping == "closeMatch" and rda_iri:
            ttl += f"    skos:closeMatch <{rda_iri}> ;\n"

        if status in ["deprecated", "deferred"]:
            ttl += "    sh:deactivated true ;\n"

        ttl = ttl.rstrip(" ;\n") + " .\n"

        with open(shape_folder / f"{property_id}.ttl", "w", encoding="utf-8") as f:
            f.write(ttl)

            print("Created:", shape_folder / f"{property_id}.ttl")
         # -------------------------------------
        # Markdown
        # -------------------------------------

        md = f"# {property_label}\n\n"

        md += "<table>\n"

        rows = [
            ("shapeID", entity),
            ("propertyID", property_id),
            ("mandatory", mandatory),
            ("repeatable", repeatable),
            ("valueNodeType", value_node_type),
            ("valueDataType", value_data_type),
            ("KBV IRI", kbv_iri),
            ("RDA", rda_label),
            ("RDA IRI", rda_iri),
            ("mapping", mapping),
            ("status", status),
            ("comment", comment),
            ("severity", severity),
            ("message", message),
        ]

        for label, value in rows:
            if value:
                md += f"<tr><td>{label}</td><td>{value}</td></tr>\n"

        md += "</table>\n"

        print("Created:", docs_folder / f"{property_id}.md")

        with open(
            docs_folder / f"{property_id}.md",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(md)

        print("Created:", docs_folder / f"{property_id}.md")

    node_ttl = PREFIXES

    node_ttl += f"kbv:{entity}Shape\n"
    node_ttl += "    a sh:NodeShape ;\n"

    for prop in node_shape_properties:
        node_ttl += f"    sh:property kbv:{prop}Shape ;\n"

    node_ttl = node_ttl.rstrip(" ;\n") + " .\n"

    with open(
        shape_folder / "_EntityShape.ttl",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(node_ttl)

    print("Created:", shape_folder / "_EntityShape.ttl")