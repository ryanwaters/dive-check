# Dive Check
### _A simple application that allows you to receive text alerts when ocean conditions are to your liking_

Using the Twilio SMS API and the Magicseaweed Forecast API this app checks the primary swell heights for the next five days and if the swell is equal to or less than the max swell height you choose, you will receive a text alerting you when and where. 

Currently we only support two locations, Sonoma and Mendocino, your text will note which.

Everyday at 9am the app will check the weeks forecasted swells and check each users swell preference and send texts if conditions are met

[Check it out here](http://ryanwaters.pythonanywhere.com/)

Technology used:
* Python
* Flask
* Jinja (templating)
* Twilio API
* Magicseaweed API
