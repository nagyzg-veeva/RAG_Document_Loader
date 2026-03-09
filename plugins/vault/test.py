from vault_connector import VaultConnector


vc = VaultConnector(
    hostname="veevasbx-commercial-tools-cs-vault-sandbox.veevavault.com",
    log_level="debug",
)

vc.login(username="commercial_tools_integration@veevasbx.com", password="Veeva2026!")

print(vc.session_id)