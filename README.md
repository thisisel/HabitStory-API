# Backend Service for Habit-Story

PGU     992-2 Internet Engineering Project

## Terminologies
_______________________
### Journal

User's representation of challenge, which has defined duration (e.g. 10 days)
*   Each journal is instantiated per challenge and is either public or private
*   Each journal has 1:N relationship with Pages.
*   Each story is associated per journal

### Page
Users daily log (notes) of an active journal.
User is rewarded by adding a new entry (page) to an active journal
*   page size = journal duration
*   Pages are only visible to author
*   

### Rewards
#### Story
as of now, only stories are rewarded
<br>

###  challenge
A blueprint for a journal.
*   either created by a user or superuser (also known as system's default challenges aka. kick starters).
#### Participants

Users whose journal shares the same challenge id.
If a journal is marked as private, it is still counted in participation, however remains invisible in public lists.

There are 3 types of participation defined:
* legacy participants: completed the challenge (finished not null)
* active participants: journal is active and not finished
* on-hold participants: journal is not active and not finished
----
## demanding TODOs
  * piecewise reward
  * cheer
  * streak
  * remaining days
  * check absence send -> email
  * ongoing challenge quota
  * social sign in
  * google calendar
  