# `_JeopardyCTF_`

The base URL will be `/challenges`.
Here all the challenges on the site (eg. from previous competitions) will be listed, and paginated. Paginated means that at a time only a fixed number of challenges will be shown on the page, and the user can see the rest by clicking `next page` or `previous page` etc. Clicking on any of the challenges will take you to it's specific challenge name. Example URL of such a challenge page is `/challenges/challenge-name`.

For reference check out [Backdoor by SDSLabs](https://backdoor.sdslabs.co/).

For now, challenges will be uploaded by the admins only, maybe through direct entry to database (using admin panel).

## Scoring system

When an user solves a challenge by correctly submitting the flag, the allotted score will be added to the User's score. And a ManyToMany relationship will be made between the Users and the Challenges.


