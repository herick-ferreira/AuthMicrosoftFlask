import os

# Application (client) ID of app registration
CLIENT_ID_MS = "YOUR_CLIENT_ID"

SECRET_SESSION = 'YOUR_SECRET'

# Application's generated client secret: never check this into source control!
CLIENT_SECRET_MS =  "YOUR_CLIENT_SECRET"


# You can configure your authority via environment variable
TENANT_ID_MS = "YOUR_TENANT_ID"

# Only Users Internal
AUTHORITY_MS = f"https://login.microsoftonline.com/{TENANT_ID_MS}"

# Or All Users
# AUTHORITY_MS = "https://login.microsoftonline.com/common"

REDIRECT_PATH_MS = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# Route Authentication in your domain
REDIRECT_URI_MS = "http://localhost:5000/callback"

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT_MS = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE_MS = ["User.ReadBasic.All", "User.Read"]

# Tells the Flask-session extension to store sessions in the filesystem
SESSION_TYPE_MS = "filesystem"
# Using the file system will not work in most production systems,
# it's better to use a database-backed session store instead.
