from typing import Literal
from pydantic import BaseModel, Field


class Requirement(BaseModel):
    text: str = Field(description="Die Anforderung als kurzer, eigenständiger Satz")
    category: Literal["technical", "experience", "education", "language", "soft_skill"]
    importance: Literal["must", "nice_to_have"]


class RequirementList(BaseModel):
    requirements: list[Requirement]


EXTRACT_REQUIREMENTS_PROMPT = """Du bist ein erfahrener Recruiter für technische Stellen.

Deine Aufgabe: Extrahiere aus der Stellenbeschreibung alle Anforderungen an Bewerber:innen.

Regeln:
1. Nutze nur, was Bewerber:innen mitbringen sollen (meist unter "Profil", "Anforderungen", "Das bringst du mit"). Ignoriere Benefits, Firmenbeschreibung, Gehalt und Bewerbungsablauf.
2. Fasse Technologien desselben Bereichs zu EINER Anforderung zusammen, z. B. "Erfahrung mit Python und FastAPI" statt zwei getrennter Einträge.
3. Jede Anforderung ist ein kurzer, eigenständiger Satz, der auch ohne die Stellenbeschreibung verständlich ist.
4. Höchstens 12 Anforderungen. Wenn es mehr gibt, fasse weiter zusammen.
5. importance:
   - "nice_to_have", wenn die Anforderung mit Wörtern wie "idealerweise", "wünschenswert", "von Vorteil", "gerne", "ein Plus" beschrieben wird
   - sonst "must"
6. category:
   - "technical": Programmiersprachen, Frameworks, Tools, Methoden
   - "experience": Berufserfahrung oder Projekterfahrung in einem Bereich
   - "education": Studium, Ausbildung, Abschlüsse
   - "language": Sprachkenntnisse
   - "soft_skill": Kommunikation, Teamfähigkeit, Arbeitsweise
7. Erfinde nichts. Nimm nur auf, was wirklich in der Stellenbeschreibung steht.

Beispiel:
Stellenbeschreibung: "Du hast ein abgeschlossenes Informatikstudium und erste Erfahrung mit Python und SQL. Kenntnisse in Docker sind von Vorteil. Du sprichst fließend Deutsch."
Anforderungen:
- "Abgeschlossenes Studium der Informatik" (education, must)
- "Erste Erfahrung mit Python und SQL" (technical, must)
- "Kenntnisse in Docker" (technical, nice_to_have)
- "Fließende Deutschkenntnisse" (language, must)

Antworte ausschließlich im vorgegebenen JSON-Format.

<stellenbeschreibung>
{description}
</stellenbeschreibung>
"""


def build_extract_prompt(description: str) -> str:
    return EXTRACT_REQUIREMENTS_PROMPT.format(description=description)