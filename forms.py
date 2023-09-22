from plugins import RESTRICT_TO_LAB, RESTRICT_TO_INSTITUTION

form = {
    'private': {
        "order": [
          "url",
          "token"
        ],
        "required": [
          "url",
          "token",
        ],
        "layout": {},
        "properties": {
          "url": {
            "type": "string",
            "title": "Bioshare URL",
            "description": "Please enter Bioshare base URL",
            "pattern": "^https?://.+$"
#             "error_message": "Please enter a URL starting with 'https://'",
#             "validators": [
#               {
#                 "id": "regex",
#                 "options": {
#                   "regex": "testregex"
#                 }
#               }
#             ]
          },
          "token": {
            "type": "string",
            "title": "Bioshare API Token",
            "validators": [],
            "description": "Please enter Bioshare API Token",
            "restrict_to": [RESTRICT_TO_LAB]
          },
        }
        },
    'public': {
        "order": [
          "foo",
        ],
        "required": [
          "foo",
        ],
        "layout": {},
        "properties": {
          "foo": {
            "type": "string",
            "title": "Enter Foo",
            "validators": [],
            "description": "Please enter anything",
            "pattern": "^.+$"
#             "error_message": "Please enter a URL starting with 'https://'",
#             "validators": [
#               {
#                 "id": "regex",
#                 "options": {
#                   "regex": "testregex"
#                 }
#               }
#             ]
          }
        }
        }
    }