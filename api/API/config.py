import os

Domain = os.environ["DOMAIN"]

DatabaseURL = os.environ["DATABASE_URL"]

SessionSecret = os.environ["SESSION_SECRET"]

# AdminList = os.environ.get("ADMIN_LIST", "").split(",")

# DiscordOauthClientID = os.environ["DISCORD_OAUTH_CLIENT_ID"]
# DiscordOauthClientSecret = os.environ["DISCORD_OAUTH_CLIENT_SECRET"]
# DiscordOauthClientScopes = "identify"

# TwitterOauthClientID = os.environ["TWITTER_OAUTH_CLIENT_ID"]
# TwitterOauthClientSecret = os.environ["TWITTER_OAUTH_CLIENT_SECRET"]
# TwitterOauthClientScopes = "identify"

ExternalAPIToken = os.environ["EXTERNAL_API_TOKEN"]