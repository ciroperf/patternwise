export class INotifier {
  send(_to, _message) {
    throw new Error("not implemented");
  }

  getChannelName() {
    throw new Error("not implemented");
  }
}

export class EmailNotifier extends INotifier {
  constructor(transport) {
    super();
    this.transport = transport;
  }

  send(to, message) {
    return this.transport.deliver({ to, subject: "Notification", body: message });
  }

  getChannelName() {
    return "email";
  }
}

export class AbstractNotifierFactory {
  createNotifier(_transport) {
    throw new Error("not implemented");
  }
}

export class NotifierFactory extends AbstractNotifierFactory {
  createNotifier(transport) {
    return new EmailNotifier(transport);
  }
}
