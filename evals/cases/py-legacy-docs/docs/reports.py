class HtmlFormatter:
    def heading(self, text):
        return "<h1>" + text + "</h1>"

    def paragraph(self, text):
        return "<p>" + text + "</p>"


class MarkdownFormatter:
    def heading(self, text):
        return "# " + text

    def paragraph(self, text):
        return text + "\n"


class HtmlReport:
    def __init__(self, documents):
        self.documents = documents
        self.formatter = HtmlFormatter()

    def render(self):
        # collect published documents
        published = []
        for d in self.documents:
            if d.status == "published":
                published.append(d)
        # sort by title
        published.sort(key=lambda d: d.title.lower())
        # build output
        out = [self.formatter.heading("Published documents (" + str(len(published)) + ")")]
        for d in published:
            out.append(self.formatter.paragraph(d.title + " - " + d.author.name + " (" + d.author.department.name + ")"))
        return "\n".join(out)


class MarkdownReport:
    def __init__(self, documents):
        self.documents = documents
        self.formatter = MarkdownFormatter()

    def render(self):
        # collect published documents
        published = []
        for d in self.documents:
            if d.status == "published":
                published.append(d)
        # sort by title
        published.sort(key=lambda d: d.title.lower())
        # build output
        out = [self.formatter.heading("Published documents (" + str(len(published)) + ")"), ""]
        for d in published:
            out.append(self.formatter.paragraph("- " + d.title + " by " + d.author.name))
        return "\n".join(out)
