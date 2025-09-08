"""
Staging settings for ProjectMeats.
Used for pre-production testing and validation.
"""

from .production import *

# Override production settings for staging
DEBUG = config("DEBUG", default=False, cast=bool)

# Staging-specific allowed hosts
STAGING_HOSTS = [
    "staging-projectmeats.ondigitalocean.app",
    "projectmeats-staging.herokuapp.com",  # Fallback
]

ALLOWED_HOSTS = STAGING_HOSTS + ALLOWED_HOSTS

# Less restrictive CORS for staging testing
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=False, cast=bool)

# Staging-specific logging (more verbose)
LOGGING["loggers"]["django"]["level"] = "DEBUG"
LOGGING["loggers"]["projectmeats"]["level"] = "DEBUG"

# Email backend for staging (console or file)
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", 
    default="django.core.mail.backends.console.EmailBackend"
)

# Staging-specific cache (can be less robust)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "staging-cache",
    }
}

# Allow less secure cookies for staging testing
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)

# Staging health checks (more lenient)
HEALTH_CHECK = {
    "DISK_USAGE_MAX": 95,  # percent
    "MEMORY_MIN": 50,      # MB
}