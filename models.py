# This file is kept for consistency with the flask guidelines
# but we're using JSON file storage instead of database models
# for this implementation as specified in the requirements

# Data structure for reference:
# {
#   "habits": [
#     {
#       "id": "unique_id",
#       "name": "Habit Name",
#       "frequency": "daily" | "weekly",
#       "created_at": "ISO datetime",
#       "tasks": [
#         {
#           "id": "unique_id",
#           "name": "Task Name",
#           "size": "small" | "medium" | "big",
#           "created_at": "ISO datetime"
#         }
#       ],
#       "completions": {
#         "YYYY-MM-DD": {
#           "task_id": true | false
#         }
#       }
#     }
#   ]
# }
