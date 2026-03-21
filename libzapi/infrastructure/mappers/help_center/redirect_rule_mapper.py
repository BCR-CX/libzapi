from libzapi.application.commands.help_center.redirect_rule_cmds import CreateRedirectRuleCmd


def to_payload_create(cmd: CreateRedirectRuleCmd) -> dict:
    return {
        "redirect_rule": {
            "brand_id": cmd.brand_id,
            "redirect_from": cmd.redirect_from,
            "redirect_to": cmd.redirect_to,
            "redirect_status": cmd.redirect_status,
        }
    }
