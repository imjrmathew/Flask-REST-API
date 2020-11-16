# Necessry imports
import os

# Configuration for developement
class Development:

    DEBUG = True
    TESTING = False


# Configuration for Production
class Production:

    DEBUG = False
    TESTING = False

    
app_config = {
    'development': Development,
    'production': Production,
}