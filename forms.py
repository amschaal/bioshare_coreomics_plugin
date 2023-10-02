from plugins import RESTRICT_TO_LAB, RESTRICT_TO_INSTITUTION

form = {
    'private': {
        "order": [
          "url",
          "token",
          "bioshare_group",
          "filesystem"
        ],
        "required": [
          "url",
          "token",
          "filesystem"
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
              "description": "Please enter Bioshare API Token",
              "restrict_to": [RESTRICT_TO_LAB]
            },
            "bioshare_group": {
              "type": "string",
              "title": "Bioshare Group",
              "description": "Optionally enter the name of a Bioshare group that should be given read access.",
              "restrict_to": [RESTRICT_TO_LAB]
            },
            "filesystem": {
              "type": "number",
              "title": "Filesystem",
              "description": "Which Bioshare filesystem should be used for creating shares (use integer primary key)?"
            }
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