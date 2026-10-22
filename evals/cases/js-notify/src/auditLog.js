export class AuditLog {
  constructor() {
    this.entries = [];
  }

  record(entry) {
    this.entries.push({ ...entry, at: entry.at ?? 0 });
  }

  all() {
    return [...this.entries];
  }

  count() {
    return this.entries.length;
  }
}

export class AuditLogProxy {
  constructor(auditLog) {
    this.auditLog = auditLog;
  }

  record(entry) {
    return this.auditLog.record(entry);
  }

  all() {
    return this.auditLog.all();
  }

  count() {
    return this.auditLog.count();
  }
}
