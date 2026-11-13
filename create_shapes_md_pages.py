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

entities = []

for csv_file in ENTITIES_DIR.glob("*.csv"):
    entities = []
    entity_summary = []

    df = pd.read_csv(
        csv_file,
        sep=";",
        encoding="cp1252",
        dtype=str
    ).fillna("")

    entity = df.iloc[0]["shapeID"]
    entities.append(entity)

    shape_folder = SHAPES_DIR / entity
    docs_folder = DOCS_DIR / entity
    
    print(df.columns.tolist())
    print(df.head())

    shape_folder.mkdir(parents=True, exist_ok=True)
    docs_folder.mkdir(parents=True, exist_ok=True)

    node_shape_properties = []
    entity_index_rows = []

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
        definition = row.get("definition", "")
        scope_note = row.get("scopeNote", "")
        marc_21 = row.get("marc21", "")
        marc_21_note = row.get("marc21Note", "")
        modelling_note = row.get("modellingNote", "")
        normalization_note = row.get("normalizationNote", "")
        com_required = row.get("comRequired", "")
        issue_link = row.get("issueLink", "")

        entity_index_rows.append(
            (
                property_id,
                property_label,
                status,
                mapping,
                mandatory,
                repeatable,
                rda_label,
                marc_21,
                marc_21_note,
                modelling_note,
                issue_link,
                comment,
                scope_note
    )
)

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

        if severity:
            ttl += f"    sh:severity sh:{severity} ;\n"

        if message:
            ttl += f'    sh:message "{message}"@sv ;\n'

        ttl = ttl.rstrip(" ;\n") + " .\n"

        with open(shape_folder / f"{property_id}.ttl", "w", encoding="utf-8") as f:
            f.write(ttl)

            print("Created:", shape_folder / f"{property_id}.ttl")
         # -------------------------------------
        # Markdown
        # -------------------------------------

        if status == "deferred":
            md = f"# {property_label} (Deferred)\n\n"

        elif status == "deprecated":
            md = f"# {property_label} (Deprecated)\n\n"
        
        else:
            md = f"# {property_label}\n\n"

        md += "<table>\n"

        rows = [
            ("shapeID", entity),
            ("propertyID", property_id),
            ("propertyLabel", property_label),
            ("definition", definition),
            ("scopeNote", scope_note),
            ("mandatory", mandatory),
            ("repeatable", repeatable),
            ("valueNodeType", value_node_type),
            ("valueDataType", value_data_type),
            ("KBV IRI", kbv_iri),
            ("RDA", rda_label),
            ("RDA IRI", rda_iri),
            ("mapping", mapping),
            ("status", status),
            ("severity", severity),
            ("message", message),
            ("marc21", marc_21),
            ("marc21Note", marc_21_note),
            ("modellingNote", modelling_note),
            ("normalizationNote", normalization_note),
            ("comRequired", com_required),
            ("issueLink", issue_link),
            ("comment", comment)
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

    # -------------------------------------
    # Entity index
    # -------------------------------------

    active_count = (df["status"] == "active").sum()
    deferred_count = (df["status"] == "deferred").sum()
    deprecated_count = (df["status"] == "deprecated").sum()

    total_count = len(df)

    in_scope = active_count + deferred_count

    completion = (
        round(active_count * 100 / in_scope)
        if in_scope > 0
        else 100
    )
    entity_summary.append(
    (
        entity,
        total_count,
        active_count,
        deferred_count,
        deprecated_count,
        completion
    )
)
    filled = round(completion / 10)
    bar = "█" * filled + "░" * (10 - filled)

    entity_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{entity}</title>
    <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 2em;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th,
            td {{
                border: 1px solid #d0d0d0;
                padding: 0.4em 0.6em;
                text-align: left;
            }}

            th {{
                background-color: #f2f2f2;
            }}

            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            tr:hover {{
                background-color: #eef6ff;
            }}

            a {{
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}
    </style>

</head>
<body>

<h1>{entity}</h1>

<p><strong>Completion:</strong> {bar} {completion}%</p>

<p>
📝 Modelling note |
📖 Scope note |
🏷️ MARC 21 note |
💬 Comment |
🔗 Issue link
</p>

<h2>Status overview</h2>

<table border="1">
<tr><th>Status</th><th>Count</th></tr>
<tr><td>Total</td><td>{total_count}</td></tr>
<tr><td>Active</td><td>{active_count}</td></tr>
<tr><td>Deferred</td><td>{deferred_count}</td></tr>
<tr><td>Deprecated</td><td>{deprecated_count}</td></tr>
</table>

<h2>Properties</h2>

<table border="1">
<tr>
<th>Property</th>
<th>Label</th>
<th>Status</th>
<th>Mapping</th>
<th>Mandatory</th>
<th>Repeatable</th>
<th>RDA Label</th>
<th>MARC 21</th>
<th>Notes</th>
</tr>
"""

    for (
        prop_id,
        prop_label,
        status,
        mapping,
        mandatory,
        repeatable,
        rda_label,
        marc_21,
        marc_21_note,
        modelling_note,
        issue_link,
        comment,
        scope_note
    ) in entity_index_rows:

        property_url = (
            f"https://github.com/MikaelWetterstrom/rda_workspace"
            f"/blob/main/docs/{entity}/{prop_id}.md"
    )

        notes = ""

        if modelling_note:
           notes += f"<a href='{property_url}' target='_blank'>📝</a> "

        if issue_link:
            notes += f"<a href='{issue_link}' target='_blank'>🔗</a> "

        if comment:
            notes += f"<a href='{property_url}' target='_blank'>💬</a> "

        if scope_note:
            notes += f"<a href='{property_url}' target='_blank'>📖</a> "

        if marc_21_note:
            notes += f"<a href='{property_url}' target='_blank'>🏷️</a> "

        entity_html += (
            f"<tr>"
            f"<td><a href='{property_url}' target='_blank'>{prop_id}</a></td>"
            f"<td>{prop_label}</td>"
            f"<td>{status}</td>"
            f"<td>{mapping}</td>"
            f"<td>{mandatory}</td>"
            f"<td>{repeatable}</td>"
            f"<td>{rda_label}</td>"
            f"<td>{marc_21}</td>"
            f"<td>{notes}</td>"
            f"</tr>\n"
        )

    entity_html += """
</table>

</body>
</html>
"""

    with open(
        docs_folder / "index.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(entity_html)

    print("Created:", docs_folder / "index.html")

site_html = """
<!DOCTYPE html>
<html>
<head>
<title>RDA Application Profile Workspace</title>
<style>
body {
    font-family: Arial, sans-serif;
    margin: 2em;
    max-width: 1200px;
}

table {
    border-collapse: collapse;
    width: 100%;
}

th,
td {
    border: 1px solid #d0d0d0;
    padding: 0.4em 0.6em;
    text-align: left;
}

th {
    background-color: #f2f2f2;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

tr:hover {
    background-color: #eef6ff;
}

a {
    text-decoration: none;
    color: #005a9c;
}

a:hover {
    text-decoration: underline;
}
</style>
</head>
<body>

<h1>RDA Application Profile Workspace</h1>

<p>
Workspace for the development of an RDA Application Profile.
Generated from DCTAP source files.
</p>

<table>
<tr>
<th>Entity</th>
<th>Properties</th>
<th>Active</th>
<th>Deferred</th>
<th>Deprecated</th>
<th>Completion</th>
</tr>
"""

for (
    entity,
    total_count,
    active_count,
    deferred_count,
    deprecated_count,
    completion
) in sorted(entity_summary):

    site_html += (
        f"<tr>"
        f"<td><a href='{entity}/index.html'>{entity}</a></td>"
        f"<td>{total_count}</td>"
        f"<td>{active_count}</td>"
        f"<td>{deferred_count}</td>"
        f"<td>{deprecated_count}</td>"
        f"<td>{completion}%</td>"
        f"</tr>\n"
    )
site_html += """
</table>

</body>
</html>
"""

with open(
    DOCS_DIR / "index.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(site_html)

print("Created:", DOCS_DIR / "index.html")