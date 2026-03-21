from libzapi.application.commands.help_center.content_subscription_cmds import CreateContentSubscriptionCmd


def to_payload_create(cmd: CreateContentSubscriptionCmd) -> dict:
    return {"subscription": {"locale": cmd.locale}}
