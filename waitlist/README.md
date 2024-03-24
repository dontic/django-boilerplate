# Waitlist

This is a module that handles waitlists.

## Setup and usage

1. Add or uncomment `waitlist` from `INSTALLED_APPS` in `settings.py`.

2. Add the following to `urls.py`:
```python
path("waitlist/", include("waitlist.urls")),
```

3. Go to django admin and modify/add/remove any waitlist you want. As well as set 3rd party app configurations for them.

4. You can add contacts to a waitlist by going to:
```
<django-url>/waitlist/add-contact/<waitlist_id>/
```

5. You can also trigger a link to a user object or a deletion of a contact from a certail waitlist when a user is created with that same email.

## Models

- `Waitlist`: You can set up different waitlists depending on the usecase in django admin. The waitlist `default` is created by default. You can delete it or keep it as a fallback.
- `WaitlistUser`: These are the users in each waitlist. 

## Endpoints

### Add a contact
```
<django-url>/waitlist/add-contact/<waitlist_id>/
```

## 3rd party features

### Brevo

When a waitlist user is saved, you can decide to create a contact in your Brevo account and add it to a list.

This feature is really nice if you want to notify or run a marketing campain the waitlisted users later on.