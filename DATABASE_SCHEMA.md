# Database Schema

## Users (Standard Django Model)
| Field Name | Type | Description |
| :--- | :--- | :--- |
| id | AutoField | Primary key for the user. |
| username | String | Unique alphanumeric alias chosen by the user. |
| first_name | String | The user's given name. |
| last_name | String | The user's family name or surname. |
| email | String | The unique electronic mail address associated with the user. |
| password | String | A hash of the user's password. |
| is_staff | Boolean | Designates whether the user can log into this admin site. |
| is_active | Boolean | Designates whether this user should be treated as active. |
| is_superuser | Boolean | Designates that this user has all permissions without explicitly assigning them. |
| last_login | DateTime | The date and time when the user last logged in. |
| date_joined | DateTime | The date and time when the account was created. |

## Profile
| Field Name | Type | Description |
| :--- | :--- | :--- |
| id | AutoField | Primary key. |
| user | OneToOneField | Link to the User model. |
| profile_image | URLField | URL to the user's profile image. |
| role | String | Role of the user ('admin' or 'user'). Default: 'user'. |
| status | String | Account status ('pending', 'approved', 'rejected'). Default: 'pending'. |
| rejection_reason | TextField | Reason for rejection if the account status is 'rejected'. |

## Workspace
| Field Name | Type | Description |
| :--- | :--- | :--- |
| id | AutoField | Primary key. |
| name | String | Name of the workspace. |
| description | String | Optional description of the workspace. |
| device_id | String | Unique Serial Number of the ESP32 Device. |
| created_at | DateTime | Timestamp when the workspace was created. |
| user | ForeignKey | The user who owns this workspace. |

## CropRecommendation
| Field Name | Type | Description |
| :--- | :--- | :--- |
| id | AutoField | Primary key. |
| workspace | ForeignKey | The workspace associated with this recommendation. |
| nitrogen | Float | Nitrogen level in the soil. |
| phosphorus | Float | Phosphorus level in the soil. |
| potassium | Float | Potassium level in the soil. |
| temperature | Float | Soil temperature. |
| moisture | Float | Soil moisture level. |
| ph | Float | Soil pH level. |
| conductivity | Float | Soil conductivity. |
| recommended_crop | String | The name of the recommended crop. |
| confidence | Float | Confidence score of the recommendation. |
| all_recommendations | JSONField | Full list of recommendations and their confidence scores. |
| timestamp | DateTime | Time when the recommendation was generated. |

## Message
| Field Name | Type | Description |
| :--- | :--- | :--- |
| id | AutoField | Primary key. |
| sender | ForeignKey | The user who sent the message. |
| receiver | ForeignKey | The user who received the message. |
| content | TextField | The body of the message. |
| timestamp | DateTime | Time when the message was sent. |
| is_read | Boolean | Whether the message has been read by the receiver. |

## Log
| Field Name | Type | Description |
| :--- | :--- | :--- |
| id | AutoField | Primary key. |
| timestamp | DateTime | Time when the log was created. |
| level | String | Log level ('INFO', 'WARNING', 'ERROR', 'DEBUG'). |
| category | String | Log category ('DEVICE', 'ACTIVITY', 'SYSTEM', 'USER', 'SECURITY', 'NOTIFY'). |
| message | TextField | The log message content. |
| source | String | Source of the log event. |
| user | ForeignKey | Optional user associated with the log event. |

## PasswordReset
| Field Name | Type | Description |
| :--- | :--- | :--- |
| id | AutoField | Primary key. |
| user | ForeignKey | The user requesting the password reset. |
| reset_id | UUIDField | Unique identifier for the reset request. |
| created_when | DateTime | Time when the reset request was created. |
    