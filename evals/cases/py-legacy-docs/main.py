from docs.document import Document
from docs.people import Department, Person, escalation_email
from docs.reports import HtmlReport, MarkdownReport

boss = Person("Grace", "grace@example.com")
eng = Department("Engineering", boss)
boss.department = eng
alan = Person("Alan", "alan@example.com", eng)

a = Document("Zebra protocol", alan, "...")
b = Document("alpha spec", alan, "...")
for d in (a, b):
    d.submit("Grace")
    d.approve("Grace")

print(a.badge())
print(HtmlReport([a, b]).render())
print(MarkdownReport([a, b]).render())
print(escalation_email(a))
