# Meeting Notes

These are my notes from the initial meeting with Shawn.
Add to these as you see fit.

## Minimum Spec
Requirements for the minimum project spec:
* Allow users to create new accounts
* Allow users to post content of interest
* Allow users to rate, review and comment on posts
* Search feature
* Provide administrators, moderators, and normal users.
* Allow for user profiles
* Ensure security; make sure that users cannot edit other user's data
  through security holes.

## Additional Requirements discussed with the client.
1. What type of information will be posted?
    * Twitter style content(short text and links) sorted by college. UMBC 
      is the initial target. Content can be sorted by class, location,
      major, etc. Content is tagged with 'hashes', similar to Twitter.
    * **Stretch Goal**: Allow users to post multimedia content, like
      pictures, videos, etc.

2. What type of information will comprises user profiles?
    * From a system perspective, user profiles will include a name,
    major, year of graduation, classes, etc. There will be a minimum 
    amount of information required by the system. Users can then choose
    which information is shared publicly.

3. What information will show up in user profiles?
    * At bare minimum, there will be an avatar (by default a Github style
    identicon) and a short bio. Additional information can be shared
    at the user's discretion.

4. What powers will administrators, moderators and users have?
    * Adminstrators have an incredible amount of power. They can manage
    content reported as spam, ban and punish users, etc. They are chosen
    from volunteers before the system is launched.
    * Moderators have less power than admins. They are able to ban a user
    if they can agree with other moderators to do so (the current projected
    requirement is three agreeing mods). They can also view spam reports
    and act upon them. Moderators are chosen by the administrator.
    * Users are able to post content, 'like' other user's content, report
    spam, etc. All users, including moderators and administrators have
    these abilities.

5. How will reviews and commenting work?
    * From a design perspective, content are treated as cards. If a user
    likes a particular piece of content, they can add it to their personal
    deck. When other users view that user's profile, they will see any
    content they have collected over time. Users can also favorite content,
    which won't add it to their deck, and also report it as spam. Comments
    are appended to the content, and can be reported as spam themselves,
    but comments can not be favorited or collected.

6. How will searching work?
    * Since content is tagged with hashes, users can search by those
    hashes. Any content that matches the search will come up. Users can
    search for as many hashes as they like, producing a stricter search
    parameter.

7. How will user reputation work?
    * User reputation will be calculated using the number of favorites
    the user has received, how many users have collected their cards,
    and the number of spam reports made against them.

