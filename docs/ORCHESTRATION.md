# Email
OPTIMUS currently supports email through OUTLOOK client running on the computer or server.
It uses the installed windows COM files to automate email sending natively from OUTLOOK.  
This is the preferred method for most enterprise deployments of OPTIMUS, as it does not require any further configuration or access for email sending, apart from the standard OUTLOOK already installed on the user's computer.  

## Formatting Email Body
For simple email messages, you can format and template your email body in Excel directly.  
For more complex email content structures, you can leverage Jinja templates.
- [Primer on Jinja Templating](https://realpython.com/primer-on-jinja-templating/)

Some useful guides on dealing with some common issues when setting up the HTML body of your email template  
- [Displaying large images in the email HTML body](https://blog.edmdesigner.com/html-email-width-overcoming-the-600px-limitation/#:~:text=The%20de%20facto%20standard%20for%20HTML%20emails'%20width%20is%20600%20pixels.)

