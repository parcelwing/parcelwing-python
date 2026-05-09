import os

from parcelwing import ParcelWing

parcel_wing = ParcelWing(api_key=os.environ["PARCEL_WING_API_KEY"])

emails = parcel_wing.emails.send(
    from_="Acme <hello@yourdomain.com>",
    to="person@example.com",
    template_alias="welcome_email",
    template_params={"first_name": "John"},
)

print(emails[0]["id"])
