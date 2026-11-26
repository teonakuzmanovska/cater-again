# CaterAgain

Catering supplier rating app for corporate event teams. The current release implements the supplier catalog. Office managers can add, find, and update catering suppliers in their company's private catalog. Delivery evaluations and supplier rankings are planned.

## What runs locally

| Component | Role |
| --- | --- |
| Kong | Routes supplier API and Swagger requests on port 8000. |
| Supplier Catalog | FastAPI service that validates Keycloak access tokens and scopes supplier operations by company. |
| PostgreSQL | Stores supplier records in the `catalog` schema and Keycloak data in the `keycloak` schema. |
| Keycloak | Authenticates demo office managers and includes their assigned `company_id` in access tokens. Its admin console is on port 8081. |

## Start the stack

Install Docker with Compose and run these commands from the repository root in Windows Command Prompt. Create a repo-root `.env` with these keys and replace the password placeholders with your own local values:

```dotenv
POSTGRES_DB=suppliercatalog
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace-with-local-database-password
KEYCLOAK_ADMIN_USERNAME=admin
KEYCLOAK_ADMIN_PASSWORD=replace-with-local-admin-password
```

Keep `.env` out of Git. Use placeholders in `.env.example`.

```cmd
docker compose up -d --build
docker compose ps
```

- [Supplier API and Swagger](http://127.0.0.1:8000/suppliers/docs)
- [Keycloak Admin Console](http://127.0.0.1:8081/admin/)

For a fresh PostgreSQL volume, the scripts in `postgres/init/` create the schemas and Catalog creates the supplier table at startup. Keycloak imports the realm from `keycloak/configs/cater-again-realm.json` when the realm is first created.

### Database upgrades

For an existing deployment, apply any pending database changes before starting the updated services. The scripts in [`postgres/init/`](postgres/init/) run only when PostgreSQL initializes an empty data directory. If an upgrade introduces a new schema, apply the corresponding SQL script to the existing database.

Review the SQL in [`postgres/migrations/`](postgres/migrations/) against your current schema. When introducing company scoping, map existing suppliers to their actual companies before enforcing the `company_id` constraint. The supplied backfill uses a demo company ID and must be adapted for existing company data.

## Set up demo users

In the Keycloak Admin Console, select the **cater-again** realm. These steps also cover settings that may have been added in the console and may need to be applied on a fresh setup.

1. Under **Realm settings → User profile**, ensure the `company_id` attribute is enabled, viewable and editable by admins only, and required in the admin context.
2. Under **Clients → cater-again-client → Client scopes → cater-again-client-dedicated → Mappers**, verify the **User Attribute** mapper includes `company_id` as a string claim in access tokens. Verify an **Audience** mapper includes `cater-again-client` in access tokens. Add either mapper if absent.
3. Under **Users**, create `manager-a` with `company_id` set to `company-a`, and `manager-b` with `company_id` set to `company-b`. Give each user a first name, last name, unique demo email, and a local demo password with **Temporary** off.

## Use the supplier API

From PowerShell in the repository root, get a token for Company A:

```powershell
.\scripts\get-demo-token.ps1 -Username manager-a
```

Enter the demo user's password. The script copies the access token to your clipboard. In Swagger, click **Authorize** and paste the token alone. This helper uses the demo client's Direct Access Grants against local Keycloak.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/suppliers` | Add a supplier to the caller's catalog. |
| GET | `/suppliers` | List suppliers with optional `offset` and `limit`. |
| GET | `/suppliers/search?name=cater` | Find suppliers by a case-insensitive partial name. |
| GET | `/suppliers/{supplier_id}` | Retrieve one supplier. |
| PATCH | `/suppliers/{supplier_id}` | Update selected supplier fields. |

Example request body for **POST /suppliers**:

```json
{
  "name": "Demo Catering",
  "category": "Food",
  "description": "Lunch catering for company workshops"
}
```

### Verify company isolation

1. Call **GET /suppliers** without a token. Expect **401**.
2. Authorize as `manager-a`, create a supplier, and note its ID. Confirm it appears when you list suppliers or search for `aTeR`.
3. Clear Manager A's authorization in Swagger. Run the script with `-Username manager-b` and authorize with the new token.
4. Confirm the supplier is absent from Manager B's list and search results. A direct lookup by its ID should return **404**.

Catalog gets the company ID from the validated token and uses it for supplier reads and writes. A valid token missing a usable company ID receives **403**.

## Local commands

| Command | Purpose |
| --- | --- |
| `docker compose logs --tail=50 supplier-catalog` | Inspect Catalog startup and request errors. |
| `docker compose logs --tail=50 keycloak` | Inspect Keycloak startup and realm import. |
| `docker compose up -d --build` | Rebuild application images and start the stack. |
| `docker compose down` | Remove the containers and network while retaining the PostgreSQL volume. |

If Docker reports a port bind error, check that ports 8000 and 8081 are available. If you change Keycloak's host port, update Catalog's expected issuer and the token script URL to match. The signing-key URL inside Docker continues to use `keycloak:8080`.
