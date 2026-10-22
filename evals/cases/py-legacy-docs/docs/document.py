import datetime


class Document:
    def __init__(self, title, author, body):
        self.title = title
        self.author = author
        self.body = body
        self.status = "draft"
        self.history = []
        self.rejection_reason = None  # only meaningful when status == "draft" after a rejection
        self.published_at = None      # only meaningful when status == "published"
        self.reviewer = None          # only meaningful when status == "review"

    def edit(self, new_body, user):
        if self.status == "draft":
            self.body = new_body
            self.history.append(("edit", user))
        elif self.status == "review":
            if user == self.reviewer:
                self.body = new_body
                self.history.append(("review-edit", user))
            else:
                raise PermissionError("only the reviewer can edit during review")
        elif self.status == "published":
            raise PermissionError("published documents are read-only")
        elif self.status == "archived":
            raise PermissionError("archived documents are read-only")

    def submit(self, reviewer):
        if self.status == "draft":
            self.status = "review"
            self.reviewer = reviewer
            self.rejection_reason = None
            self.history.append(("submit", reviewer))
        elif self.status == "review":
            raise ValueError("already in review")
        else:
            raise ValueError("cannot submit a " + self.status + " document")

    def approve(self, user):
        if self.status == "review":
            if user != self.reviewer:
                raise PermissionError("only the reviewer can approve")
            self.status = "published"
            self.published_at = datetime.date.today()
            self.reviewer = None
            self.history.append(("approve", user))
        else:
            raise ValueError("cannot approve a " + self.status + " document")

    def reject(self, user, reason):
        if self.status == "review":
            if user != self.reviewer:
                raise PermissionError("only the reviewer can reject")
            self.status = "draft"
            self.rejection_reason = reason
            self.reviewer = None
            self.history.append(("reject", user))
        else:
            raise ValueError("cannot reject a " + self.status + " document")

    def archive(self, user):
        if self.status == "published" or self.status == "draft":
            self.status = "archived"
            self.history.append(("archive", user))
        else:
            raise ValueError("cannot archive a " + self.status + " document")

    def badge(self):
        if self.status == "draft":
            return "[DRAFT]" if self.rejection_reason is None else "[DRAFT - CHANGES REQUESTED]"
        elif self.status == "review":
            return "[IN REVIEW by " + self.reviewer + "]"
        elif self.status == "published":
            return "[PUBLISHED " + self.published_at.isoformat() + "]"
        elif self.status == "archived":
            return "[ARCHIVED]"
