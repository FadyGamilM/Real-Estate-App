# Real-Estate-App
**this repo contains the server-side implementation of a real estate app**

## Types of users in our real estate app:
- **Realtors users who are allawoed to create lists and publish them into the app so other users can see.**
- **Admin user who can manage the app's data through admin pannel (for now).**
- **Normal users who can view and selects from offered lists.**

## Apps in our real estate project:
- **User App**
> **for managing all users of the app**
> **has its own Database**
 
 - **Listing App**
> **for managing listitng Endpoints**
> **also has its own Database**
 

## Features of Users App API:
- **register for a new account**.
- **Retrieve specific User details**
- **Login (get an access token)**
 
## Features of Listing App API:
- Available Services For Normal Users 
   - **Get published listings**.
   - **Get specific published listing details**.
   - **Search for listings**.

- Available Services For Realtor Users 
   - **Get realtor's listings**.
   - **Get specific realtor's listing details**.
   - **create a listing**.
   - **Uodate a listing**.
   - **Update the `is_published` status of a specific listing**.
   - **Delete a specific listing**.


